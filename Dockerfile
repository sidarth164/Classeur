#This creates an image for storage server
FROM ubuntu:16.04
MAINTAINER nileshv1997@gmail.com

RUN apt-get update
RUN apt-get install iputils-ping
RUN apt-get install net-tools
RUN apt-get install python2.7
RUN apt-get install python-pip
RUN pip install hurry.filesize
RUN pip install virtualenv
RUN pip install grpcio
RUN pip install grpcio-tools
RUN pip install googleapis-common-protos
RUN pip install pymongo
CMD ["echo","Image created"]
