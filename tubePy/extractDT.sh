#!/bin/bash 
#
# This script extracts dense trajectories as used for computing Dense Trajectory Proposals (DTPs) on a video.
# 
# This script is part of the Python code for Dense Trajectory Proposals (DTP). 
# Written by Jan van Gemert, if you find any bugs, feel free to let me know. 
# If you find the code useful, please cite our paper: "Fast Spatio-Temporal Proposals for Action Localization"
#
# All cpp code here is to the credit of INRIA, H. Wang.
# Improved Trajectory code (http://lear.inrialpes.fr/people/wang/improved_trajectories 
#
# Note that DenseTrackStab.cpp is slightly adapted to export the trajectory x and y per frame, and also the video statistics (width, height, length) are exported. 
# See the comments in DenseTrackStab.cpp


localDir=./local"$1";
mkdir -p $localDir

#/var/scratch/jvgemert/DTPy/third/DenseTrackStab $1 | gzip > "$localDir"/DenseTrackStab.txt.gz
./third/DenseTrackStab $1 | gzip > "$localDir"/DenseTrackStab.txt.gz

echo  "$localDir"/DenseTrackStab.txt.gz
echo
echo "** Convert the trajectories to the format as used for DTP **"
python ./tubePy/runConvertDenseTraj2fvec.py "$localDir"/DenseTrackStab.txt.gz $2

echo
echo "clean up temporary file; rm " "$localDir"/DenseTrackStab.txt.gz

rm  "$localDir"/DenseTrackStab.txt.gz
