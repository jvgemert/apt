import numpy as np
import bisect
import sys

print '\t** Warning: using slow SLINK clustering, consider compiling to cython with "compileSlink.sh"'

# do it with SLINK
def SSclustSlink(neighborGraph, neighborSims, n):
    print '\tRun SLINK clustering (slower: not in cython)', 
    
    Lambda = np.ones(n, dtype=np.double) * np.inf   
    Pi = np.array( np.ones(n, dtype='uint32') * np.inf, dtype='uint32')   
    M = np.ones(n, dtype=np.double) * np.inf   

    Pi[0] = 0
    Lambda[0] = np.inf
    
    for i in range(1, n):

        Pi[i] = i
        Lambda[i] = np.inf

        simArr = neighborSims[i,:]
        idArr = neighborGraph[i,:]
        
        ids = idArr[idArr>-1].tolist()

        M[ ids ] = simArr[0:len(ids)]
        
        counter = 0
        #for j in range(i):
        while counter < len(ids):
            j = ids[counter]
            origPi = Pi[j]
            if Lambda[j] >= M[j]:
                M[Pi[j]] = min(M[Pi[j]], Lambda[j])
                Lambda[j] = M[j]
                Pi[j] = i
            else:            
                M[Pi[j]] = min(M[Pi[j]], M[j])
            
            # if origPi is not in ids, add it
            insertPos = bisect.bisect_left( ids, origPi )
            if insertPos == len(ids) or ids[insertPos] != origPi:
                ids.insert(insertPos,origPi)
                
            # reset M val    
            M[j] = np.inf    
            counter += 1
        if M[i] < np.inf:
            print M[i]
        M[i] = np.inf

        Pi[ Lambda[:i] >= Lambda[Pi][:i] ] = i
        # output some statistics every K interations
        if i % 1000 == 0:
            print '%d:' % (i/1000 ), 
            sys.stdout.flush()
    
    return Lambda, Pi
    #mergedTracks = convertPointerRepresentation(Lambda, Pi, n)

    #return mergedTracks
    
