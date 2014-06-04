#!/bin/bash

PATH_FOLDER="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

docker run -d -v $PATH_FOLDER:/home/dashboard:rw --name="dashboard" -p 5000:5000 mjulian/dashboard /home/dashboard/run.sh
