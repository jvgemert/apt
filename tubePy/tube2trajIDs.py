import numpy as np
import os, os.path
import sys

def check():
    print '\t** Warning: using (very) slow "tube2trajIDs", consider compiling to cython with "compileTube2trajIDs.sh"'

def tube2trajIDs( tubeBeginFrame, tube, featSpat, framesPerTrack=15 ):
    """
    get trajectory IDS that belong to the tube
    Trajectories are: [framenrEnd, x1,y1, x2, y2, ..]
    Tube has a beginFrame, and tube is an array of: [xmin, ymin, xmax, ymax]
    """
    
    # get the spatial trajectory features (without the framenr)
    tubeFeatSpat = featSpat[:,1:]
    
    # nr of trajectories
    nrTraj = featSpat.shape[0]
    
    # which trajectories to keep
    trajToKeep = np.zeros( nrTraj, dtype='bool')

    # go over the tube frames
    for f in range(1+tube.shape[0]-framesPerTrack):
        
        if np.sum( tube[f,:] ) == 0:
            continue
        for t in range(nrTraj):

            # check frame nr OK?
            if featSpat[t,0] != (f + tubeBeginFrame + framesPerTrack):
                continue

            # xmin OK?
            keep = 1
            for j in range(framesPerTrack):
                if tubeFeatSpat[t,j*2] <= tube[f+j,0]:
                    keep = 0
                    break
            if keep == 0:
                continue

            # ymin OK?
            keep = 1
            for j in range(framesPerTrack):
                if tubeFeatSpat[t,j*2+1] <= tube[f+j,1]:
                    keep = 0
                    break
            if keep == 0:
                continue

            # xmax OK?
            keep = 1
            for j in range(framesPerTrack):
                if tubeFeatSpat[t,j*2] >= tube[f+j,2]:
                    keep = 0
                    break
            if keep == 0:
                continue

            # ymax OK?
            keep = 1
            for j in range(framesPerTrack):
                if tubeFeatSpat[t,j*2+1] >= tube[f+j,3]:
                    keep = 0
                    break
            if keep == 0:
                continue

            # if all OK, keep the trajectory
            trajToKeep[t] = True

    return np.nonzero( trajToKeep )[0]


            

