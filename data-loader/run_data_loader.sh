#!/bin/bash

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

