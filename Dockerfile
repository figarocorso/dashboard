FROM ubuntu:14.04

# Installing dependencies
RUN apt-get update
RUN apt-get install -y --force-yes python python-pip wget

# Downloading the source code
RUN mkdir -p /home/dashboard
RUN wget https://github.com/figarocorso/dashboard/archive/master.tar.gz -O /home/dashboard/master.tar.gz
RUN tar xzf /home/dashboard/master.tar.gz -C /home/dashboard
RUN rm -rf /home/dashboard/master.tar.gz
RUN ls -la /home/dashboard/*

# Installing more dependencies
RUN pip install -r /home/dashboard/dashboard-master/requirements.txt

# Adding our customized configuration file
ADD dashboard.conf /home/dashboard/dashboard-master/dashboard.conf

EXPOSE 5000
