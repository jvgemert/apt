#!/bin/bash
python setupTube2trajIDs.py build_ext --inplace
mv tubePy/tube2trajIDs.so .
