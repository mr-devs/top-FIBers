#!/bin/bash

# Purpose:
#   This is a script that make connection between the LISA through lenny and access the database in there.
#
# Inputs:
#   None
#
# Configs:
#   python        :  This will get the conda environment path
#   loader_home   :  Add the data-loader path
#
# Output:
#   This will make connection with the LISA and insert the data in the tables. 
#
# How to call:
#   ```
#   cd /home/data/apps/topfibers/repo/data-loader/run_data_loader.sh
#   ```
#
#
# Author: Pasan Kamburugamuwa

python="/home/data/apps/topfibers/repo/environments/env_code/bin/python"

loader_home="/home/data/apps/topfibers/repo/data-loader"

# Create SSH tunnel
ssh -i /u/truthy/.ssh/id_rsa -4 -N -L 5580:localhost:5432 truthy@lisa.luddy.indiana.edu &

# Store the PID of the SSH tunnel process
tunnel_pid=$!

# Run Python script
${python} ${loader_home}/server.py

# Kill SSH tunnel process
kill $tunnel_pid

