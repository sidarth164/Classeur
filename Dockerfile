#This creates an image for storage server
FROM ubuntu:16.04
MAINTAINER nileshv1997@gmail.com

RUN apt-get update
RUN apt-get install iputils-ping
RUN apt-get install net-tools
RUN apt-get install python2.7
CMD ["echo","Image created"]
