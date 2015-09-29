import numpy as np
import scipy.spatial
import sys
import bisect
from array import array



def uniqueKey(t1, t2):
    # make a unique key for this pair
    mi = min(t1, t2)
    ma = max(t1, t2)
    trackPair = (mi,ma)
    return trackPair


def getTrackNeighborsYaelYnumpy(feats, k):
    from yael import ynumpy, yael

    nrTracks = feats.shape[0]
    print '\tFinding %d nearest neighbors, for %d trajectories' % (k,nrTracks), 
    sys.stdout.flush()
   
    (simMatIDs, simMat) = ynumpy.knn(feats, feats, nnn=k+1, distance_type=12, nt=1)
    
    print '.'
    
    return simMatIDs[:,1:], simMat[:,1:]
    
    
def convertPointerRepresentation(Lambda, Pi, n):
    
    # output, newID, ID1, ID2
    mergedIDs = np.zeros( (n, 4), dtype='float32' )

    # reference for building the clusters
    clustRef = range( Pi.shape[0]*2)

    srtIds = Lambda.argsort()
     
    counter = 0
    while counter < n-1:
    
        newID = counter + n
        
        i = srtIds[counter]
        l = Lambda[i]
        p = Pi[i]
                        
        #print newID, counter, l, i,p, clustRef[i], clustRef[p]
        iID = clustRef[i]
        pID = clustRef[p]
            
        mergedIDs[counter] = [newID, min(iID,pID), max(iID,pID), l]
        
        clustRef[i] = newID        
        clustRef[p] = newID        

        counter += 1        
    
    return mergedIDs


# create neighborhood matrix from kNN matrix
def getNeighborGraph(simMatIDs, n):

    
    nrNN = simMatIDs.shape[1]
    print '\tCreating the neighborhood graph for k=%d;' % nrNN,
    sys.stdout.flush()

    # for each track, keep a dict for which tracks are neighbors

    maxNrNN = 0
    
    id2IdsArr = {}

    # for each track, and its neigbors
    for i in xrange(n):
        for j in xrange(nrNN):

            # IDs of the track pair
            t1 = i
            t2 = simMatIDs[i,j]
            
            # t1 equal t2 is possible, if exact copies exists (should not be the case though)
            if t1 != t2:

                # to remember which tracks are neighbors
                if t1 not in id2IdsArr:
                    id2IdsArr[t1] = array('I',[])
                if t2 not in id2IdsArr:
                    id2IdsArr[t2] = array('I',[])
                 
                miT = min(t1,t2)
                maT = max(t1,t2)
                
                maTids = id2IdsArr[maT]
                
                # if not in ids, add it; and keep sorted
                insertPos = bisect.bisect_left( maTids, miT )
                if insertPos == len(maTids) or maTids[insertPos] != miT:
                    maTids.insert(insertPos,miT)
                    if maxNrNN < len(maTids):
                        maxNrNN = len(maTids)
                    
    print 'the maximum number of neighbors is', maxNrNN,
    # now convert to numpy array of lower triangle of a NxN neighborhood 
    # all non used IDs are INF (maybe use sparse matrix?)
    neighborGraph = np.empty( (n,maxNrNN), dtype=np.int32 )
    neighborGraph.fill(np.inf)
    for i in xrange(n):
        arr = id2IdsArr[i]
        nrNN = len(arr)
        neighborGraph[i, 0:nrNN] = arr

    print '.'
    return neighborGraph

def getNeighborSimilarities(neighborGraph, feat, simFunct):

    print '\tComputing feature similarities for all neighboring trajectory pairs',
    sys.stdout.flush()
    
    n, maxNrNN = neighborGraph.shape
    neighborSims = np.empty( (n,maxNrNN), dtype=np.float32 )
    neighborSims.fill(np.nan)
    
    intInf = np.empty( 1, dtype=np.int32 )
    intInf.fill(np.inf)
    
    # for each track, and its neigbors
    for i in xrange(n):
        nnIDs = neighborGraph[i, :] 
        for counter in xrange(maxNrNN):
            j = nnIDs[counter]
            if j == intInf:
                break

            simScore = simFunct(feat[i,:], feat[j, :])
            neighborSims[i,counter] = simScore

    print '.'
    return neighborSims
    
    
def normalizeNeighborSimilarities(neighborSims):

    simMean = np.nanmean( neighborSims )
    simVar = np.nanvar(neighborSims)
    #print 'simMean', simMean, 'simVar', simVar
    return np.array( (neighborSims - simMean ) / simVar, dtype=np.float32)

def normalizeNeighborSimilaritiesMiMa(neighborSims):

    simMi = np.nanmin( neighborSims)
    simMa = np.nanmax(neighborSims)
    
    #print 'simMi', simMi, 'simMa', simMa

    return np.array( (neighborSims - simMi ) / (simMa - simMi), dtype=np.float32)
        
