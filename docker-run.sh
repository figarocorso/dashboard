#!/bin/bash

docker run -d --name="dashboard" -p 5000:5000 mjulian/dashboard /home/dashboard/dashboard-master/run.sh
