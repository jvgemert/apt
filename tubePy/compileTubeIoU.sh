#!/bin/bash
python setupTubeIoU.py build_ext --inplace
mv tubePy/tubeIoU.so .
