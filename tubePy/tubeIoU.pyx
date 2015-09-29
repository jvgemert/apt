#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True

import sys
import numpy as np

cdef inline int int_max(int a, int b): return a if a >= b else b
cdef inline int int_min(int a, int b): return a if a <= b else b
cdef inline float float_max(float a, float b): return a if a >= b else b
cdef inline float float_min(float a, float b): return a if a <= b else b

def check():
    pass

cdef float intersectionOverUnion(float [:] bb1, float [:] bb2):
    """
    Compute Intersection over Union for bounding boxes bb1 and bb2
    Assume a box is in the form: (xMin, yMin, xMax, yMax)   
    """

    cdef float xMiBox1, yMiBox1, xMaBox1, yMaBox1
    cdef float xMiBox2, yMiBox2, xMaBox2, yMaBox2
    cdef float maxOfMinX, minOfMaxX, xI
    cdef float maxOfMinY, minOfMaxY, yI
    cdef float intersectionBB, unionBB
    cdef float wBox1, wBox2, hBox1, hBox2

    # get boxes
    xMiBox1 = bb1[0]
    yMiBox1 = bb1[1]
    xMaBox1 = bb1[2]
    yMaBox1 = bb1[3]
   
    xMiBox2 = bb2[0]
    yMiBox2 = bb2[1]
    xMaBox2 = bb2[2]
    yMaBox2 = bb2[3]
    
    maxOfMinX = float_max( xMiBox1, xMiBox2)
    minOfMaxX = float_min( xMaBox1, xMaBox2)
    
    if minOfMaxX > maxOfMinX:
        xI = minOfMaxX - maxOfMinX
    else:
        return 0.0
        #xI = 0.0
    
    maxOfMinY = float_max( yMiBox1, yMiBox2)
    minOfMaxY = float_min( yMaBox1, yMaBox2)
    
    if minOfMaxY > maxOfMinY:
        yI = minOfMaxY - maxOfMinY
    else:
        return 0.0
        #yI = 0
    
    intersectionBB = xI*yI
    
    # get union
    wBox1 = xMaBox1 - xMiBox1
    wBox2 = xMaBox2 - xMiBox2
    hBox1 = yMaBox1 - yMiBox1
    hBox2 = yMaBox2 - yMiBox2
    unionBB = (wBox1 * hBox1) + (wBox2 * hBox2) - intersectionBB

    # get Intersection over Union (IoU)
    if unionBB == 0:
        return 0
        
    return intersectionBB / unionBB


def tubeIoU( float [:,:] gtFrames, float [:,:] tubeFrames, float nrNonZeroFrames=0 ):
    """Compute tube overlap between 2 tubes"""
    
    cdef float IoU = 0.0
    cdef int nrFrames = gtFrames.shape[0]
    cdef float bbIoU
    
    for i in range(nrFrames):
        bbIoU = intersectionOverUnion(gtFrames[i], tubeFrames[i])
        nrNonZeroFrames += 1.0
        IoU += bbIoU

    return IoU / nrNonZeroFrames

