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
	enc_chunk=rs.encode(chunk).decode('Latin-1')
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

	# decoded=rs.decode(enc_chunk,epos_arr).decode('Latin-1')
	try:
		decoded=rs.decode(enc_chunk,epos_arr).decode('Latin-1')
		print('decode successful')
	except:
		print('decode failure')
		raise
		decoded=None

	return decoded

def upload_chunk(snode,snode_port,chunk,username,chunk_id,filename):
	sock = socket.socket()
	sock.connect((snode, snode_port))
	upload={}
	upload["source"]="mserver" #change this to mserver here and in snode.py
	upload["purpose"]="upload"
	upload["username"]=username
	upload["chunk_id"]=chunk_id
	upload["filename"]=filename
	upload=json.dumps(upload)
	sock.send(upload + "\n" + chunk.encode('Latin-1'))
	sock.close()

def download_chunk(snode,snode_port,username,chunk_id,filename):
	sock = socket.socket()
	try:
		sock.connect((snode,snode_port))
	except:
		return ''
	download={}
	download["source"]="mserver"
	download["purpose"]="get"
	download["username"]=username
	download["chunk_id"]=chunk_id
	download["filename"]=filename
	download=json.dumps(download)
	sock.send(download+'\n')
	
	reply = sock.recv(1024)
	if reply.startswith("OK"):
		reply = reply[3:]
	else:
		return ''
	data = ''
	if reply == "":
		reply = sock.recv(1024)
	while reply:
		data += reply
		reply = sock.recv(1024)

	sock.close()
	return data.decode('Latin-1')

# Client Service Handler
class clientHandlerServicer(classeur_pb2_grpc.clientHandlerServicer):

	def __init__(self):
		pass


	def CheckAuthentication(self, request, context):
		queryResult = users.find_one({"username":request.username,"password":request.password,"logged_in":False})
		print(queryResult)
		if queryResult == None:
			return classeur_pb2.Validity(vailidity=False)
		else:
			users.update_one({"username":request.username},{'$set': {'logged_in':True}})
			return classeur_pb2.Validity(vailidity=True)

	def LogOut(self, request, context):
		username = request.username
		try:
			users.update_one({"username":username},{"$set":{"logged_in":False}})
			return classeur_pb2.Acknowledgement(response=True)
		except:
			return classeur_pb2.Acknowledgement(response=False)

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
		snodes = 0
		snode_list = []
		snode_iter = sNodeBinding.find({"ACTIVE":True})
		for snode in snode_iter:
			snode_list.append(snode["id"])
			snodes+=1
		for filechunk in request_iterator:
			filename = filechunk.fileName
			username = filechunk.userName
			chunk_id = filechunk.chunkId
			chunk_data = filechunk.chunkData
			tot_size += len(chunk_data)
			print(chunk_id)
			chunk_data = bytearray(chunk_data, 'Latin-1')
			echunk_arr,echunk_length,csize_div=encode_chunk(chunk_data, snodes)
			x=0
			for id in snode_list:
				query = {"id":id}
				queryResult = sNodeBinding.find_one(query)
				ip = queryResult['ip']
				port = queryResult['port']
				chunk = echunk_arr[x]
				upload_chunk(ip,port,chunk,username,chunk_id,filename)
				x+=1

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
				file_old = file
				files.delete_one({"name":filename,"user":username})
				file={}
				file["name"]=filename
				file["user"]=username
				file["size"]=tot_size
				file["chunk_count"]=chunk_id
				file["snodes"]=snode_list
				file["chunk"]={}
				for chunkid_old in file_old["chunk"]:
					file["chunk"][chunkid_old]=file_old["chunk"][chunkid_old]
				file["chunk"][str(chunk_id)]={'size':echunk_length,'div':csize_div}
				files.insert_one(file)

			print(echunk_length)
			print(csize_div)


		ack = classeur_pb2.Acknowledgement(response=True)
		return ack

	def DownloadFile(self, request, context):
		# retrieved_chunk=decode_chunk(echunk_arr,echunk_length,csize_div,snodes)

		filename = request.fileName
		username = request.userName
		# snodes = 5
		# snode_list = [y+1 for y in xrange(snodes)]
		file_data = files.find_one({'name':filename,'user':username})
		snode_list = file_data["snodes"]
		snodes = len(snode_list)
		file_chunk = classeur_pb2.FileChunks(
			fileName = filename, chunkId=-1, chunkData=None, userName=username)
		if not file_data:
			print('File %s not found!'%filename)
			for x in range(1):
				yield file_chunk
		else:
			for ch_id in xrange(file_data["chunk_count"]):
				echunk_arr=[]
				chunk_id=str(ch_id+1)
				for snode in snode_list:
					query = {"id":snode}
					queryResult = sNodeBinding.find_one(query)
					ip = queryResult['ip']
					port = queryResult['port']
					active = queryResult['ACTIVE']
					if active:
						echunk = download_chunk(ip,port,username,chunk_id,filename)
						echunk = bytearray(echunk, 'Latin-1')
						if not echunk:
							print('echunk is None')
						elif echunk=='':
							print('echunk is ""')
						echunk_arr.append(echunk)
					else:
						echunk_arr.append('')
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
		# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# sock.connect((ip, port))
		# query = {}
		# query["source"]="mserver"
		# query["purpose"]="testing"
		# query["message"]="yo bro wassup?"
		# query = json.dumps(query)
		# sock.send(query + "\n")
		# sock.close()
		x=sNodeBinding.find_one({"id":SNodeId})
		if x == None:
			sNodeBinding.insert_one(query)
			ack = classeur_pb2.Acknowledgement(response = True)
			return ack
		else:
			sNodeBinding.update_one(
				{"id":SNodeId},
				{"$set":query})
			ack = classeur_pb2.Acknowledgement(response = True)
			return ack

	# def ReceiveFileChunks(self, request, context):
	# 	pass

	def DeleteSNode(self, request, context):
		snode_id = request.id
		snode = sNodeBinding.find_one({"id":snode_id})
		if not snode:
			ack = classeur_pb2.Acknowledgement(response = False)
			return ack
		else:
			sNodeBinding.update_one(
				{"id":snode_id},
				{"$set": {"ACTIVE":False}})
			ack = classeur_pb2.Acknowledgement(response = True)
			return ack

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
		# remove all the snodes: make them inactive
		snode_list = sNodeBinding.update_many({"ACTIVE":True}, {"$set":{"ACTIVE":False}})
		users.update_many({"logged_in":True},{"$set":{"logged_in":False}})
		server.stop(0)

if __name__ == '__main__':
	serve()