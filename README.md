Python code for Action Proposals from dense Trajectory (APT). 
Written by Jan van Gemert, if you find any bugs or improvements, feel free to let me know. 
If you find the code useful, please cite our paper: "APT: Action localization Proposals from dense Trajectories"

Note that this code may not run out of the box.
This is because the third party libraries need to be installed, and they may vary depending on your system. 
For convenience we include all third party code here, although all credit for them is with the original authors, and we highly recommend them.

# Requirements:
 - python 2.7
 - numpy
 - h5py (hdf5 data format)
 - cython
 - yael ( best: https://gforge.inria.fr/projects/yael/ or see 'third/yael_v438.tar.gz'; Configure yael with "./configure.sh --enable-numpy" )
 - Improved Trajectory code (http://lear.inrialpes.fr/people/wang/improved_trajectories or see folder 'third/'. Note that DenseTrackStab.cpp is adapted to export the trajectory x and y per frame, and the video statistics (width, height, lenght) are exported. See 'third/' for the modified version of DenseTrackStab.cpp. And, see tubePy/extractDT.sh for an example script on how to extract them.

# Cython:
The APT package contains Python code with some parts in cython. The code also works without cython, albeit slower (slower parts are: clustering, merging, and IoU computations). To take advantage of the cython speedup you have to compile the tubePy/*.pyx files (see the compile2cython.sh script that calls the individual tubePy/compile*.sh scripts). 

# Organization

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
 yael: https://gforge.inria.fr/projects/yael/ 
 Improved Trajectory code: http://lear.inrialpes.fr/people/wang/improved_trajectories 

# doExample.sh

The 'doExample.sh' file has all steps explained to compute APT for the included example, the steps it does are:

1- extract the dense trajectories from the video and put in the expected format --> feat/
2- create Action Proposals from dense Trajectories by clustering --> clusts/
3- convenience function to convert proposals clusters of step 2 to tubes --> tubes/
4- compare proposal clusters/tubes to groundTruth, outputs IoU overlap scores in --> IoU/
5- convert proposal clusters/tubes to (0-based) trajectory IDs, so that the trajectories in a proposal can be mapped to Vlad/Fisher-vector/BoW --> trajIDs/ 

all steps in this package can be done on the internal cluster format (which will be converted to tubes internally each time), or, they can be done on explicitly exported tube proposals.
The reason for providing a 'detour' to tube files, is the ability to use tubes in other software.
The example includes all steps for the internal cluster format, and also for tube files.

For more details, read 'doExample.sh'.

The included example consists of sub folders. The minimum input requirements are:

    example/
        gt/             # Tube ground truth (needed for evaluating proposal quality)
        vid/            # Input video

The output is computed with this packages, which results in the following folder structure:

    example/
        feat/           # dense trajectory features 
        IoU/            # Intersection over Union scores with ground truth for proposals 
        IoU-tubes/      # Intersection over Union scores with ground truth for proposals in txt format
        clusts/         # Cluster results
        trajIDs/        # The trajectory IDs that belong to proposal tubes
        trajIDs-tubes/  # The trajectory IDs that belong to proposal tubes in txt format
        tubes/          # Tube proposals


To start, it is best to read and run the 'doExample.sh' file, it has all steps required to compute APT for an included example video: /example/vid/001.avi.

