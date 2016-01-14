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

All steps in this package can be done on the internal cluster format (which will be converted to tubes internally each time), or, they can be done on explicitly exported tube proposals.
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


### - Do you also have the 'Tubelet' results?

Yes. The Tubelet action tube proposals come from our CVPR 2014 paper [Action Localization by Tubelets from Motion](http://jvgemert.github.io/pub/jain-tubelets-cvpr2014.pdf) and are computed on MSR-II [MSRIITubeletCVPR14.tar.gz](http://isis-data.science.uva.nl/jvgemert/apt/MSRIITubeletCVPR14.tar.gz) and on UCF-Sports [ucfSportsTubeletCVPR14.tar.gz](http://isis-data.science.uva.nl/jvgemert/apt/ucfSportsTubeletCVPR14.tar.gz).

### - What is the tube dataformat?
A tube is a set of frameNRs and  bounding boxes.

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


### - What does the output look like? 


#### isTrimmedVideo=0;
```
./doExample.sh 
** Step 0: try to compile parts to cython **
Done compiling

** Step 1: Extract trajectories from the video **
run tubePy/extractDT.sh example/vid/001.avi example/feat/001/idt.hdf5
Saved temporary trajectories to: ./localexample/vid/001.avi/DenseTrackStab.txt.gz

** Convert the trajectories to the format as used for DTP **
python ./tubePy/runConvertDenseTraj2fvec.py ./localexample/vid/001.avi/DenseTrackStab.txt.gz example/feat/001/idt.hdf5
	writing to example/feat/001/idt.hdf5
	Information of video size, length: 55, width: 720, height: 404 ; Write 55 720 404 to: "vidinfo"
	Counting nr of features: 10k ; Total: 14337
	Feature: trajecShape, (nrTraj x dim) =  (14337, 40) ; Write to "trajecShape"
	Feature: trajecTubes, (nrTraj x dim) =  (14337, 60) ; Write to "trajecTubes"
	Feature: trajstab, (nrTraj x dim) =  (14337, 30) ; Write to "trajstab"
	Feature: hogstab, (nrTraj x dim) =  (14337, 96) ; Write to "hogstab"
	Feature: hofstab, (nrTraj x dim) =  (14337, 108) ; Write to "hofstab"
	Feature: mbhstab, (nrTraj x dim) =  (14337, 192) ; Write to "mbhstab"

clean up temporary file; rm  ./localexample/vid/001.avi/DenseTrackStab.txt.gz

** Step 2: Create Action Proposals from dense Trajectories by clustering **
python tubePy/runClust.py example/feat/001/idt.hdf5 10 0 example/clusts/001/nn10.hdf5
	adding (possible) missing features to example/clusts/001/nn10.hdf5

** Possible Step 3: Convenience function to export the clusters of step 2 to proposals **
python tubePy/runClust2tube.py example/clusts/001/nn10.hdf5 example/feat/001/idt.hdf5 50 example/tube/001/nn10T50.hdf5
	Write tubes to: example/tube/001/nn10T50.hdf5
	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	Reading feature file: example/feat/001/idt.hdf5, "vidinfo" size (3,)
	Feature: "hofstab"; Number of proposals: 48 tot: 48
	Feature: "hofstab-hogstab-trajstab-mbhstab"; Number of proposals: 70 tot: 118
	Feature: "hofstab-mbhstab"; Number of proposals: 62 tot: 180
	Feature: "hofstab-trajstab"; Number of proposals: 63 tot: 243
	Feature: "hofstab-trajstab-mbhstab"; Number of proposals: 67 tot: 310
	Feature: "hogstab"; Number of proposals: 71 tot: 381
	Feature: "hogstab-hofstab"; Number of proposals: 70 tot: 451
	Feature: "hogstab-hofstab-mbhstab"; Number of proposals: 69 tot: 520
	Feature: "hogstab-hofstab-trajstab"; Number of proposals: 66 tot: 586
	Feature: "hogstab-mbhstab"; Number of proposals: 71 tot: 657
	Feature: "hogstab-trajstab"; Number of proposals: 72 tot: 729
	Feature: "hogstab-trajstab-mbhstab"; Number of proposals: 70 tot: 799
	Feature: "mbhstab"; Number of proposals: 71 tot: 870
	Feature: "spat"; Number of proposals: 67 tot: 937
	Feature: "spat-hofstab"; Number of proposals: 69 tot: 1006
	Feature: "spat-hofstab-mbhstab"; Number of proposals: 70 tot: 1076
	Feature: "spat-hofstab-trajstab"; Number of proposals: 64 tot: 1140
	Feature: "spat-hofstab-trajstab-mbhstab"; Number of proposals: 72 tot: 1212
	Feature: "spat-hogstab"; Number of proposals: 70 tot: 1282
	Feature: "spat-hogstab-hofstab"; Number of proposals: 75 tot: 1357
	Feature: "spat-hogstab-hofstab-mbhstab"; Number of proposals: 75 tot: 1432
	Feature: "spat-hogstab-hofstab-trajstab"; Number of proposals: 74 tot: 1506
	Feature: "spat-hogstab-hofstab-trajstab-mbhstab"; Number of proposals: 72 tot: 1578
	Feature: "spat-hogstab-mbhstab"; Number of proposals: 72 tot: 1650
	Feature: "spat-hogstab-trajstab"; Number of proposals: 74 tot: 1724
	Feature: "spat-hogstab-trajstab-mbhstab"; Number of proposals: 76 tot: 1800
	Feature: "spat-mbhstab"; Number of proposals: 70 tot: 1870
	Feature: "spat-trajstab"; Number of proposals: 71 tot: 1941
	Feature: "spat-trajstab-mbhstab"; Number of proposals: 66 tot: 2007
	Feature: "trajstab"; Number of proposals: 67 tot: 2074
	Feature: "trajstab-mbhstab"; Number of proposals: 73 tot: 2147

** Step 4: Compare clustered proposals of step 2 to ground-truth(s) to obtain Intersection over Union (IoU) scores per tube proposal **
python tubePy/runTube2iou.py example/clusts/001/nn10.hdf5 example/IoU/001/nn10T50.txt example/gt/001/tubes.hdf5 50 example/feat/001/idt.hdf5
	Read ground truth; 	reading tubes: example/gt/001/tubes.hdf5 ; Number of tubes to read: 1
	Get trajectory positions; 	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	Get video dimensions; 	Reading feature file: example/feat/001/idt.hdf5, "vidinfo" size (3,)
	Feature: "hofstab", number of proposals: 48; 0 Best IoUs: [ 0.33105031] ; Best so far: [ 0.33105031]
	Feature: "hofstab-hogstab-trajstab-mbhstab", number of proposals: 70; 0 Best IoUs: [ 0.50275546] ; Best so far: [ 0.50275546]
	Feature: "hofstab-mbhstab", number of proposals: 62; 0 Best IoUs: [ 0.52908528] ; Best so far: [ 0.52908528]
	Feature: "hofstab-trajstab", number of proposals: 63; 0 Best IoUs: [ 0.49810889] ; Best so far: [ 0.52908528]
	Feature: "hofstab-trajstab-mbhstab", number of proposals: 67; 0 Best IoUs: [ 0.50223243] ; Best so far: [ 0.52908528]
	Feature: "hogstab", number of proposals: 71; 0 Best IoUs: [ 0.55509269] ; Best so far: [ 0.55509269]
	Feature: "hogstab-hofstab", number of proposals: 70; 0 Best IoUs: [ 0.53952658] ; Best so far: [ 0.55509269]
	Feature: "hogstab-hofstab-mbhstab", number of proposals: 69; 0 Best IoUs: [ 0.53791386] ; Best so far: [ 0.55509269]
	Feature: "hogstab-hofstab-trajstab", number of proposals: 66; 0 Best IoUs: [ 0.50420201] ; Best so far: [ 0.55509269]
	Feature: "hogstab-mbhstab", number of proposals: 71; 0 Best IoUs: [ 0.55121255] ; Best so far: [ 0.55509269]
	Feature: "hogstab-trajstab", number of proposals: 72; 0 Best IoUs: [ 0.50179219] ; Best so far: [ 0.55509269]
	Feature: "hogstab-trajstab-mbhstab", number of proposals: 70; 0 Best IoUs: [ 0.58327597] ; Best so far: [ 0.58327597]
	Feature: "mbhstab", number of proposals: 71; 0 Best IoUs: [ 0.53587353] ; Best so far: [ 0.58327597]
	Feature: "spat", number of proposals: 67; 0 Best IoUs: [ 0.54253024] ; Best so far: [ 0.58327597]
	Feature: "spat-hofstab", number of proposals: 69; 0 Best IoUs: [ 0.56753778] ; Best so far: [ 0.58327597]
	Feature: "spat-hofstab-mbhstab", number of proposals: 70; 0 Best IoUs: [ 0.56003076] ; Best so far: [ 0.58327597]
	Feature: "spat-hofstab-trajstab", number of proposals: 64; 0 Best IoUs: [ 0.55896378] ; Best so far: [ 0.58327597]
	Feature: "spat-hofstab-trajstab-mbhstab", number of proposals: 72; 0 Best IoUs: [ 0.55293119] ; Best so far: [ 0.58327597]
	Feature: "spat-hogstab", number of proposals: 70; 0 Best IoUs: [ 0.54906946] ; Best so far: [ 0.58327597]
	Feature: "spat-hogstab-hofstab", number of proposals: 75; 0 Best IoUs: [ 0.5381276] ; Best so far: [ 0.58327597]
	Feature: "spat-hogstab-hofstab-mbhstab", number of proposals: 75; 0 Best IoUs: [ 0.55357611] ; Best so far: [ 0.58327597]
	Feature: "spat-hogstab-hofstab-trajstab", number of proposals: 74; 0 Best IoUs: [ 0.54222506] ; Best so far: [ 0.58327597]
	Feature: "spat-hogstab-hofstab-trajstab-mbhstab", number of proposals: 72; 0 Best IoUs: [ 0.54427665] ; Best so far: [ 0.58327597]
	Feature: "spat-hogstab-mbhstab", number of proposals: 72; 0 Best IoUs: [ 0.544303] ; Best so far: [ 0.58327597]
	Feature: "spat-hogstab-trajstab", number of proposals: 74; 0 Best IoUs: [ 0.56068218] ; Best so far: [ 0.58327597]
	Feature: "spat-hogstab-trajstab-mbhstab", number of proposals: 76; 0 Best IoUs: [ 0.54952419] ; Best so far: [ 0.58327597]
	Feature: "spat-mbhstab", number of proposals: 70; 0 Best IoUs: [ 0.55278176] ; Best so far: [ 0.58327597]
	Feature: "spat-trajstab", number of proposals: 71; 0 Best IoUs: [ 0.55731547] ; Best so far: [ 0.58327597]
	Feature: "spat-trajstab-mbhstab", number of proposals: 66; 0 Best IoUs: [ 0.56513512] ; Best so far: [ 0.58327597]
	Feature: "trajstab", number of proposals: 67; 0 Best IoUs: [ 0.54874068] ; Best so far: [ 0.58327597]
	Feature: "trajstab-mbhstab", number of proposals: 73; 0 Best IoUs: [ 0.56846899] ; Best so far: [ 0.58327597]
	Writing IoU scores to example/IoU/001/nn10T50.txt

** Or do Step 4 on the exported tubes of step 3: Compare to ground-truth(s) to obtain Intersection over Union (IoU) scores per tube proposal **
python tubePy/runTube2iou.py example/tube/001/nn10T50.hdf5 example/IoU-tubes/001/nn10T50.txt example/gt/001/tubes.hdf5
	Read ground truth; 	reading tubes: example/gt/001/tubes.hdf5 ; Number of tubes to read: 1
	reading tubes: example/tube/001/nn10T50.hdf5 ; Number of tubes to read: 2147
	Feature: "tubes", number of proposals: 2147; 0 1000 2000 Best IoUs: [ 0.58327597] ; Best so far: [ 0.58327597]
	Writing IoU scores to example/IoU-tubes/001/nn10T50.txt

** Step 5: Find trajectory IDs that are inside of each clustered proposal from step 2 **
python tubePy/runTube2trajIDs.py example/clusts/001/nn10.hdf5 example/trajIDs/001/nn10T50.hdf5 example/feat/001/idt.hdf5 50
	Get trajectory positions; 	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	Get video dimensions; 	Reading feature file: example/feat/001/idt.hdf5, "vidinfo" size (3,)
	Feature: "hofstab", number of proposals: 48;
	Feature: "hofstab-hogstab-trajstab-mbhstab", number of proposals: 70;
	Feature: "hofstab-mbhstab", number of proposals: 62;
	Feature: "hofstab-trajstab", number of proposals: 63;
	Feature: "hofstab-trajstab-mbhstab", number of proposals: 67;
	Feature: "hogstab", number of proposals: 71;
	Feature: "hogstab-hofstab", number of proposals: 70;
	Feature: "hogstab-hofstab-mbhstab", number of proposals: 69;
	Feature: "hogstab-hofstab-trajstab", number of proposals: 66;
	Feature: "hogstab-mbhstab", number of proposals: 71;
	Feature: "hogstab-trajstab", number of proposals: 72;
	Feature: "hogstab-trajstab-mbhstab", number of proposals: 70;
	Feature: "mbhstab", number of proposals: 71;
	Feature: "spat", number of proposals: 67;
	Feature: "spat-hofstab", number of proposals: 69;
	Feature: "spat-hofstab-mbhstab", number of proposals: 70;
	Feature: "spat-hofstab-trajstab", number of proposals: 64;
	Feature: "spat-hofstab-trajstab-mbhstab", number of proposals: 72;
	Feature: "spat-hogstab", number of proposals: 70;
	Feature: "spat-hogstab-hofstab", number of proposals: 75;
	Feature: "spat-hogstab-hofstab-mbhstab", number of proposals: 75;
	Feature: "spat-hogstab-hofstab-trajstab", number of proposals: 74;
	Feature: "spat-hogstab-hofstab-trajstab-mbhstab", number of proposals: 72;
	Feature: "spat-hogstab-mbhstab", number of proposals: 72;
	Feature: "spat-hogstab-trajstab", number of proposals: 74;
	Feature: "spat-hogstab-trajstab-mbhstab", number of proposals: 76;
	Feature: "spat-mbhstab", number of proposals: 70;
	Feature: "spat-trajstab", number of proposals: 71;
	Feature: "spat-trajstab-mbhstab", number of proposals: 66;
	Feature: "trajstab", number of proposals: 67;
	Feature: "trajstab-mbhstab", number of proposals: 73;
	Write trajectory IDs to example/trajIDs/001/nn10T50.hdf5

** Or do Step 5 on the exported tubes of step 3: Find trajectory IDs that are inside of each proposal **
python tubePy/runTube2trajIDs.py example/tube/001/nn10T50.hdf5 example/trajIDs-tubes/001/nn10T50.hdf5 example/feat/001/idt.hdf5
	Get trajectory positions; 	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	reading tubes: example/tube/001/nn10T50.hdf5 ; Number of tubes to read: 2147
	Feature: "tubes", number of proposals: 2147;
	Write trajectory IDs to example/trajIDs-tubes/001/nn10T50.hdf5
```

#### isTrimmedVideo=1;
```
./doExample.sh 
** Step 0: try to compile parts to cython **
Done compiling

** Step 1: Extract trajectories from the video **
run tubePy/extractDT.sh example/vid/001.avi example/feat/001/idt.hdf5

** Step 2: Create Action Proposals from dense Trajectories by clustering **
python tubePy/runClust.py example/feat/001/idt.hdf5 10 1 example/clusts/001/nn10.hdf5
	writing features to example/clusts/001/nn10.hdf5
	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	Finding 10 nearest neighbors, for 14337 trajectories .
	Creating the neighborhood graph for k=10; the maximum number of neighbors is 23 .
	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	Computing feature similarities for all neighboring trajectory pairs .
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 7.90s
	write to: example/clusts/001/nn10.hdf5, "spat"
	Reading feature file: example/feat/001/idt.hdf5, "hogstab" size (14337, 96)
	Computing feature similarities for all neighboring trajectory pairs .
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 8.82s
	write to: example/clusts/001/nn10.hdf5, "hogstab"
	Reading feature file: example/feat/001/idt.hdf5, "hofstab" size (14337, 108)
	Computing feature similarities for all neighboring trajectory pairs .
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 9.92s
	write to: example/clusts/001/nn10.hdf5, "hofstab"
	Reading feature file: example/feat/001/idt.hdf5, "trajstab" size (14337, 30)
	Computing feature similarities for all neighboring trajectory pairs .
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 10.81s
	write to: example/clusts/001/nn10.hdf5, "trajstab"
	Reading feature file: example/feat/001/idt.hdf5, "mbhstab" size (14337, 192)
	Computing feature similarities for all neighboring trajectory pairs .
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 11.74s
	write to: example/clusts/001/nn10.hdf5, "mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 12.08s
	write to: example/clusts/001/nn10.hdf5, "spat-hogstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 12.42s
	write to: example/clusts/001/nn10.hdf5, "spat-hofstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 12.76s
	write to: example/clusts/001/nn10.hdf5, "spat-trajstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 13.08s
	write to: example/clusts/001/nn10.hdf5, "spat-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 13.39s
	write to: example/clusts/001/nn10.hdf5, "hogstab-hofstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 13.75s
	write to: example/clusts/001/nn10.hdf5, "hogstab-trajstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 14.07s
	write to: example/clusts/001/nn10.hdf5, "hogstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 14.41s
	write to: example/clusts/001/nn10.hdf5, "hofstab-trajstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 14.74s
	write to: example/clusts/001/nn10.hdf5, "hofstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 15.08s
	write to: example/clusts/001/nn10.hdf5, "trajstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 15.35s
	write to: example/clusts/001/nn10.hdf5, "spat-hogstab-hofstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 15.63s
	write to: example/clusts/001/nn10.hdf5, "spat-hogstab-trajstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 15.90s
	write to: example/clusts/001/nn10.hdf5, "spat-hogstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 16.19s
	write to: example/clusts/001/nn10.hdf5, "spat-hofstab-trajstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 16.46s
	write to: example/clusts/001/nn10.hdf5, "spat-hofstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 16.74s
	write to: example/clusts/001/nn10.hdf5, "spat-trajstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 17.04s
	write to: example/clusts/001/nn10.hdf5, "hogstab-hofstab-trajstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 17.33s
	write to: example/clusts/001/nn10.hdf5, "hogstab-hofstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 17.63s
	write to: example/clusts/001/nn10.hdf5, "hogstab-trajstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 17.92s
	write to: example/clusts/001/nn10.hdf5, "hofstab-trajstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 18.27s
	write to: example/clusts/001/nn10.hdf5, "spat-hogstab-hofstab-trajstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 18.59s
	write to: example/clusts/001/nn10.hdf5, "spat-hogstab-hofstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 18.96s
	write to: example/clusts/001/nn10.hdf5, "spat-hogstab-trajstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 19.31s
	write to: example/clusts/001/nn10.hdf5, "spat-hofstab-trajstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 19.65s
	write to: example/clusts/001/nn10.hdf5, "hofstab-hogstab-trajstab-mbhstab"
	Run SLINK clustering in cython 1: 2: 3: 4: 5: 6: 7: 8: 9: 10: 11: 12: 13: 14: ; Time: 19.94s
	write to: example/clusts/001/nn10.hdf5, "spat-hogstab-hofstab-trajstab-mbhstab"

** Possible Step 3: Convenience function to export the clusters of step 2 to proposals **
python tubePy/runClust2tube.py example/clusts/001/nn10.hdf5 example/feat/001/idt.hdf5 50 example/tube/001/nn10T50.hdf5
	Write tubes to: example/tube/001/nn10T50.hdf5
	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	Reading feature file: example/feat/001/idt.hdf5, "vidinfo" size (3,)
	Feature: "hofstab"; Number of proposals: 48 tot: 48
	Feature: "hofstab-hogstab-trajstab-mbhstab"; Number of proposals: 47 tot: 95
	Feature: "hofstab-mbhstab"; Number of proposals: 46 tot: 141
	Feature: "hofstab-trajstab"; Number of proposals: 43 tot: 184
	Feature: "hofstab-trajstab-mbhstab"; Number of proposals: 71 tot: 255
	Feature: "hogstab"; Number of proposals: 70 tot: 325
	Feature: "hogstab-hofstab"; Number of proposals: 49 tot: 374
	Feature: "hogstab-hofstab-mbhstab"; Number of proposals: 60 tot: 434
	Feature: "hogstab-hofstab-trajstab"; Number of proposals: 60 tot: 494
	Feature: "hogstab-mbhstab"; Number of proposals: 54 tot: 548
	Feature: "hogstab-trajstab"; Number of proposals: 51 tot: 599
	Feature: "hogstab-trajstab-mbhstab"; Number of proposals: 73 tot: 672
	Feature: "mbhstab"; Number of proposals: 71 tot: 743
	Feature: "spat"; Number of proposals: 66 tot: 809
	Feature: "spat-hofstab"; Number of proposals: 46 tot: 855
	Feature: "spat-hofstab-mbhstab"; Number of proposals: 66 tot: 921
	Feature: "spat-hofstab-trajstab"; Number of proposals: 68 tot: 989
	Feature: "spat-hofstab-trajstab-mbhstab"; Number of proposals: 44 tot: 1033
	Feature: "spat-hogstab"; Number of proposals: 50 tot: 1083
	Feature: "spat-hogstab-hofstab"; Number of proposals: 67 tot: 1150
	Feature: "spat-hogstab-hofstab-mbhstab"; Number of proposals: 52 tot: 1202
	Feature: "spat-hogstab-hofstab-trajstab"; Number of proposals: 47 tot: 1249
	Feature: "spat-hogstab-hofstab-trajstab-mbhstab"; Number of proposals: 68 tot: 1317
	Feature: "spat-hogstab-mbhstab"; Number of proposals: 73 tot: 1390
	Feature: "spat-hogstab-trajstab"; Number of proposals: 68 tot: 1458
	Feature: "spat-hogstab-trajstab-mbhstab"; Number of proposals: 52 tot: 1510
	Feature: "spat-mbhstab"; Number of proposals: 54 tot: 1564
	Feature: "spat-trajstab"; Number of proposals: 46 tot: 1610
	Feature: "spat-trajstab-mbhstab"; Number of proposals: 63 tot: 1673
	Feature: "trajstab"; Number of proposals: 67 tot: 1740
	Feature: "trajstab-mbhstab"; Number of proposals: 57 tot: 1797

** Step 4: Compare clustered proposals of step 2 to ground-truth(s) to obtain Intersection over Union (IoU) scores per tube proposal **
python tubePy/runTube2iou.py example/clusts/001/nn10.hdf5 example/IoU/001/nn10T50.txt example/gt/001/tubes.hdf5 50 example/feat/001/idt.hdf5
	Read ground truth; 	reading tubes: example/gt/001/tubes.hdf5 ; Number of tubes to read: 1
	Get trajectory positions; 	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	Get video dimensions; 	Reading feature file: example/feat/001/idt.hdf5, "vidinfo" size (3,)
	Feature: "hofstab", number of proposals: 48; 0 Best IoUs: [ 0.33105031] ; Best so far: [ 0.33105031]
	Feature: "hofstab-hogstab-trajstab-mbhstab", number of proposals: 47; 0 Best IoUs: [ 0.36498034] ; Best so far: [ 0.36498034]
	Feature: "hofstab-mbhstab", number of proposals: 46; 0 Best IoUs: [ 0.53581631] ; Best so far: [ 0.53581631]
	Feature: "hofstab-trajstab", number of proposals: 43; 0 Best IoUs: [ 0.5345403] ; Best so far: [ 0.53581631]
	Feature: "hofstab-trajstab-mbhstab", number of proposals: 71; 0 Best IoUs: [ 0.40785718] ; Best so far: [ 0.53581631]
	Feature: "hogstab", number of proposals: 70; 0 Best IoUs: [ 0.55509269] ; Best so far: [ 0.55509269]
	Feature: "hogstab-hofstab", number of proposals: 49; 0 Best IoUs: [ 0.45972297] ; Best so far: [ 0.55509269]
	Feature: "hogstab-hofstab-mbhstab", number of proposals: 60; 0 Best IoUs: [ 0.56552345] ; Best so far: [ 0.56552345]
	Feature: "hogstab-hofstab-trajstab", number of proposals: 60; 0 Best IoUs: [ 0.55978656] ; Best so far: [ 0.56552345]
	Feature: "hogstab-mbhstab", number of proposals: 54; 0 Best IoUs: [ 0.58594525] ; Best so far: [ 0.58594525]
	Feature: "hogstab-trajstab", number of proposals: 51; 0 Best IoUs: [ 0.25605616] ; Best so far: [ 0.58594525]
	Feature: "hogstab-trajstab-mbhstab", number of proposals: 73; 0 Best IoUs: [ 0.59684622] ; Best so far: [ 0.59684622]
	Feature: "mbhstab", number of proposals: 71; 0 Best IoUs: [ 0.54105645] ; Best so far: [ 0.59684622]
	Feature: "spat", number of proposals: 66; 0 Best IoUs: [ 0.54721773] ; Best so far: [ 0.59684622]
	Feature: "spat-hofstab", number of proposals: 46; 0 Best IoUs: [ 0.30386361] ; Best so far: [ 0.59684622]
	Feature: "spat-hofstab-mbhstab", number of proposals: 66; 0 Best IoUs: [ 0.58907235] ; Best so far: [ 0.59684622]
	Feature: "spat-hofstab-trajstab", number of proposals: 68; 0 Best IoUs: [ 0.3859756] ; Best so far: [ 0.59684622]
	Feature: "spat-hofstab-trajstab-mbhstab", number of proposals: 44; 0 Best IoUs: [ 0.23712544] ; Best so far: [ 0.59684622]
	Feature: "spat-hogstab", number of proposals: 50; 0 Best IoUs: [ 0.49025244] ; Best so far: [ 0.59684622]
	Feature: "spat-hogstab-hofstab", number of proposals: 67; 0 Best IoUs: [ 0.58805013] ; Best so far: [ 0.59684622]
	Feature: "spat-hogstab-hofstab-mbhstab", number of proposals: 52; 0 Best IoUs: [ 0.27198192] ; Best so far: [ 0.59684622]
	Feature: "spat-hogstab-hofstab-trajstab", number of proposals: 47; 0 Best IoUs: [ 0.26660463] ; Best so far: [ 0.59684622]
	Feature: "spat-hogstab-hofstab-trajstab-mbhstab", number of proposals: 68; 0 Best IoUs: [ 0.43409982] ; Best so far: [ 0.59684622]
	Feature: "spat-hogstab-mbhstab", number of proposals: 73; 0 Best IoUs: [ 0.57482898] ; Best so far: [ 0.59684622]
	Feature: "spat-hogstab-trajstab", number of proposals: 68; 0 Best IoUs: [ 0.50923556] ; Best so far: [ 0.59684622]
	Feature: "spat-hogstab-trajstab-mbhstab", number of proposals: 52; 0 Best IoUs: [ 0.24952577] ; Best so far: [ 0.59684622]
	Feature: "spat-mbhstab", number of proposals: 54; 0 Best IoUs: [ 0.31943393] ; Best so far: [ 0.59684622]
	Feature: "spat-trajstab", number of proposals: 46; 0 Best IoUs: [ 0.29647863] ; Best so far: [ 0.59684622]
	Feature: "spat-trajstab-mbhstab", number of proposals: 63; 0 Best IoUs: [ 0.39398888] ; Best so far: [ 0.59684622]
	Feature: "trajstab", number of proposals: 67; 0 Best IoUs: [ 0.54874068] ; Best so far: [ 0.59684622]
	Feature: "trajstab-mbhstab", number of proposals: 57; 0 Best IoUs: [ 0.25747517] ; Best so far: [ 0.59684622]
	Writing IoU scores to example/IoU/001/nn10T50.txt

** Or do Step 4 on the exported tubes of step 3: Compare to ground-truth(s) to obtain Intersection over Union (IoU) scores per tube proposal **
python tubePy/runTube2iou.py example/tube/001/nn10T50.hdf5 example/IoU-tubes/001/nn10T50.txt example/gt/001/tubes.hdf5
	Read ground truth; 	reading tubes: example/gt/001/tubes.hdf5 ; Number of tubes to read: 1
	reading tubes: example/tube/001/nn10T50.hdf5 ; Number of tubes to read: 1797
	Feature: "tubes", number of proposals: 1797; 0 1000 Best IoUs: [ 0.59684622] ; Best so far: [ 0.59684622]
	Writing IoU scores to example/IoU-tubes/001/nn10T50.txt

** Step 5: Find trajectory IDs that are inside of each clustered proposal from step 2 **
python tubePy/runTube2trajIDs.py example/clusts/001/nn10.hdf5 example/trajIDs/001/nn10T50.hdf5 example/feat/001/idt.hdf5 50
	Get trajectory positions; 	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	Get video dimensions; 	Reading feature file: example/feat/001/idt.hdf5, "vidinfo" size (3,)
	Feature: "hofstab", number of proposals: 48;
	Feature: "hofstab-hogstab-trajstab-mbhstab", number of proposals: 47;
	Feature: "hofstab-mbhstab", number of proposals: 46;
	Feature: "hofstab-trajstab", number of proposals: 43;
	Feature: "hofstab-trajstab-mbhstab", number of proposals: 71;
	Feature: "hogstab", number of proposals: 70;
	Feature: "hogstab-hofstab", number of proposals: 49;
	Feature: "hogstab-hofstab-mbhstab", number of proposals: 60;
	Feature: "hogstab-hofstab-trajstab", number of proposals: 60;
	Feature: "hogstab-mbhstab", number of proposals: 54;
	Feature: "hogstab-trajstab", number of proposals: 51;
	Feature: "hogstab-trajstab-mbhstab", number of proposals: 73;
	Feature: "mbhstab", number of proposals: 71;
	Feature: "spat", number of proposals: 66;
	Feature: "spat-hofstab", number of proposals: 46;
	Feature: "spat-hofstab-mbhstab", number of proposals: 66;
	Feature: "spat-hofstab-trajstab", number of proposals: 68;
	Feature: "spat-hofstab-trajstab-mbhstab", number of proposals: 44;
	Feature: "spat-hogstab", number of proposals: 50;
	Feature: "spat-hogstab-hofstab", number of proposals: 67;
	Feature: "spat-hogstab-hofstab-mbhstab", number of proposals: 52;
	Feature: "spat-hogstab-hofstab-trajstab", number of proposals: 47;
	Feature: "spat-hogstab-hofstab-trajstab-mbhstab", number of proposals: 68;
	Feature: "spat-hogstab-mbhstab", number of proposals: 73;
	Feature: "spat-hogstab-trajstab", number of proposals: 68;
	Feature: "spat-hogstab-trajstab-mbhstab", number of proposals: 52;
	Feature: "spat-mbhstab", number of proposals: 54;
	Feature: "spat-trajstab", number of proposals: 46;
	Feature: "spat-trajstab-mbhstab", number of proposals: 63;
	Feature: "trajstab", number of proposals: 67;
	Feature: "trajstab-mbhstab", number of proposals: 57;
	Write trajectory IDs to example/trajIDs/001/nn10T50.hdf5

** Or do Step 5 on the exported tubes of step 3: Find trajectory IDs that are inside of each proposal **
python tubePy/runTube2trajIDs.py example/tube/001/nn10T50.hdf5 example/trajIDs-tubes/001/nn10T50.hdf5 example/feat/001/idt.hdf5
	Get trajectory positions; 	Reading feature file: example/feat/001/idt.hdf5, "trajecShape" size (14337, 40)
	reading tubes: example/tube/001/nn10T50.hdf5 ; Number of tubes to read: 1797
	Feature: "tubes", number of proposals: 1797;
	Write trajectory IDs to example/trajIDs-tubes/001/nn10T50.hdf5
```

---



