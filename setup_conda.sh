#!/bin/bash

# Create a new conda environment with Python 3.11
conda create --name real-estate-automation python=3.11 -y

# Install dependencies using the python from the new environment
/Users/gurindersingh/conda/envs/real-estate-automation/bin/python -m pip install -r requirements.txt