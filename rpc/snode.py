from __future__ import print_function

import grpc

import classeur_pb2
import classeur_pb2_grpc

MSERVER_PORT = 50051

def run():
	if (len(sys.argv) < 2):
		print("Usage %s MainServer IP" % sys.argv[0])
		sys.exit(0)

	mserver_host = sys.argv[1]
	mserver_host_port = mserver_host + str(MSERVER_PORT)

	with grpc.insecure_channel(mserver_host_port) as channel:
		stub = classeur_pb2_grpc.sNodeHandlerStub(channel)

		#now start using the stub

if __name__ == "__main__":
	run()