from __future__ import print_function
from concurrent import futures

import grpc
import time

import pymongo
from pymongo import MongoClient
import json

import classeur_pb2
import classeur_pb2_grpc

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

client = MongoClient("mongodb://localhost:27017/")
db = client["classeur"]
users = db["users"]
sNodeData = db["sNodeData"]
files = db["files"]

class clientHandlerServicer(classeur_pb2_grpc.clientHandlerServicer):

	def __init__(self):
		pass

	def CheckAuthentication(self, request, context):
		query = { "username" : request.username, "password" : request.password }
		print(query)
		queryResult = users.find_one(query)
		print(queryResult)
		if queryResult == None:
			return classeur_pb2.Validity(vailidity=False)
		else:
			return classeur_pb2.Validity(vailidity=True)

	def ListFiles(self, request, context):
		username = request.username
		query = {"username": username}
		queryResult = users.find_one(query, {"_id":0, "files_owned":1})
		data = {'data':queryResult['files_owned']}
		data = json.dumps(data)
		filelist = classeur_pb2.FileList(
			filesOwned=data,fileSizes=0)
		return filelist

	def UploadFile(self, request_iterator, context):
		pass

	def DownloadFile(self, request, context):
		pass

class sNodeHandlerServicer(classeur_pb2_grpc.sNodeHandlerServicer):
	
	def SendFileChunks(self, request_iterator, context):
		pass

	def ReceiveFileChunks(self, request, context):
		pass

	def Heartbeat(self, request, context):
		pass


def serve():
	server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
	classeur_pb2_grpc.add_clientHandlerServicer_to_server(clientHandlerServicer(), server)
	classeur_pb2_grpc.add_sNodeHandlerServicer_to_server(sNodeHandlerServicer(), server)
	server.add_insecure_port('[::]:50051')
	server.start()
	print("hello")
	try:
		while True:
			print("anyone there?")
			time.sleep(_ONE_DAY_IN_SECONDS)
	except KeyboardInterrupt:
		server.stop(0)

if __name__ == '__main__':
	serve()