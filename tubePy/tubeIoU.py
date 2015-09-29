import numpy as np
import sys

def check():
    print '\t** Warning: using slow "tubeIoU", consider compiling to cython with "compileTubeIoU.sh"'

def intersectionOverUnion(bb1, bb2):
    """
    Compute Intersection over Union for bounding boxes bb1 and bb2
    Assume a box is in the form: (xMin, yMin, xMax, yMax)   
    """
    
    # get boxes
    xMiBox1, yMiBox1, xMaBox1, yMaBox1 = bb1
    xMiBox2, yMiBox2, xMaBox2, yMaBox2 = bb2


    maxOfMinX = max( xMiBox1, xMiBox2)
    minOfMaxX = min( xMaBox1, xMaBox2)
    
    if minOfMaxX > maxOfMinX:
        xI = minOfMaxX - maxOfMinX
    else:
        return 0.0

    maxOfMinY = max( yMiBox1, yMiBox2)
    minOfMaxY = min( yMaBox1, yMaBox2)
    
    if minOfMaxY > maxOfMinY:
        yI = minOfMaxY - maxOfMinY
    else:
        return 0.0
        #yI = 0
        
    # get intersection
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
        
    IoU = float(intersectionBB) / float(unionBB)
    return IoU


def tubeIoU( gtFrames, tubeFrames, nrNonZeroFrames=0 ):
    """Compute tube overlap between 2 tubes"""
    
    IoU = 0.0
    nrFrames = gtFrames.shape[0]
    for i in xrange(nrFrames):
        bbIoU = intersectionOverUnion(gtFrames[i], tubeFrames[i])
        nrNonZeroFrames += 1.0
        IoU += bbIoU

    return IoU / nrNonZeroFrames



