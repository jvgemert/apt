#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

import numpy as np

def check():
    pass
    
def tube2trajIDs( int tubeBeginFrame, float [:,:] tube, float [:,:] featSpat, int framesPerTrack=15 ):

    """
    get trajectory IDS that belong to the tube
    Trajectories are: [framenrEnd, x1,y1, x2, y2, ..]
    Tube has a beginFrame, and tube is an array of: [xmin, ymin, xmax, ymax]
    """
    cdef int f, t, j, nrTraj, nrFrames
    cdef int keep
    cdef float [:,:] tubeFeatSpat

    # get the spatial trajectory features (without the framenr)
    tubeFeatSpat = featSpat[:,1:]
    
    # nr of trajectories
    nrTraj = featSpat.shape[0]
    
    # which trajectories to keep
    trajToKeep = np.zeros( nrTraj, dtype='bool')
    
    # nr of frames
    nrFrames = tube.shape[0]
    
    # go over the tube frames
    for f in range(1+nrFrames-framesPerTrack):
        if tube[f,0] == 0 and tube[f,1] == 0 and tube[f,2] == 0 and tube[f,3] == 0:
            continue
        for t in range(nrTraj):
            # check frame nr
            if featSpat[t,0] != (f + tubeBeginFrame + framesPerTrack):
                continue

            # xmin
            keep = 1
            for j in range(framesPerTrack):
                if tubeFeatSpat[t,j*2] <= tube[f+j,0]:
                    keep = 0
                    break
            if keep == 0:
                continue

            # ymin
            keep = 1
            for j in range(framesPerTrack):
                if tubeFeatSpat[t,j*2+1] <= tube[f+j,1]:
                    keep = 0
                    break
            if keep == 0:
                continue

            # xmax
            keep = 1
            for j in range(framesPerTrack):
                if tubeFeatSpat[t,j*2] >= tube[f+j,2]:
                    keep = 0
                    break
            if keep == 0:
                continue

            # ymax
            keep = 1
            for j in range(framesPerTrack):
                if tubeFeatSpat[t,j*2+1] >= tube[f+j,3]:
                    keep = 0
                    break
            if keep == 0:
                continue

            trajToKeep[t] = True

    return np.nonzero( trajToKeep )[0]

            

