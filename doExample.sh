#!/bin/bash
#set -x #echo on
#
# This script gives an example of computing APT action proposals on a sample video from UCF-sports (Diving/001).
#
# Python code for Action Proposals from dense Trajectory (APT). 
# Written by Jan van Gemert, if you find any bugs or improvements, feel free to let me know. 
# If you find the code useful, please cite our paper: "APT: Action localization Proposals from dense Trajectories"
#
# The algorithmic steps:
#
# 1- extract the dense trajectories from the video and put in the expected format --> feat/
# 2- create Action Proposals from dense Trajectories by clustering --> clusts/
# 3- convenience function to convert proposals clusters of step 2 to tubes --> tubes/
# 4- compare proposal clusters/tubes to groundTruth, outputs IoU overlap scores in --> IoU/
# 5- convert proposal clusters/tubes to (0-based) trajectory IDs, so that the trajectories in a proposal can be mapped to Vlad/Fisher-vector/BoW --> trajIDs/ 
#
# Steps 4 and 5 can be done on the hierarchical clusters (in a binary cluster format which will be converted to proposals internally), or, the clusters can be first exported to proposal files, which can be used by step 4 and 5.
# The example includes all steps for both the internal cluster format, and also for proposals files.
#
########
# PARAMETERS to set: 
########
# isTrimmedVideo: is the video trimmed or untrimmed?
#   isTrimmedVideo=1; the datasets UCF-sports and UCF101 contain trimmed clips around an action 
#   isTrimmedVideo=0; the MSR-II dataset is untrimmed, the action can occur anywhere in the video
isTrimmedVideo=0;

# nrNN: nr of nearest neigbors to consider
nrNN=10;

# nrTrajThresh4Tube: min nr of trajectories required to output a tube
#   Adjust this parameter if you want more/less tube proposals 
#   - a lower value will give higher recall, but outputs more tubes
#   - a higher value will output less tubes, but also reduces recall
nrTrajThresh4Tube=50;

########
# Paths to set
########
#

# the name of the video
vidName=001
# video file
vidFile=example/vid/$vidName.avi;
# ground truth tube
gtFile=example/gt/$vidName/tubes.hdf5;
# trajectory features
featFile=example/feat/$vidName/idt.hdf5;
# trajectory clusters
clustFile=example/clusts/$vidName/nn"$nrNN".hdf5;
# tubes
tubeFile=example/tube/$vidName/nn"$nrNN"T"$nrTrajThresh4Tube".hdf5;
# Intersection over Union scores
iouFile=example/IoU/$vidName/nn"$nrNN"T"$nrTrajThresh4Tube".txt;
# Intersection over Union scores based on tubes
iouFromTubesFile=example/IoU-tubes/$vidName/nn"$nrNN"T"$nrTrajThresh4Tube".txt;
# exported trajectory IDs per cluster
trajIDsFile=example/trajIDs/$vidName/nn"$nrNN"T"$nrTrajThresh4Tube".hdf5;
# exported trajectory IDs per cluster based on tubes
trajIDsFromTubesFile=example/trajIDs-tubes/$vidName/nn"$nrNN"T"$nrTrajThresh4Tube".hdf5;

########
# First try to compile to cython, if compilation fails the code will run in pure python, albeit slower.
echo "** Step 0: try to compile parts to cython **"
./compile2cython.sh
echo

######## Step 1: Extract improved trajectories from the video and put them in the expected format
##
## Warning: you need to have the improved trajectory executable in 'third/DenseTrackStab' compiled for your platform
##
echo "** Step 1: Extract trajectories from the video **"
echo "run tubePy/extractDT.sh" $vidFile $featFile
tubePy/extractDT.sh $vidFile $featFile

######## Step 2: Create Action Proposals form dense Trajectories by trajectory clustering
##
echo
echo "** Step 2: Create Action Proposals from dense Trajectories by clustering **"
echo "python tubePy/runClust.py" $featFile $nrNN $isTrimmedVideo $clustFile
python tubePy/runClust.py $featFile $nrNN $isTrimmedVideo $clustFile

######## Possible Step 3: (not-essential) function to export the clusters of step 2 to proposals 
##
echo
echo "** Possible Step 3: Convenience function to export the clusters of step 2 to proposals **"
echo "python tubePy/runClust2tube.py" $clustFile $featFile $nrTrajThresh4Tube $tubeFile 
python tubePy/runClust2tube.py $clustFile $featFile $nrTrajThresh4Tube $tubeFile 

######## Step 4: Compare proposals to ground-truth(s) to obtain Intersection over Union (IoU) scores per tube proposal; can be used on the clusters of step 2 or on the tubes of step 3
## 
echo
echo "** Step 4: Compare clustered proposals of step 2 to ground-truth(s) to obtain Intersection over Union (IoU) scores per tube proposal **"
echo "python tubePy/runTube2iou.py" $clustFile $iouFile $gtFile $nrTrajThresh4Tube $featFile
python tubePy/runTube2iou.py $clustFile $iouFile $gtFile $nrTrajThresh4Tube $featFile

echo
echo "** Or do Step 4 on the exported tubes of step 3: Compare to ground-truth(s) to obtain Intersection over Union (IoU) scores per tube proposal **"
echo "python tubePy/runTube2iou.py" $tubeFile $iouFromTubesFile $gtFile
python tubePy/runTube2iou.py $tubeFile $iouFromTubesFile $gtFile

######## Step 5: Output the trajectory IDs that are inside of proposals (to allow classification). Trajectory IDs are used to identify trajectories (0-based, so the first trajectory = 0); this step can be done on the clusters of step 2 or on the exported tubes of step 3
##
echo
echo "** Step 5: Find trajectory IDs that are inside of each clustered proposal from step 2 **"
echo "python tubePy/runTube2trajIDs.py" $clustFile $trajIDsFile $featFile $nrTrajThresh4Tube
python tubePy/runTube2trajIDs.py $clustFile $trajIDsFile $featFile $nrTrajThresh4Tube

echo
echo "** Or do Step 5 on the exported tubes of step 3: Find trajectory IDs that are inside of each proposal **"
echo "python tubePy/runTube2trajIDs.py" $tubeFile $trajIDsFromTubesFile $featFile
python tubePy/runTube2trajIDs.py $tubeFile $trajIDsFromTubesFile $featFile

