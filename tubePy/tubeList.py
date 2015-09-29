import os, os.path, sys
import glob
import numpy as np
import h5py
from singleTube import SingleTube

class TubeList:
    '''Class for a collection of video tubes'''
    
    # attribute: _tubes = a list of tubes
    
    def __init__(self):
        # a tube collection consists of a list of SingeTube 
        self._tubes = []

    def __getitem__(self, key):
        return self._tubes[key]
       
    def __setitem__(self, key, item):
        self._tubes[key] = item
        
    def __len__(self):
        #print self._tubes
        return len(self._tubes)
        
    def append(self, item):
        self._tubes.append(item)

    def computeTubeOverlap(self, tubes):
        aboMat = np.zeros( (len(self), len(tubes)) )

        for i in xrange(len(self) ):
            if i % 1000 == 0:
                print i,
                sys.stdout.flush()
            for j in xrange(len(tubes)):
                aboMat[i,j] = self[i].IoU(tubes[j]) 
            #print

        return aboMat        
        

    def write(self, path, startID = 0, format='tubeID%06d.txt'):
        """
        Write tubes in TXT format to path/format % tubeID , where tubeID=tube index
        A tube is a frameNr mapped to a tupel of 4 numbers (xmin, ymin, xmax, ymax).
        startID gives a possible offset to the tubeID
        Returns the nr of written tubes
        """
        if not os.path.exists(path):    
            os.makedirs(path)

        i = format.find('%')
        j = format.find('d',i)
        if i <0 or j <0:
            raise ValueError('Cannot map tubeIDs, format does not have a "%d": ' + format)
                    
        for i in range(len(self)):
            #print i
            fName = os.path.join( path, format % (i+startID) )
            self._tubes[i].write(fName)

    def writeHDF5(self, outHDF5file, startID = 0):
        """
        Write tubes to an open HDF5 file
        A tube is a frameNr mapped to a tupel of 4 numbers (xmin, ymin, xmax, ymax).
        startID gives a possible offset to the tubeID
        Returns the nr of written tubes
        """
                    
        for i in range(len(self)):
            #print i
            self._tubes[i].writeHDF5(outHDF5file, str(i+startID) )



    def read(self, path):
        """
        Read tubes from path; 
        A tube is a tupel of 4 numbers (xmin, ymin, xmax, ymax).
        """
        
        if not os.path.exists(path):    
            raise Exception('Path does not exist: %s' % (path) )
            
        pp = os.path.join(path, '*.txt')
        #print pp
        files = glob.glob( pp )
        nrFiles = len(files) # nr Frames
        print '\treading tubes:', path, '; Number of tubes read:', nrFiles
        
        if nrFiles == 0:
            raise Exception('No files found in: %s' % (pp) )
        files.sort()
        #files.reverse()

        for i in xrange(nrFiles):

            f = files[i]
            tube = SingleTube()
            tube.read(f)
            self._tubes.append( tube )

    def readHDF5(self, inHDF5fileName):
        """
        Read tubes from hdf5 fileName; 
        A tube is a tupel of 4 numbers (xmin, ymin, xmax, ymax).
        """
        
        if not os.path.exists(inHDF5fileName):    
            print 'Path does not exist: %s' % (inHDF5fileName) 
            raise Exception('Path does not exist: %s' % (inHDF5fileName) )
            
        inHDF5file = h5py.File(inHDF5fileName, 'r')    
        nrTubes = len(inHDF5file) 
        print '\treading tubes:', inHDF5fileName, '; Number of tubes to read:', nrTubes
        
        if nrTubes == 0:
            raise Exception('No tubes found in: %s' % (pp) )

        for i in xrange(nrTubes):

            tube = SingleTube()
            tube.readHDF5(inHDF5file, str(i) )
            self._tubes.append( tube )

        inHDF5file.close()
            
    def readFrameFormat(self, path, readWHformat=False, spatialSubSampleRate=1):
        """
        Read tubes from path; dense format = a tube at each frame number
        A tube is a tupel of 4 numbers (xmin, ymin, xmax, ymax).
        if readWHformat == True:
            A tube is converted from (xmin, ymin, w, h) format.
        Every frame X should have a X.txt file with tubes.
        Every .txt file has a fixed nr of lines, each line is a tube; All .txt files have the same nr of tubes.
        If a tube is not visible in a frame XXX.txt, set the tube to (0,0,0,0)
        """
        
        if not os.path.exists(path):    
            raise Exception('Path does not exist: %s' % (path) )
            
        pp = os.path.join(path, '*.txt')
        #print pp
        files = glob.glob( pp )
        nrFiles = len(files) # nr Frames
        print 'readFrameFormat:', path, 'nrFiles', nrFiles,
        
        if nrFiles == 0:
            raise Exception('No files found in: %s' % (pp) )
        files.sort()
        #files.reverse()

        for i in xrange(nrFiles):

            f = files[i]
            #print f

            fileIn = open(f,'r')
            lines = fileIn.readlines()

            nrLines = len(lines) # nr proposals

            if i ==0:
                # if first element, reserve space
                data = np.zeros( (nrFiles, nrLines, 4), dtype='float32' )
                print 'nrTubes', nrLines
            else:
                # nr tubes cannot differ per file
                if nrLines != data.shape[1]:
                    raise Exception('NrLines in %s should be %d, but is %d' % (f, nrLines, data.shape[0]) )

            for j in range(nrLines):
                line = lines[j]
                d = line.split(',')
                if len(d) == 1:
                    d = line.split()
                data[i,j,:] = np.array([float(s)/spatialSubSampleRate for s in d[:4] ] )
                if readWHformat:
                    data[i,j,2] = data[i,j,2] + data[i,j,0]
                    data[i,j,3] = data[i,j,3] + data[i,j,1]

            fileIn.close()
            
        # convert data array to SingleTube objects
        nrTubes = data.shape[1]
        for t in range(nrTubes):

            # find frames without BBs: sum the BBs, empty are <= 0 
            minFrameNr = 0
            maxFrameNr = nrFiles-1
            
            summedBB = np.sum(data[:,t,:], axis=1)
            emptyIdx = np.nonzero(summedBB <=0)[0]
    
            # if pre-BB empty
            if summedBB[0] <0:
                minFrameNr = min(emptyIdx)
            # if post-BB empty
            if summedBB[-1] <0:
                maxFrameNr = max(emptyIdx)
            
            bbList = []
            for f in range(nrFiles):
                if f >= minFrameNr and f <= maxFrameNr:
                    bb = data[f,t,:]
                    bbList.append(bb)
            tube = SingleTube( minFrameNr, bbList )
            
            # add tube to list
            self._tubes.append( tube )        
        
        

