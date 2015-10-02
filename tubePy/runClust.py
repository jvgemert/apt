import os, os.path, sys
import numpy as np
import h5py
import denseTraj, tubeClust, slink
import time

def dotSim(track1, track2):
    """dotprod"""
    return -np.dot(track1, track2.T)


def spatSim(track1, track2):
    """Euclidean distance"""
    AminB = track1 - track2
    return np.sqrt(np.dot(AminB, AminB.T))


def histInt(track1, track2):
    """Histogram intersection similarity"""
    return -np.sum(np.minimum(track1, track2))

# all combinations of features
featNames = ['spat', 'hogstab', 'hofstab', 'trajstab', 'mbhstab', 'spat-hogstab', 'spat-hofstab', 'spat-trajstab', 'spat-mbhstab', 'hogstab-hofstab', 'hogstab-trajstab', 'hogstab-mbhstab', 'hofstab-trajstab', 'hofstab-mbhstab', 'trajstab-mbhstab', 'spat-hogstab-hofstab', 'spat-hogstab-trajstab', 'spat-hogstab-mbhstab', 'spat-hofstab-trajstab', 'spat-hofstab-mbhstab', 'spat-trajstab-mbhstab', 'hogstab-hofstab-trajstab', 'hogstab-hofstab-mbhstab', 'hogstab-trajstab-mbhstab','hofstab-trajstab-mbhstab', 'spat-hogstab-hofstab-trajstab', 'spat-hogstab-hofstab-mbhstab', 'spat-hogstab-trajstab-mbhstab', 'spat-hofstab-trajstab-mbhstab', 'hofstab-hogstab-trajstab-mbhstab', 'spat-hogstab-hofstab-trajstab-mbhstab' ]

featName2DistFun = {'spat': spatSim, 'hogstab': spatSim, 'hofstab' : histInt, 'trajstab' : spatSim, 'mbhstab' : spatSim}

def main(featPath, nrSpatNeighbors, isTrimmedVideo, outFileName):
    """main function"""

    if isTrimmedVideo:
        featNorm = "Z"
        tempScale = 0.0
    else:
        featNorm = "MiMaN"
        tempScale = 1.0
    
    # simple timing
    tic = time.time()
    
    # a bool to check if the spatial neighborhood is already computed
    spatFeatComputed = False    

    # a bool to check if there were enough trajectories to cluster
    enoughTrajectories = True
    
    # mapping from feature to similarities (to avoid recomputing)
    feat2neighborSims = {}
    
    # if some features are already computed, only compute missing features
    doneFeatNames = []
    if not os.path.exists(outFileName):
        outHDF5file = h5py.File( outFileName, 'w')
        outHDF5file.close()
        print '\twriting features to %s' % outFileName
    else:
        try:
            print '\tadding (possible) missing features to %s' % outFileName
            inHDF5file = h5py.File( outFileName, 'r')
            doneFeatNames = inHDF5file.keys()
            inHDF5file.close()
        except IOError as e:
            outHDF5file = h5py.File( outFileName, 'w')
            outHDF5file.close()
            print '\toverwriting features to %s' % outFileName

    
    # for a given feature (or feature combination, a combination has a '-' in it)
    for featName in featNames:
        #print 'featName "%s"' % featName

        # if featName already computed, skip it.
        if featName not in doneFeatNames:
            if enoughTrajectories:

                #print 'do', featName
                #sys.exit()
                #print featName.split('-') 
                if not spatFeatComputed:
                    feat = denseTraj.getFeatFromFileByName(featPath, 'spat', tempScale)

                    nrTracks = feat.shape[0]
                    if nrTracks < nrSpatNeighbors:
                        print featName, 'not enough tracks to continue:', nrTracks, 
                        enoughTrajectories = False
                        continue

                    #vidInfo = denseTraj.getFeatFromFileByName(featPath, 'vidinfo')
                    #simMatIDs, simMat = tubeClust.getTrackNeighborsYaelYnumpyChunked(feat, nrSpatNeighbors, int(vidInfo[0]))
                    simMatIDs, _simMat = tubeClust.getTrackNeighborsYaelYnumpy(feat, nrSpatNeighbors)
                    neighborGraph = tubeClust.getNeighborGraph(simMatIDs, nrTracks)

                    spatFeatComputed = True

            if enoughTrajectories:

                # combined features are separated with a dash "-"
                combiFeatNames = featName.split('-') 
                # first do the first feature
                if combiFeatNames[0] not in feat2neighborSims.keys():
                    feat = denseTraj.getFeatFromFileByName(featPath, combiFeatNames[0], tempScale)
                
                    neighborSims = tubeClust.getNeighborSimilarities(neighborGraph, feat, featName2DistFun[combiFeatNames[0]])

                    if featNorm == 'Z':
                        neighborSims = tubeClust.normalizeNeighborSimilarities(neighborSims)
                    if featNorm == 'MiMaN':
                        neighborSims = tubeClust.normalizeNeighborSimilaritiesMiMa(neighborSims)
                    feat2neighborSims[ combiFeatNames[0] ] = neighborSims
                else:                    
                    neighborSims = feat2neighborSims[ combiFeatNames[0] ]
                    
                # add the scores of the to-be-combined features
                for indiFeat in combiFeatNames[1:]:
                    #print indiFeat,
                    if indiFeat not in feat2neighborSims.keys():
                    
                        feat = denseTraj.getFeatFromFileByName(featPath, indiFeat, tempScale)
                        neighborSimsIndi = tubeClust.getNeighborSimilarities(neighborGraph, feat, featName2DistFun[indiFeat] )
                        if featNorm == 'Z':
                            neighborSimsIndi = tubeClust.normalizeNeighborSimilarities(neighborSimsIndi)
                        if featNorm == 'MiMaN':
                            neighborSimsIndi = tubeClust.normalizeNeighborSimilaritiesMiMa(neighborSimsIndi)
                        feat2neighborSims[indiFeat] = neighborSimsIndi
                    else:
                        neighborSimsIndi = feat2neighborSims[indiFeat]
                    neighborSims = neighborSims * neighborSimsIndi

                Lambda,Pi = slink.SSclustSlink(neighborGraph, neighborSims, nrTracks)
                mergedTracks = tubeClust.convertPointerRepresentation(np.array(Lambda), Pi, nrTracks)

            toc = time.time()

            print '; Time: %.2fs' % (toc-tic)

            if not enoughTrajectories:
                mergedTracks = -1

            print '\twrite to: %s, "%s"' % (outFileName, featName)
            outHDF5file = h5py.File( outFileName, 'a')
            outHDF5file.create_dataset(featName, data=mergedTracks)
            outHDF5file.close()

    #  write time

    # write timing to disk
    #fOut = open(outFileName.replace('.hdf5', '.time'), 'w')
    #fOut.write('%f' % (toc-tic) )
    #fOut.close()


# if run as a command (ie: not imported)
if __name__ == "__main__":    
                                                                                                                                                                                
    if len(sys.argv) < 4:
        raise ValueError('not enough input arguments')

    featPath = sys.argv[1]
    nrSpatNeighbors = int(sys.argv[2])
    isTrimmedVideo = int(sys.argv[3])
    outFileName = sys.argv[4]
    
    outPath = os.path.dirname(outFileName)
    if not os.path.exists(outPath):
        os.makedirs(outPath)
        
    main(featPath, nrSpatNeighbors, isTrimmedVideo, outFileName)

