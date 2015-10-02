import os, os.path, sys
import numpy as np
import h5py
import denseTraj
import tubeIoU

from tubeList import TubeList 


def main(doTubeFormat, inFileName, outIoUfile, gtPath, nrTrajThresh4Tube=-1, featPath=''):

    # check if cython is used    
    tubeIoU.check()
    
    # read ground truth tubes
    print '\tRead ground truth;',
    gtTubes = TubeList()
    gtTubes.readHDF5(gtPath)

    outPath = os.path.dirname(outIoUfile)
    if not os.path.exists( outPath ):
        os.makedirs(outPath)

    # if proposals are stored as Tubes already, read them
    if doTubeFormat:
        tubeProposals = TubeList()
        tubeProposals.readHDF5(inFileName)        
        # initialize with a single name
        inHDF5fileClusts = ['tubes']
    else:
        # otherwise, read trajectory positions and vidinfo to generate proposals later
        print '\tGet trajectory positions;', 
        geoFeat = denseTraj.getFeatFromFileByName(featPath, 'geo')
        print '\tGet video dimensions;', 
        vidInfo = denseTraj.getFeatFromFileByName(featPath, 'vidinfo')
        xmax = vidInfo[1]
        ymax = vidInfo[2]
        # input cluster file
        inHDF5fileClusts = h5py.File( inFileName, 'r')

    aboMax = []
    # go over all features
    
    for featName in inHDF5fileClusts:
    
        if not doTubeFormat:
            # get the clustered proposals for this feature type in SLINK pointer-representation
            dset = inHDF5fileClusts[featName]
            mergedTracks = dset[()]           
            # convert pointer-representation to tube proposals 
            if len(mergedTracks.shape) > 1 and mergedTracks.shape[0] > 1:
                tubeProposals = denseTraj.createProposals(mergedTracks, geoFeat, nrTrajThresh4Tube, xmax, ymax)
       
        nrProposals = len(tubeProposals)
        print '\tFeature: "%s", number of proposals: %d;' % (featName,nrProposals),
        # if ok             
        if nrProposals > 0:

            # get Intersection over Union scores
            aboMatCur = tubeProposals.computeTubeOverlap(gtTubes)
                
            # if first feature, write to new file otherwise append to existing file            
            if aboMax == []:
                fileOut = open(outIoUfile, 'w')
            else:
                fileOut = open(outIoUfile, 'a')
            
            # write scores
            for prop in range(aboMatCur.shape[0]):
                for score in aboMatCur[prop,:]:
                    fileOut.write('%f ' % score)
                fileOut.write('\n')
            fileOut.close()

            # keep track of the maximum score
            curMax = np.max(aboMatCur, axis=0)
            if aboMax == []:
                aboMax = curMax
            else:
                aboMax = np.maximum( aboMax, curMax)

            print 'Best IoUs:',  curMax, '; Best so far:', aboMax
            
    print '\tWriting IoU scores to', outIoUfile    
    if not doTubeFormat:
        inHDF5fileClusts.close()

# if run as a command (ie: not imported)
if __name__ == "__main__":    

    if len(sys.argv) != 4  and len(sys.argv) != 6:
        print 'nr arguments', len(sys.argv)
        raise ValueError('not enough input arguments')


    inFileName = sys.argv[1]
    outIoUfile = sys.argv[2]
    gtPath = sys.argv[3]

    # if tube format
    if len(sys.argv) == 4:
        main(True, inFileName, outIoUfile, gtPath)
    else:    
        nrTrajThresh4Tube = int(sys.argv[4])
        featPath = sys.argv[5]
        main(False, inFileName, outIoUfile, gtPath, nrTrajThresh4Tube, featPath)

