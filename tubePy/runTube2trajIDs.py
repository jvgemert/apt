import os, os.path, sys
import numpy as np
import h5py
import denseTraj
import tube2trajIDs

from tubeList import TubeList 
from singleTube import SingleTube

def main(doTubeFormat, inFileName, outTrajIDfileName, featPath, nrTrajThresh4Tube=0):

    tube2trajIDs.check()
    
    outPath = os.path.dirname(outTrajIDfileName)
    if not os.path.exists( outPath ):
        os.makedirs(outPath)

    # read trajectory positions
    print '\tGet trajectory positions;',
    geoFeat = denseTraj.getFeatFromFileByName(featPath, 'geo')

    
    # if proposals are stored as Tubes already, read them
    if doTubeFormat:
        tubeProposals = TubeList()
        tubeProposals.readHDF5(inFileName)        
        # initialize with a single name
        inHDF5fileClusts = ['tubes']
    else:
        print '\tGet video dimensions;', 
        vidInfo = denseTraj.getFeatFromFileByName(featPath, 'vidinfo')
        xmax = vidInfo[1]
        ymax = vidInfo[2]    
        # input cluster file
        inHDF5fileClusts = h5py.File( inFileName, 'r')
        
    # go over all features
    totNrProposals = 0
    for featName in inHDF5fileClusts:

        if not doTubeFormat:
            # get the clustered proposals for this feature type in SLINK pointer-representation
            dset = inHDF5fileClusts[featName]
            mergedTracks = dset[()]           
            # convert pointer-representation to tube proposals 
            if len(mergedTracks.shape) > 1 and mergedTracks.shape[0] > 1:
                tubeProposals = denseTraj.createProposals(mergedTracks, geoFeat, nrTrajThresh4Tube, xmax, ymax)

        nrProposals = len(tubeProposals)
        print '\tFeature: "%s", number of proposals: %d;' % (featName,nrProposals)
        
        # if ok                    
        if nrProposals > 0:
            # write as traj IDs

            if totNrProposals==0:
                outHDF5file = h5py.File( outTrajIDfileName, 'w', compression="gzip", compression_opts=9)
            
            for j in range(nrProposals):
                trajIDs = tubeProposals[j].tube2trajIDs(geoFeat)
                outHDF5file.create_dataset(str(totNrProposals), data=trajIDs)
                totNrProposals += 1
            
    print '\tWrite trajectory IDs to', outTrajIDfileName
    outHDF5file.close()

# if run as a command (ie: not imported)
if __name__ == "__main__":    
                  
    if len(sys.argv) != 4 and len(sys.argv) != 5:
        print 'nr args', len(sys.argv)
        raise ValueError('not correct nr of input arguments')

    inFileName = sys.argv[1]
    outTrajIDfileName = sys.argv[2]
    featPath = sys.argv[3]

    # if txt format
    if len(sys.argv) == 4:
        main(True, inFileName, outTrajIDfileName, featPath)
    else:    
        nrTrajThresh4Tube = int(sys.argv[4])
        main(False, inFileName, outTrajIDfileName, featPath, nrTrajThresh4Tube)

