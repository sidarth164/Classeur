from __future__ import print_function
from concurrent import futures

import grpc
import time
import socket

import pymongo
from pymongo import MongoClient
import json

import classeur_pb2
import classeur_pb2_grpc

from rs import RSCodec

_ONE_DAY_IN_SECONDS = 60 * 60 * 24
rs = RSCodec(51)

# Comment below global variables
# echunk_arr=['']*5
# echunk_length=[]
# csize_div=[]

client = MongoClient("mongodb://localhost:27017/")
db = client["classeur"]
users = db["users"]
sNodeBinding = db["sNodeBinding"]  # {"id": id, "ip":ip, "ACTIVE"=True}
files = db["files"]

# Reed-Solomon Encoding-Decoding Functions
def encode_chunk(chunk,n):
	enc_chunk=rs.encode(chunk).decode('latin-1')
	# Uncomment below line
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
	print(len(echunk_arr))
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

	try:
		decoded=rs.decode(enc_chunk,epos_arr).decode('latin-1')
		print('decode successful')
	except:
		print('decode failure')
		decoded=None

	return decoded

def upload_chunk(snode, chunk,username,chunk_id,filename):
    sock = socket.socket()
    sock.connect((snode, snode_port))
    upload={}
    upload["source"]="mserver" #change this to mserver here and in snode.py
    upload["purpose"]="upload"
    upload["username"]=username
    upload["chunk_id"]=chunk_id
    upload["filename"]=filename
    upload=json.dumps(upload)
    sock.send(upload + "\n" + chunk)
    sock.close()

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
		filename = ''
		username = ''
		for filechunk in request_iterator:
			filename = filechunk.fileName
			username = filechunk.userName
			chunk_id = filechunk.chunkId
			chunk_data = filechunk.chunkData
			tot_size += len(chunk_data)
			snodes = 5
			snode_list = [y+1 for y in xrange(snodes)]
			print(type(chunk_data))
			chunk_data = bytearray(chunk_data, 'latin-1')
			echunk_arr,echunk_length,csize_div=encode_chunk(chunk_data, snodes)
			for id in snode_list:
				query = {"id":id}
				queryResult = users.find_one(query)
				ip = queryResult['ip']
				chunk = echunk_arr[id-1]
				upload_chunk(ip,chunk,username,chunk_id,filename)

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
				users.update_one(
					{'username':username},
					{'$push':{'files_owned':filename},
					'$inc':{'total_size':tot_size}})
			else:
				chunk={'size':echunk_length,'div':csize_div}
				files.update_one(
					{'name':filename,'user':username},
					{'$set':
						{'chunk.'+str(chunk_id):chunk, 'size':tot_size, 'chunk_count':chunk_id, 'snodes':snode_list}
					})

			print(echunk_length)
			print(csize_div)


		ack = classeur_pb2.Acknowledgement(response=True)
		return ack

	def DownloadFile(self, request, context):
		# retrieved_chunk=decode_chunk(echunk_arr,echunk_length,csize_div,snodes)

		filename = request.fileName
		username = request.userName
		snodes = 5
		snode_list = [y+1 for y in xrange(snodes)]
		file_data = files.find_one({'name':filename,'user':username})
		file_chunk = classeur_pb2.FileChunks(
			fileName = filename, chunkId=-1, chunkData=None, userName=username)
		if not file_data:
			print('File %s not found!'%filename)
			for x in range(1):
				yield file_chunk
		else:
			for chunk_id in file_data["chunk"]:
				
				''' 
				Collect the chunks from all the snodes. If a node is down assume its chunk as null string
				echunk_arr => list of chunks
				echunk_length
				echunk_csize_div
				'''
				echunk_length=file_data["chunk"][chunk_id]['size']
				csize_div=file_data["chunk"][chunk_id]['div']
				retrieved_chunk=decode_chunk(echunk_arr,echunk_length,csize_div,snodes)
				if not retrieved_chunk:
					file_chunk.chunkId=-2
					yield file_chunk
				else:
					file_chunk.chunkData=retrieved_chunk
					file_chunk.chunkId=int(chunk_id)
					yield file_chunk


class sNodeHandlerServicer(classeur_pb2_grpc.sNodeHandlerServicer):
	
	def SendFileChunks(self, request_iterator, context):
		pass

	def AddSNode(self, request, context):
		ip = request.ip
		port = request.port
		SNodeId = request.id
		query = {"id":SNodeId, "ip":ip, "port":port, "ACTIVE":True}
		print(query)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((ip, port))
		query = {}
		query["source"]="mserver"
		query["purpose"]="testing"
		query["message"]="yo bro wassup?"
		query = json.dumps(query)
		sock.send(query + "\n")
		sock.close()
		x=sNodeBinding.insert_one(query)
		if x == None:
			ack = classeur_pb2.Acknowledgement(response = False)
			return ack
		else:
			ack = classeur_pb2.Acknowledgement(response = True)
			return ack

	# def ReceiveFileChunks(self, request, context):
	# 	pass

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