ZENTYAL OVERVIEW DASHBOARD
==========================

The aim of this project is to provide as much information about Zentyal stability in only one page. It takes information from the following sources:

* Our continuous integration tool (Jenkins)
* Our Redmine (issue tracker) network (both internal and external)

## Installation
    sudo pip install -r requirements.txt
    ./run.sh

## Deploy
Docker configuration has recently been added.

* Copy the following files to the server you want to deploy (Dockerfile, docker-\* and dashboard.conf)
* docker-build.sh will prepare a container installing all the dependencies, and then will download the master branch of this repo into **/home/dashboard**.
* docker-run.sh will run the container, you will be able to access at port 5000.
* docker-stop.sh will stop the container.
