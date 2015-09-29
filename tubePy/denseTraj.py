import numpy as np
import os, os.path
import sys
import shutil
from yael import ynumpy
import h5py

from tubeList import TubeList 
from singleTube import SingleTube

"""
Tools for dealing with dense trajectories:
- read dense trajectories and features from file
- convert trajectories to tube
- create proposals from trajectory clusters
"""

def readFeatFile(fName, featname):   
    """read a hdf5 format file """
    print '\tReading feature file: %s, "%s"' % (fName, featname), 
    sys.stdout.flush()
    inHDF5file = h5py.File( fName, 'r')

    dset = inHDF5file[featname]
    feats = dset[()]
    print 'size', feats.shape
    inHDF5file.close()
    return feats 

def readFeatFileYael(fName):   
    """read a fvec yael format file """
    print '\tReading feature file:', fName, 
    sys.stdout.flush()
    feats = ynumpy.fvecs_read(fName)
    print 'size', feats.shape
    return feats 
        

def getFeatFromFileByName(fName, featName, tempScale=1.0):
    """read the approproate feature featName from file"""
    #print fName, featName
    if featName == 'geo':
        # raw spatial positions of trajectories   
        feats = readFeatFile(fName, 'trajecShape')
        return np.concatenate( (feats[:,0:1], feats[:,10:42]), axis=1 )    
    elif featName == 'spat':
        # temporaly weighted spatial positions of trajectories   
        feats = readFeatFile(fName, 'trajecShape')
        return np.concatenate( (tempScale*feats[:,0:1], feats[:,10:42]), axis=1 )
    #elif featName == 'vidinfo':
    #    feats = readFeatFile(fName, 'vidinfo')
    #    print feats
    #    sys.exit()
    #    return np.array([np.inf, np.inf, np.inf], dtype='float32')
    else:
        # other features
        feats = readFeatFile(fName, featName)

    if featName == 'mbhstab':
        # if MBH feature, L2 normalize       
        feats = (feats.T / np.linalg.norm(feats,ord=2, axis=1)).T

    return feats
    
    
def traj2tube(frameNumEnd, tubeFeatSpat, xmax=np.inf, ymax=np.inf, regionSize=15, framesPerTrack=15):
    """convert a trajectory to a SingleTube proposal"""
    frameNumStart = int(frameNumEnd - framesPerTrack)

    # make a tube as a tupel of 4 numbers (xmin, ymin, xmax, ymax).
    tube = np.zeros( (framesPerTrack, 4), dtype='float32' )
    
    # a trajectory has x,y in the center, with a size of 2*regionSize
    i = np.arange(framesPerTrack)
    tube[i,0] = np.maximum(0,tubeFeatSpat[i*2] - regionSize) # xmin
    tube[i,1] = np.maximum(0,tubeFeatSpat[i*2+1] - regionSize) # ymin
    tube[i,2] = np.minimum(xmax,tubeFeatSpat[i*2] + regionSize) # xmax
    tube[i,3] = np.minimum(ymax,tubeFeatSpat[i*2+1] + regionSize) # ymax    
    
    return SingleTube(frameNumStart,tube)

    
def createProposals(mergedTracks, featSpat, cutOffLevel, xmax=np.inf, ymax=np.inf, regionSize=15):
    """create SingleTube proposals from the 'mergedTracks' clusters in trajectory clusters format"""
    
    # how many proposals
    nrProposals = mergedTracks.shape[0]
    # how many trajectory tracks
    nrTracks = featSpat.shape[0]

    zeroFound = True
    while zeroFound:
        # the list of tubes that will be created
        tubeLst = TubeList()
        # the list of tubes that will be sub-sampled
        selectedTubes = TubeList()
        
        # keep track of the nr of trajectories per merge
        nrTraj = np.zeros(nrProposals)
        nrTrajT1 = np.zeros(nrProposals)
        nrTrajT2 = np.zeros(nrProposals)
        
        for p in xrange(nrProposals):
                # clusterformat: a merged ID, and trackIDs t1 and t2
                [mergedID, t1, t2] = mergedTracks[p][0:3]
                
                if t1 < nrTracks:
                    # if a trackID is lower than nrTracks it is a trajectory
                    tube1 = traj2tube(featSpat[t1,0], featSpat[t1,1:], xmax, ymax, regionSize)
                    nrT1 = 1

                else:
                    # otherwise it is a previously merged proposal
                    idx = int(t1) - nrTracks
                    tube1 = tubeLst[idx]
                    nrT1 = nrTraj[idx]
            
                if t2 < nrTracks:
                    # if a trackID is lower than nrTracks it is a trajectory
                    tube2 = traj2tube(featSpat[t2,0], featSpat[t2,1:], xmax, ymax, regionSize)
                    nrT2 = 1
                else:
                    # otherwise it is a previously merged proposal
                    idx = int(t2) - nrTracks
                    tube2 = tubeLst[idx]
                    nrT2 = nrTraj[idx]

                # the nr of trajectories of this merge
                nrTraj[p] = nrT1 + nrT2
                nrTrajT1[p] = nrT1 
                nrTrajT2[p] = nrT2 

                # make a copy of t1 and merge it with t2
                newTube = tube1.copy()
                newTube.merge(tube2)
                tubeLst.append(newTube)
                                        
                # if to subsample, add to the selected list
                if nrT1 >= cutOffLevel and nrT2 >= cutOffLevel:
                    selectedTubes.append(newTube)
        if len(selectedTubes) == 0:
            cutOffLevel = cutOffLevel/2
            if cutOffLevel <= 0:
                return selectedTubes
        else:
            return selectedTubes 
             

