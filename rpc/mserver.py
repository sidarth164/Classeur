from __future__ import print_function
from concurrent import futures

import grpc
import time

import pymongo
from pymongo import MongoClient
import json

import classeur_pb2
import classeur_pb2_grpc

from rs import RSCodec

CHUNK_SIZE=65536
_ONE_DAY_IN_SECONDS = 60 * 60 * 24
rs = RSCodec(51)

client = MongoClient("mongodb://localhost:27017/")
db = client["classeur"]
users = db["users"]
sNodeData = db["sNodeData"]
files = db["files"]

# Reed-Solomon Encoding-Decoding Functions
def encode_chunk(chunk,n):
	enc_chunk=rs.encode(chunk)
	echunk_arr=['']*n
	echunk_length=[0]*n
	csize=255/n
	csize_div=[csize]*n
	crem=255%n
	for x in xrange(crem):
		csize_div[x]+=1
	for i in range(0,len(enc_chunk),255):
		j=0
		for x in xrange(n):
			echunk_arr[x]+=enc_chunk[i+j:i+j+csize_div[x]]
			j+=csize_div[x]
	for x in xrange(n):
		echunk_length[x]=len(echunk_arr[x])
	return echunk_arr,echunk_length,csize_div

def decode_chunk(echunk_arr,echunk_length,csize_div,n):
	epos=einc=node=0
	for x in xrange(n):
		if echunk_arr[x]=='':
			echunk_arr[x]=''.join(['0' for y in xrange(echunk_length[x])])
			for y in xrange(x):
				epos+=csize_div[x]
			einc=csize_div[x]
			node=x
	epos_arr=[]
	i=0
	e=0
	inc=[0]*n
	enc_chunk=''
	for i in range(0,len(echunk_arr[0]),csize_div[0]):
		if einc:
			if(inc[node]+csize_div[node]<len(echunk_arr[node])):
				epos_arr+=[y for y in range(e+epos,e+epos+einc)]
			else:
				epos_arr+=[y for y in range(e+epos,e+epos+len(echunk_arr[node])-inc[node])]
		
		for x in range(0,n):
			enc_chunk+=echunk_arr[x][inc[x]:inc[x]+csize_div[x]]
			inc[x]+=csize_div[x]
		e+=255

	return rs.decode(enc_chunk,epos_arr)

# Client Service Handler
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
		queryResult = users.find_one(query)
		data = {'files':queryResult['files_owned']}
		data = json.dumps(data)
		filelist = classeur_pb2.FileList(
			filesOwned=data,filesSizes=queryResult['total_size'])
		return filelist

	def ReportSize(self, request,context):
		username = request.username
		user = users.find_one({'username':username})
		filesize = classeur_pb2.FileSize(
			size=user['total_size'])
		return filesize

	def UploadFile(self, request_iterator, context):
		tot_size = 0
		for filechunk in request_iterator:
			filename = filechunk.fileName
			username = filechunk.userName
			chunk_id = filechunk.chunkId
			chunk_data = filechunk.chunkData
			tot_size += len(chunk_data)
			snodes = 5
			snode_list = [y+1 for y in xrange(snodes)]
			print(type(chunk_data))
			chunk_data = bytearray(chunk_data, 'utf-8')
			echunk_arr,echunk_length,csize_div=encode_chunk(chunk_data, snodes)
			
			'''
				send echunk_arr elements to their respective snodes
			'''

			file = files.find_one({"name":filename,"user":username})
			if not file:
				file={}
				file["name"]=filename
				file["user"]=username
				file["size"]=tot_size
				file["chunk_count"]=chunk_id
				file["snodes"]=snode_list
				file["chunk"]={}
				file["chunk"][str(chunk_id)]={'size':echunk_length,'div':csize_div}
				files.insert_one(file)
			else:
				chunk={'size':echunk_length,'div':csize_div}
				files.update_one(
					{'name':filename,'user':username},
					{'$set':
						{'chunk.'+str(chunk_id):chunk, 'size':tot_size, 'chunk_count':chunk_id, 'snodes':snode_list}
					})

			print(echunk_length)
			print(csize_div)

		users.update_one(
			{'username':username},
			{'$push':{'files_owned':filename},
			'$inc':{'total_size':tot_size}})

		ack = classeur_pb2.Acknowledgement(response=True)
		return ack

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