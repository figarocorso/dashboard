FROM ubuntu:14.04

RUN echo "deb http://de.archive.ubuntu.com/ubuntu trusty main universe" >> /etc/apt/sources.list

# Installing dependencies
RUN apt-get update
RUN apt-get install -y --force-yes python python-pip

# Installing more dependencies
ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

VOLUME [/home/dashboard]

EXPOSE 5000
