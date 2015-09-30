import os, os.path, sys
import gzip
#from yael import ynumpy
import numpy as np
import h5py


"""
Convert improved trajectories to hdf5 format, group per feature type

Format of improved trajectories:

1st line: video size, length: 55, width: 720, height: 404

remaining lines:
(taken from http://lear.inrialpes.fr/people/wang/dense_trajectories )

The features are computed one by one, and each one in a single line, with the following format:

frameNum mean_x mean_y var_x var_y length scale x_pos y_pos t_pos Trajectory HOG HOF MBHx MBHy

The first 10 elements are information about the trajectory:

frameNum:     The trajectory ends on which frame
mean_x:       The mean value of the x coordinates of the trajectory
mean_y:       The mean value of the y coordinates of the trajectory
var_x:        The variance of the x coordinates of the trajectory
var_y:        The variance of the y coordinates of the trajectory
length:       The length of the trajectory
scale:        The trajectory is computed on which scale
x_pos:        The normalized x position w.r.t. the video (0~0.999), for spatio-temporal pyramid 
y_pos:        The normalized y position w.r.t. the video (0~0.999), for spatio-temporal pyramid 
t_pos:        The normalized t position w.r.t. the video (0~0.999), for spatio-temporal pyramid

Then 30 elements, 15 * [x,y] for the trajectory shape

The following element are five descriptors concatenated one by one:

Trajectory:    2x[trajectory length] (default 30 dimension) 
HOG:           8x[spatial cells]x[spatial cells]x[temporal cells] (default 96 dimension)
HOF:           9x[spatial cells]x[spatial cells]x[temporal cells] (default 108 dimension)
MBHx:          8x[spatial cells]x[spatial cells]x[temporal cells] (default 96 dimension)
MBHy:          8x[spatial cells]x[spatial cells]x[temporal cells] (default 96 dimension)

Structure:

0:10 traj info
10:40 trajectory shape
40:70 trajectory descriptor
70:166 HOG descriptor
166:274 HOF descriptor
274:370 MBHx
370:466 MBHx
"""

def getPartOfLine(line, pre, post):
    i = line.find(pre) + len(pre) 
    j = line.find(post, i)
    return line[i:j].strip()

def getLWH(line, outHDF5file):

    #video size, length: 55, width: 720, height: 404

    print '\tInformation of', line.strip(),
    L = getPartOfLine(line, 'length: ', ',')
    W = getPartOfLine(line, 'width: ', ',')
    H = getPartOfLine(line, 'height: ', ',')
    
    lwh = np.array( [L,W,H], dtype='float32' )
    print '; Write', L, W, H, 'to: "vidinfo"'
    dset = outHDF5file.create_dataset('vidinfo', data=lwh)
    #ynumpy.fvecs_write(fName, np.array([[ float(L), float(W), float(H)]], dtype='float32'))

def writeFeat(featGzipFname, idx, nrFeat, fName, outHDF5fileName):
    # open zip file    
    f = gzip.open(featGzipFname, 'rb')
    # first line is video lenght/width/height
    line = f.readline()
    #print line
    featArr = np.empty( (nrFeat, len(idx)), dtype='float32')
    count = 0
    for line in f:
        lst = line.split()
        featList = [lst[i] for i in idx]
        featArr[count,:] = np.array(featList, dtype='float32')
        count += 1
    #featArr = np.array(featList, dtype='float32')
    f.close()
    
    #featName = fName[fName.rfind('.')+1:]
    
    print '\tFeature: %s, (nrTraj x dim) = ' % (fName), featArr.shape, '; Write to "%s"' % fName
    
    #print featArr
    
    outHDF5file = h5py.File( outHDF5fileName, 'a')
    dset = outHDF5file.create_dataset(fName, data=featArr)
    outHDF5file.close()
    #ynumpy.fvecs_write(fName, featArr)

def main(featGzipFname, outPath):

    if not os.path.exists(featGzipFname):
        raise ValueError('File %s does not exist.' % featGzipFname)

    if not os.path.exists( os.path.dirname(outPath)):
        os.makedirs(os.path.dirname(outPath))
        
    # open zip file    
    f = gzip.open(featGzipFname, 'rb')
    
    # first line is video lenght/width/height
    line = f.readline()
    if line.find('video size,') != 0:
        raise ValueError('File does not seem to be in correct format: %s' % featGzipFname)

    print 'writing to', outPath
    outHDF5file = h5py.File( outPath, 'w')
    getLWH(line, outHDF5file)
    outHDF5file.close()

    nrFeat = 0
    for line in f:
        nrFeat += 1
        if nrFeat % 10000 == 0:
            print int(nrFeat/10000),
            sys.stdout.flush()

    f.close()

    print 'nrFeat', nrFeat
    
    # for the sake of memory, process each feature separately

    """
    0:10 traj info
    10:40 trajectory shape
    
    40:70 trajectory descriptor
    70:166 HOG descriptor
    166:274 HOF descriptor
    274:370 MBHx
    370:466 MBHx
    """    
    # trajectory positions
    fName = 'trajecShape'
    b = 0
    nr = 40
    e = b + nr
    writeFeat(featGzipFname, range(b,e), nrFeat, fName, outPath)
    
    b = e
    nr = 60
    e = b + nr
    fName = 'trajecTubes'
    writeFeat(featGzipFname, range(b,e), nrFeat, fName, outPath)

    b = e
    nr = 30
    e = b + nr    
    fName = 'trajstab'
    writeFeat(featGzipFname, range(b,e), nrFeat, fName, outPath)
    
    b = e
    nr = 96
    e = b + nr   
    fName = 'hogstab'
    writeFeat(featGzipFname, range(b,e), nrFeat, fName, outPath)

    b = e
    nr = 108
    e = b + nr       
    fName = 'hofstab'
    writeFeat(featGzipFname, range(b,e), nrFeat, fName, outPath)

    b = e
    nr = 192
    e = b + nr       
    fName = 'mbhstab'
    writeFeat(featGzipFname, range(274,466), nrFeat, fName, outPath)


# if run as a command (ie: not imported)
if __name__ == "__main__":    
    if len(sys.argv) < 3:
        raise ValueError('not enough input arguments')

    featGzipFname = sys.argv[1]
    outPath = sys.argv[2]

    main(featGzipFname, outPath)
