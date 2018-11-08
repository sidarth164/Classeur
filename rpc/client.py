from __future__ import print_function

import grpc
import getpass
import sys
import json

import classeur_pb2
import classeur_pb2_grpc

MSERVER_PORT = 50051

def checkAuthentication(stub, username, password):
	userCreds = classeur_pb2.UserCredentials(
		username = username, password = password)
	response = stub.CheckAuthentication(userCreds)
	#Blooper Alert! 'vailidity' in place of 'validity' in the proto file
	return response.vailidity

def listFiles(stub, username):
	userToken = classeur_pb2.UserToken(
		username = username)
	data = stub.ListFiles(userToken)
	data = json.loads(data)
	fileList = data["data"]   #it will return an array of filenames
	for files in fileList:
		print(files)
	# return fileList

def uploadFile(stub):
	pass

def downloadFile(stub):
	pass

def run():
	if (len(sys.argv) < 2):
		print("Usage: %s MainServer IP" % sys.argv[0])
		sys.exit(1)

	mserver_host = sys.argv[1]
	mserver_host_port = mserver_host + ":" + str(MSERVER_PORT)

	with grpc.insecure_channel(mserver_host_port) as channel:
		stub = classeur_pb2_grpc.clientHandlerStub(channel)
		#now start using the stub
		username = raw_input("Please enter your username: ")
		password = getpass.getpass('Password: ')

		if checkAuthentication(stub, username, password)==True:
			print("Congratulations! Authentication successful")
			while 1:
				print("Choose any option <Enter the option number>:\n 1. List Files\n 2. Upload File\n 3. Download File\n 4. Exit")
				option = raw_input("Option: ")
				if option == 1:
					listFiles(username)
				elif option == 2:
					uploadFile()
				elif option == 3:
					downloadFile()
				else:
					sys.exit(0)
		else:
			print("Incorrect credentials! Please try again.")
		

if __name__ == "__main__":
	run()