#!/bin/bash
# script to compile python functions to cython
# cython will have to be installed 
#
# If compilation to cython does not succeed, the code will still run as pure python; albeit slower.

cd tubePy

# test if .so file exists, if not, try to compile it
if [ ! -f slink.so ]; then
    echo "** Compiling SLINK to cython"
    ./compileSlink.sh
fi

# test if .so file exists, if not, try to compile it
if [ ! -f tube2trajIDs.so ]; then
    echo "** Compiling tube2trajIDs to cython"
    ./compileTube2trajIDs.sh
fi


# test if .so file exists, if not, try to compile it
if [ ! -f tubeIoU.so ]; then
    echo "** Compiling TubeIoU to cython"
    ./compileTubeIoU.sh
fi


cd ..

echo "Done compiling"

