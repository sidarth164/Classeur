from __future__ import print_function

import grpc
import getpass
import sys

import classeur_pb2
import classeur_pb2_grpc

MSERVER_PORT = 50051

def checkAuthentication(stub, username, password):
	userCreds = classeur_pb2.UserCredentials(
		username = username, password = password)
	response = stub.CheckAuthentication(userCreds)
	#Blooper Alert! 'vailidity' in place of 'validity' in the proto file
	return response.vailidity


def run():
	if (len(sys.argv) < 2):
		print("Usage %s MainServer IP" % sys.argv[0])
		sys.exit(0)

	mserver_host = sys.argv[1]
	mserver_host_port = mserver_host + ":" + str(MSERVER_PORT)

	with grpc.insecure_channel(mserver_host_port) as channel:
		stub = classeur_pb2_grpc.clientHandlerStub(channel)
		#now start using the stub
		username = raw_input("Please enter your username: ")
		password = getpass.getpass('Password: ')

		if checkAuthentication(stub, username, password)==True:
			print("Congratulations! Authentication successful")
		else:
			print("Incorrect credentials! Please try again.")
		

if __name__ == "__main__":
	run()