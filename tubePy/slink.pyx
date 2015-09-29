#cython: boundscheck=False
#cython: wraparound=False

import numpy as np
import bisect
import sys
from cpython cimport array
from array import array


cdef inline int int_max(int a, int b): return a if a >= b else b
cdef inline int int_min(int a, int b): return a if a <= b else b
cdef inline float float_max(float a, float b): return a if a >= b else b
cdef inline float float_min(float a, float b): return a if a <= b else b


# do it with SLINK

#cimport cython
#@cython.boundscheck(False) # turn of bounds-checking for entire function
def SSclustSlink(int [:, :] neighborGraph, float[:, :] neighborSims, int n):
    print '\tRun SLINK clustering in cython', 
    
    cdef int i, j, counter, insertPos, nrIds, origPi
    cdef int maxNrNN = neighborGraph.shape[1]
    cdef int[:] Pi = np.ndarray(n, dtype=np.int32)
    cdef float[:] Lambda = np.ndarray(n, dtype=np.float32)
    cdef float[:] M = np.ndarray(n, dtype=np.float32)
    #cdef float[:] simArr = np.ndarray(n, dtype=np.float32)
    #cdef int[:] idArr = np.ndarray(n, dtype=np.int32)
    cdef float INF = np.inf
    
    M = np.array( np.ones(n) * np.inf, dtype=np.float32)
    Lambda = np.array( np.ones(n) * np.inf, dtype=np.float32)
    Pi = np.array( np.ones(n) * np.inf, dtype=np.int32)
    
    #idArr = np.array( np.ones(n) * np.inf, dtype=np.int32)      
    #simArr = np.array( np.ones(n) * np.inf, dtype=np.float32)
    
    Pi[0] = 0
    Lambda[0] = INF
    for i in range(1, n):

        Pi[i] = i
        Lambda[i] = INF

        nrIds = 0
        for j in range(maxNrNN):
            if neighborGraph[i,j] < 0:
                break
            nrIds += 1

        ids = array('i', neighborGraph[i,0:nrIds] )
        
        # M[ ids ] = nnSims[0:len(ids)]
        for j in range(nrIds):
            M[ neighborGraph[i,j] ] = neighborSims[i,j]
        
        counter = 0
        #for j in range(i):
        while counter < nrIds:
            j = ids[counter]
            origPi = Pi[j]
            if Lambda[j] >= M[j]:
                M[Pi[j]] = float_min(M[Pi[j]], Lambda[j])
                Lambda[j] = M[j]
                Pi[j] = i
            else:            
                M[Pi[j]] = float_min(M[Pi[j]], M[j])
            
            # if origPi is not in ids, add it
            insertPos = bisect.bisect_left( ids, origPi )
            if insertPos == nrIds or ids[insertPos] != origPi:
                ids.insert(insertPos,origPi)
                nrIds += 1

            # reset M val to inf    
            M[j] = INF
            counter += 1
        
        #Pi[ Lambda[:i] >= Lambda[Pi][:i] ] = i
        for j in range(i): # ids
            if Lambda[j] >= Lambda[Pi[j]]:
                Pi[j] = i
        
        M[i] = INF
        
        # output some statistics every K interations
        if i % 1000 == 0:
            print '%d:' % (i/1000 ), 
            sys.stdout.flush()
    #print
    
    return Lambda, Pi
    #mergedTracks = convertPointerRepresentation(Lambda, Pi, n)

    #return mergedTracks
    
    
    
    
