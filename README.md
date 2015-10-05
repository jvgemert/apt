# APT: Action localization Proposals from dense Trajectories

Python source code written by [Jan van Gemert](http://jvgemert.github.io), if you find any bugs or improvements, feel free to let me know. 
If you find the code useful, please cite our paper: [APT: Action localization Proposals from dense Trajectories](http://jvgemert.github.io/pub/gemertBMVC15APTactionProposals.pdf).

Note that this code may not run directly out of the box.
This is because the third party libraries need to be installed, and they may vary depending on your system. 
For convenience we include all third party code here, although all credit for them is with the original authors, and we highly recommend them.

### Requirements:

 - python 2.7
 - numpy
 - h5py (hdf5 data format)
 - cython
 - yael ( best: https://gforge.inria.fr/projects/yael/ or see `third/yael_v438.tar.gz`; Configure yael with `./configure.sh --enable-numpy`. And you may have to add the yael install directory to the `PYTHONPATH`.)
 - Improved Trajectory code (http://lear.inrialpes.fr/people/wang/improved_trajectories or see folder `third/`. Note that `DenseTrackStab.cpp` is adapted to export the trajectory `x` and `y` coordinates per frame, and the video statistics (width, height, lenght) are exported. See the folder `third/` for the modified version of `DenseTrackStab.cpp`. And, see `tubePy/extractDT.sh` for an example script on how to extract them.

### Cython:
The APT package contains Python code with some parts in cython. The code also works without cython, albeit slower (slower parts are: clustering, merging, and IoU computations). To take advantage of the cython speedup you have to compile the `tubePy/*.pyx` files (see the `compile2cython.sh` script that calls the individual `tubePy/compile*.sh` scripts). 

### Organization

This package is organized as follows.

    example/            # example video and groundtruth tube
    third/              # third party libs 
    tubePy/             # APT python code
    doExample.sh        # script that will run the example
    compile2cython.sh   # script to compile python functions to cython
    README.md           # this file

The APT package is developed under linux mint.
The third party libs needs to be installed. The third party software is in:

    third/
        DenseTrackStab                  # pre-compiled linux mint 17 64bit executable for improved trajectories
        improved_trajectory_APT         # Slightly modified source code for improved trajectories
        yael_v438.tar.gz                # source code for yael

All credit for third party sofware is with the authors.
It is best to rely on the original source code which is taken from:
 [yael](https://gforge.inria.fr/projects/yael/) and [Improved Trajectory code](http://lear.inrialpes.fr/people/wang/improved_trajectories).

### doExample.sh

The 'doExample.sh' file has all steps explained to compute APT for the included example, the steps it does are:

    1- extract the dense trajectories from the video and put in the expected format --> feat/
    2- create Action Proposals from dense Trajectories by clustering --> clusts/
    3- convenience function to convert proposals clusters of step 2 to tubes --> tubes/
    4- compare proposal clusters/tubes to groundTruth, outputs IoU overlap scores in --> IoU/
    5- convert proposal clusters/tubes to (0-based) trajectory IDs, so that the trajectories in a proposal can be mapped to Vlad/Fisher-vector/BoW --> trajIDs/ 

all steps in this package can be done on the internal cluster format (which will be converted to tubes internally each time), or, they can be done on explicitly exported tube proposals.
The reason for providing a 'detour' to tube files, is the ability to use tubes in other software.
The example includes all steps for the internal cluster format, and also for tube files.

For more details, read `doExample.sh`.

### Input and output

The included example consists of sub folders. The minimum input requirements are:

    example/
        gt/             # Tube ground truth (needed for evaluating proposal quality)
        vid/            # Input video

The output is computed with this package, which results in the following folder structure:

    example/
        feat/           # dense trajectory features 
        IoU/            # Intersection over Union scores with ground truth for proposals 
        IoU-tubes/      # Intersection over Union scores with ground truth for proposals in tube format
        clusts/         # Cluster results
        trajIDs/        # The trajectory IDs that belong to proposal tubes
        trajIDs-tubes/  # The trajectory IDs that belong to proposal tubes in tube format
        tube/           # Tube proposals


To start, it is best to read and run the 'doExample.sh' file, it has all steps required to compute APT for an included example video: `/example/vid/001.avi`.

---

# Frequently Asked Questions


### - Did the UCF101 scores change?

Yes. We made a mistake in the ground truth. We corrected our ground truth and make it [available](http://isis-data.science.uva.nl/jvgemert/apt/ucf101GT.tar.gz). We updated the scores in the [paper](http://jvgemert.github.io/pub/gemertBMVC15APTactionProposals.pdf), the numbers are different but the conclusions do not change. 


### - Do you have pre-computed tubes available?

Yes.
##### UCF-Sports (trimmed)
150 sports videos in 10 classes, available from http://crcv.ucf.edu/data/UCF_Sports_Action.php

- [ucfSportsAptTube.tar.gz](http://isis-data.science.uva.nl/jvgemert/apt/ucfSportsAptTube.tar.gz) : 
The tube proposals
- [ucfSportsGT.tar.gz](http://isis-data.science.uva.nl/jvgemert/apt/ucfSportsGT.tar.gz) : the ground truth tubes

##### UCF-101 (trimmed)
3,207 youtube videos for action detection of 24 classes, available from http://crcv.ucf.edu/data/UCF101.php

- [ucf101AptTube.tar.gz](http://isis-data.science.uva.nl/jvgemert/apt/ucf101AptTube.tar.gz) : 
The tube proposals
- [ucf101GT.tar.gz](http://isis-data.science.uva.nl/jvgemert/apt/ucf101GT.tar.gz) : the ground truth tubes


##### MSR Action Dataset II (untrimmed)
54 videos of 3 classes, available from http://research.microsoft.com/en-us/um/people/zliu/actionrecorsrc/

- [MSRIIAptTube.tar.gz](http://isis-data.science.uva.nl/jvgemert/apt/MSRIIAptTube.tar.gz) : 
The tube proposals
- [MSRIIGT.tar.gz](http://isis-data.science.uva.nl/jvgemert/apt/MSRIIGT.tar.gz) : the ground truth tubes


### - What is the tube dataformat?
A tube is a set of frameNRs and  boundingBoxes.

Specifically, a tube is represented as an array of 5 numbers: [frameNr, minX, minY, maxX, maxY].


### - How do I read a tube from disk?

The tubes are stored in [hdf5](https://www.hdfgroup.org/HDF5/) a platform-independent binary dataformat.

Examples on how to read tubes:

##### Matlab:
```
>> hinfo = hdf5info('example/tube/001/nn10T50.hdf5')
>> nrTubes = numel(hinfo.GroupHierarchy.Datasets)
>> tube1 = hdf5read(hinfo.GroupHierarchy.Datasets(1))
>> tube2 = hdf5read(hinfo.GroupHierarchy.Datasets(2))
```

##### Python, using the provide TubeList class:
```
>>> import h5py
>>> from tubePy.tubeList import TubeList
>>> tubes = TubeList()
>>> tubes.readHDF5('example/tube/001/nn10T50.hdf5')
	reading tubes: example/tube/001/nn10T50.hdf5 ; Number of tubes to read: 2147
>>> tube1 = tubes[0]
>>> print tube1
>>> tube2 = tubes[1]
```

##### Python, without the TubeList class:
```
>>> import h5py
>>> inHDF5file = h5py.File('example/tube/001/nn10T50.hdf5', 'r')
>>> nrTubes = len(inHDF5file)
>>> tube1 = inHDF5file["0"]
>>> print tube1[()]
>>> tube2 = inHDF5file["1"]
```

Other languages like c/c++ also have hdf5 implementations.



---
