from __future__ import print_function

import grpc
import getpass
import sys
import json
import os
import classeur_pb2
import classeur_pb2_grpc
from hurry.filesize import size
import codecs

MSERVER_PORT = 50051
CHUNK_SIZE = 65536

def checkAuthentication(stub, username, password):
	userCreds = classeur_pb2.UserCredentials(
		username = username, password = password)
	response = stub.CheckAuthentication(userCreds)
	#Blooper Alert! 'vailidity' in place of 'validity' in the proto file
	return response.vailidity

def listFiles(stub, username):
	userToken = classeur_pb2.UserToken(
		username = username)
	result = stub.ListFiles(userToken)
	data = json.loads(result.filesOwned)
	fileList = data["files"]   #it will return an array of filenames
	fileSize = result.filesSizes
	print("You have occupied %s space in total"%size(fileSize))
	i=1
	for file in fileList:
		print("[%s] %s"%(i,file))
		i+=1

def reportSize(stub, username):
	userToken = classeur_pb2.UserToken(
		username = username)
	result = stub.ReportSize(userToken)
	print("You have occupied %s space in total"%size(result.size))

def uploadFile(stub, username):
	filepath = raw_input("Enter the file path: ")
	filename = os.path.basename(filepath)
	try:
		file = codecs.open(filepath,'r', encoding="Latin-1")
	except:
		print("Unable to open file %s"%filepath)
		return
	filesize = os.path.getsize(filepath)
	chunk_count = filesize/CHUNK_SIZE
	if filesize%CHUNK_SIZE:
		chunk_count+=1
	chunk_iterator= fileChunkIterator(file,filename,chunk_count,username)
	ack = stub.UploadFile(chunk_iterator)
	if ack.response == True:
		print("File uploaded successfully")
	else:
		print("Problem in file upload!")
	file.close()

def downloadFile(stub,username):
	filename = raw_input("Enter the filename: ")
	filename = os.path.basename(filename)
	fileName = classeur_pb2.FileName(fileName=filename, userName=username)
	chunk_iter = stub.DownloadFile(fileName)
	if not os.path.exists('downloads'):
	    try:
	        os.makedirs('downloads')
	    except OSError as exc: # Guard against race condition
	        if exc.errno != errno.EEXIST:
	            raise
	file = codecs.open('./downloads/'+filename, 'w', encoding="Latin-1")
	for chunk in chunk_iter:
		if chunk.chunkId==-1:
			print("File not found!")
			os.remove(file.name)
			file.close()
			return
		elif chunk.chunkId==-2:
			print("File Corrupted in cloud! Can not be downloaded!")
			file.close()
			os.remove(file.name)
			return
		ch_data = chunk.chunkData
		file.write(ch_data)
	print("Download Successful!")
	file.close()

def fileChunkIterator(file, filename, chunk_count, username):
	filechunk = classeur_pb2.FileChunks(
		fileName = filename, chunkId = -1, chunkData = None, userName = username)
	for x in xrange(chunk_count):
		chunk = file.read(CHUNK_SIZE)
		filechunk.chunkId=x+1
		filechunk.chunkData=chunk
		yield filechunk

def logOut(stub,username):
	user = classeur_pb2.UserToken(username=username)
	ack = stub.LogOut(user)
	if ack.response:
		print('\nSuccessfully logged out')
		sys.exit(0)
	else:
		print('\nLog out unsuccessful')
		sys.exit(1)

def run():
	if (len(sys.argv) < 2):
		print("Usage: %s MainServer IP" % sys.argv[0])
		sys.exit(1)

	mserver_host = sys.argv[1]
	mserver_host_port = mserver_host + ":" + str(MSERVER_PORT)

	with grpc.insecure_channel(mserver_host_port) as channel:
		stub = classeur_pb2_grpc.clientHandlerStub(channel)
		#now start using the stub

		# username = 'nilesh'
		# success = uploadFile(stub, username)

		username = raw_input("Please enter your username: ")
		password = getpass.getpass('Password: ')

		# TODO: uncomment below code after testing is complete!
		if checkAuthentication(stub, username, password)==True:
			print("Congratulations! Authentication successful")
			while 1:
				try:
					print("Choose any option <Enter the option number>:\n 1. List Files\n 2. Upload File\n 3. Download File\n 4. Total Size\n 5. Exit")
					option = raw_input("Option: ")
					option = int(option)
					if option == 1:
						listFiles(stub,username)
					elif option == 2:
						uploadFile(stub, username)
					elif option == 3:
						downloadFile(stub,username)
					elif option == 4:
						reportSize(stub,username)
						pass
					else:
						logOut(stub,username)
				except:
					logOut(stub,username)
		else:
			print("Incorrect credentials! Please try again.")
		

if __name__ == "__main__":
	run()