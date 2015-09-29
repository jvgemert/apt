import os, os.path, sys
import h5py

import numpy as np
import denseTraj

def main(inFileName, featPath, nrTrajThresh4Tube, outFileName):

    #print inFileName, featPath, nrTrajThresh4Tube, outFileName
    #sys.exit()

    outPath = os.path.dirname(outFileName)
    if not os.path.exists(outPath):
        os.makedirs(outPath)


    # output file
    print '\tWrite tubes to: %s' % (outFileName)
    outHDF5fileTubes = h5py.File( outFileName, 'w')


    # get the trajectory locations
    geoFeat = denseTraj.getFeatFromFileByName(featPath, 'geo')
    # get vid info (length, width, height)
    vidInfo = denseTraj.getFeatFromFileByName(featPath, 'vidinfo')
    xmax = vidInfo[1]
    ymax = vidInfo[2]

    # input cluster file
    inHDF5fileClusts = h5py.File( inFileName, 'r')

    propOutstartID = 0
    for featName in inHDF5fileClusts:
    
        # get the clustered proposals for this feature type in SLINK pointer-representation
        #featName = featNames[featNameID] 
        #fnameSS = os.path.join(inPath, featName + suffixIn + '.npy')
        #mergedTracks = np.load( fnameSS )
        
        dset = inHDF5fileClusts[featName]
        mergedTracks = dset[()]
        
        # convert pointer-representation to tube proposals and write to disk
        if len(mergedTracks.shape) > 1 and mergedTracks.shape[0] > 1:
        
            tubeProposals = denseTraj.createProposals(mergedTracks, geoFeat, nrTrajThresh4Tube, xmax, ymax)
            nrProposals = len(tubeProposals)
            print '\tFeature: "%s"; Number of proposals: %d' % (featName, nrProposals),

            # if OK
            if nrProposals > 0:

                # write to file
                #print '; writing proposals:', outPath
                tubeProposals.writeHDF5(outHDF5fileTubes, propOutstartID)
                propOutstartID += nrProposals
                print 'tot:', propOutstartID
    # close the file            
    outHDF5fileTubes.close()

                
# if run as a command (ie: not imported)
if __name__ == "__main__":    

    if len(sys.argv) < 4:
        raise ValueError('not enough input arguments')

    inFileName = sys.argv[1]
    featPath = sys.argv[2]
    nrTrajThresh4Tube = int(sys.argv[3])
    outFileName = sys.argv[4]

    main(inFileName, featPath, nrTrajThresh4Tube, outFileName)

