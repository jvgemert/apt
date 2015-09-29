import numpy as np
import copy
import tubeIoU
import tube2trajIDs
import h5py

class SingleTube:
    '''Class for a single video tube'''
    
    def __init__(self, f=0, arr=[[]] ):
        # a single tube has a begin frame an end frame and an array of bounding boxes
        self._beginFrame = int(f)
        self._tube = np.array(arr, dtype='float32')
        self._endFrame = self._beginFrame + self._tube.shape[0]
        
    def __len__(self):
        return self._tube.shape[0]

    def __str__(self):
        s = ''
        for k in range(len(self)):
            val = self._tube[k,:]
            if not np.any(val == np.inf) and not np.any(val == -np.inf) and val.sum() > 0 :
                s += '%d %f %f %f %f\n' % (k+self._beginFrame, val[0], val[1], val[2], val[3])
        return s
                
    def copy(self):
        return SingleTube( self._beginFrame, copy.deepcopy(self._tube) )
            
    def getFrameOverlap(self, tube):
        '''Returns (overlap, idx) where
            overlap: how many frames overlap with tube, 
            idx: at which position (in self) the overlap starts
        '''
        
        # if self starts earlier
        if self._beginFrame < tube._beginFrame:
            # if no overlap
            if self._endFrame < tube._beginFrame:
                return 0, 0
            overlap = min(self._endFrame, tube._endFrame) - tube._beginFrame 
            idx = tube._beginFrame - self._beginFrame
            
        # if tube starts earlier or if both start equal
        else:
            
            # if no overlap
            if tube._endFrame < self._beginFrame:
                return 0, 0
            overlap = min(self._endFrame, tube._endFrame) - self._beginFrame 
            idx = 0
        return overlap, idx            

    # not tested, a bit buggy still? (is it faster?)
    def mergePerPart(self, tube):
        '''Merge another tube to self'''
        
        newSelf = self.copy()
        newSelf.mergeSimple(tube)
        
        
        newStart = min(self._beginFrame, tube._beginFrame)
        newEnd = max(self._endFrame, tube._endFrame)
        newLen = newEnd-newStart
        
        # create a new arry
        newArr = np.empty( (newLen, 4), dtype='float32')

        overlap1, selfIdx = self.getFrameOverlap(tube)
        overlap2, tubeIdx = tube.getFrameOverlap(self)
        #if overlap1 != overlap2:
        #    print 'should not happen'
        #    print self
        #   print tube
        #    raise

        overlapStart = 0
        overlapEnd = overlap1
        
        # copy any non-overlapping part at the front
        if self._beginFrame < tube._beginFrame:
            newArr[:selfIdx,:] = self._tube[:selfIdx,:]
            overlapStart = selfIdx
        if self._beginFrame > tube._beginFrame:
            newArr[:tubeIdx,:] = tube._tube[:tubeIdx,:]
            overlapStart = tubeIdx
            
        # copy any non-overlapping part at the end
        if self._endFrame > tube._endFrame:
            newArr[overlapStart+overlap1:min(overlapStart+len(self),newLen),:] = self._tube[selfIdx+overlap1:,:]
        if self._endFrame < tube._endFrame:
            newArr[overlapStart+overlap2:min(overlapStart+len(tube),newLen),:] = tube._tube[tubeIdx+overlap2:,:]
            
        overlapEnd = overlapStart+overlap2
        
        # now overlaping part
        # fill with INFs to represent empty frames
        newArr[overlapStart:overlapEnd,0:2].fill(np.inf)
        newArr[overlapStart:overlapEnd,2:4].fill(-np.inf)

        # merge
        np.minimum( self._tube[selfIdx:selfIdx+overlap1,0:2], tube._tube[tubeIdx:tubeIdx+overlap1,0:2], newArr[overlapStart:overlapEnd,0:2])
        np.maximum( self._tube[selfIdx:selfIdx+overlap1,2:4], tube._tube[tubeIdx:tubeIdx+overlap1,2:4], newArr[overlapStart:overlapEnd,2:4])
    
        if not np.all(newSelf._tube == newArr):
            print 'simple', newSelf._tube
            print 'merged', newArr
            raise
    
        self._beginFrame = newStart
        self._tube = newArr
        self._endFrame = newEnd
                
            
    def merge(self, tube):
        '''Merge another tube to self'''
        
        newStart = min(self._beginFrame, tube._beginFrame)
        newEnd = max(self._beginFrame+len(self), tube._beginFrame+len(tube))
        newLen = newEnd-newStart
        
        # create an arry for self
        newArr1 = np.empty( (newLen, 4), dtype='float32')
        
        # fill with INFs to represent empty frames
        newArr1[:,0:2].fill(np.inf)
        newArr1[:,2:4].fill(-np.inf)

        # create an arry for tube
        newArr2 = np.empty( (newLen, 4), dtype='float32')
        # fill with INFs to represent empty frames
        newArr2[:,0:2].fill(np.inf)
        newArr2[:,2:4].fill(-np.inf)

        # copy self into new arry        
        selfStart = self._beginFrame - newStart
        newArr1[selfStart:selfStart+len(self), :] = self._tube
        # copy tube into new arry        
        tubeStart = tube._beginFrame - newStart
        newArr2[tubeStart:tubeStart+len(tube), :] = tube._tube

        # merge
        np.minimum( newArr1[:,0:2], newArr2[:,0:2], newArr1[:,0:2])
        np.maximum( newArr1[:,2:4], newArr2[:,2:4], newArr1[:,2:4])
    
        self._beginFrame = newStart
        self._tube = newArr1
        self._endFrame = newEnd


    def IoU(self, tube):
        '''Compute Intersection over Union with another tube and self'''

        overlap1, selfIdx = self.getFrameOverlap(tube)
        overlap2, tubeIdx = tube.getFrameOverlap(self)

        zeroFramesSelf = len(self) - overlap1
        zeroFramesTube = len(tube) - overlap2
        
        iou = tubeIoU.tubeIoU(self._tube[selfIdx:selfIdx+overlap1,:], tube._tube[tubeIdx:tubeIdx+overlap1,:], zeroFramesSelf + zeroFramesTube)
        
        return iou

    def tube2trajIDs(self, geoFeat):
        return tube2trajIDs.tube2trajIDs(self._beginFrame, self._tube, geoFeat) 
        
    def write(self, fName):
        '''Write to TXT format'''
        fileOut = open(fName, 'w')
        fileOut.write(str(self))
        fileOut.close()

    def writeHDF5(self, outHDF5file, name):
        '''Write to open binary HDF5 file'''
        
        tube = np.empty( (len(self), 5), dtype=np.float32 )
        
        i = 0
        for k in range(len(self)):
            val = self._tube[k,:]
            if not np.any(val == np.inf) and not np.any(val == -np.inf) and val.sum() > 0 :
                tube[i,:] = np.array([k+self._beginFrame, val[0], val[1], val[2], val[3] ])
                i += 1
        tube = tube[:i,:]
        dset = outHDF5file.create_dataset(name, data=tube)
        
    def read(self, fName):
    
        bbList = []
        #print fName
        minFrameNr = -1
        fileIn = open(fName, 'r')

        lastFrameNr = -1
        for line in fileIn:
            if line.count(',') == 4:
                sep = ','
                lst = line.strip().split(sep)
            else:
                lst = line.strip().split()
            frameNr = float(lst[0])
            if minFrameNr == -1:
                minFrameNr = frameNr
            else:
                # pad with INF if there are missing frameNrs
                while lastFrameNr < frameNr-1:
                    bbList.append([np.inf, np.inf, -np.inf, -np.inf])
                    lastFrameNr += 1
            bb = [float(s) for s in lst[1:] ]
            bbList.append(bb)    
            lastFrameNr = frameNr    

        fileIn.close()                    

        self._beginFrame = minFrameNr
        self._tube = np.array(bbList, dtype='float32')
        self._endFrame = lastFrameNr + 1
        
    def readHDF5(self, inHDF5file, name):
        '''Read tube from open HDF5 file'''
        dset = inHDF5file[name]
        tube = dset[()]
        
        bbList = []
        #print fName
        minFrameNr = -1
        lastFrameNr = -1
        for i in range(tube.shape[0]):
            val = tube[i,:] 
            frameNr = int(val[0])
            if minFrameNr == -1:
                minFrameNr = frameNr
            else:
                # pad with INF if there are missing frameNrs
                while lastFrameNr < frameNr-1:
                    bbList.append([np.inf, np.inf, -np.inf, -np.inf])
                    lastFrameNr += 1
            bb = val[1:]
            bbList.append(bb)    
            lastFrameNr = frameNr    

        self._beginFrame = minFrameNr
        self._tube = np.array(bbList, dtype='float32')
        self._endFrame = lastFrameNr + 1
        
        
        
