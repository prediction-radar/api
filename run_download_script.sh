#!/bin/bash

conda init bash
conda activate radarenv

python /root/data_processing/download_grib.py
