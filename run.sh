#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR
gunicorn dashboard:app -b 127.0.0.1:5000
