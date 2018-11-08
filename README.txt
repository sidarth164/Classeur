To run this demo, first ensure if you have the necessary pre-requisites:

Prerequisites:
--------------

gRPC Python is supported for use with Python 2.7 or Python 3.4 or higher.

Ensure you have pip version 9.0.1 or higher:

$ python -m pip install --upgrade pip

If you cannot upgrade pip due to a system-owned installation, you can run the example in a virtualenv:

$ python -m pip install virtualenv
$ virtualenv grpcDemo
$ source grpcDemo/bin/activate
$ python -m pip install --upgrade pip

Install gRPC:

$ python -m pip install grpcio

Install gRPC tools

Python’s gRPC tools include the protocol buffer compiler protoc and the special plugin for generating
server and client code from .proto service definitions.

To install gRPC tools, run:

$ python -m pip install grpcio-tools googleapis-common-protos

Run the Demo:
-------------

Now open two terminals with the virtual environment 'grpcDemo' activated.

In one terminal, run the server:
$ python read_fileSection_server.py

In the other terminal, run the client:
$ python read_fileSection_client.py

*NOTE: The 'large' file for testing the program is hardcoded in the code and kept at the location: "./files/stdio.h"

grpc Reference Docs:
--------------
https://grpc.io/docs/guides/index.html
