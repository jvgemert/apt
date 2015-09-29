#!/bin/bash
python setupSlink.py build_ext --inplace
mv tubePy/slink.so .
