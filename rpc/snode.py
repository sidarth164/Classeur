import os
import socket
import sys
import json
import SocketServer

import grpc
import classeur_pb2
import classeur_pb2_grpc

HOST = ""
PORT = "8081"
MSERVER_PORT = 50051
mserver_host = ""

size = 4*1024*1024
snode_port = 8081
expected_tokens = []

def upload_chunk(snode, hash, chunk):
	sock = socket.socket()
	sock.connect((snode[0], snode_port))
	upload={}
	upload["source"]="snode"
	upload["purpose"]="upload"
	upload["hash"]="hash"
	upload["token"]=snode[1]
	upload["chunk"]=chunk
	# upload = "snode upload " + hash + " " + snode[1] + "\n" + chunk
	sock.send(upload + "\n")
	sock.close()

class SNodeHandler(SocketServer.StreamRequestHandler):

	def handle(self):
		data = self.rfile.readline().strip()
		# data = data + self.rfile.read(1024)
		# data = self.rfile.read(1024)
		# while data:
					# file.write(data)
			# data = data + self.rfile.read(1024)
		# print data
		repsonse = json.loads(data)
		print "{} wrote:".format(self.client_address[0])
		print response

		# if data.startswith("client"):
		if repsonse["source"]=="mserver":
			# if data.startswith("upload", 7):
			if repsonse["purpose"]=="upload":
				# hash = data.split(" ")[2]
				folderName = response["username"] + "/" + response["filename"]
				if not os.path.exists(folderName):
					os.makedirs(folderName)
				filepath = "./" + folderName + "/" + response["chunk_id"]
				file = open(filepath, 'wb')
				# file.write(response["chunk"])
				data = self.rfile.read(1024)
				while data:
					file.write(data)
					data = self.rfile.read(1024)

			elif response["purpose"] == "testing":
				print(response["message"])


				# # Send the uploaded ack to MServer
				# sock = socket.socket()
				# sock.connect((mserver_host, mserver_port))
				# file.close()
				# filesize = os.path.getsize("./storage/" + hash)

				# query={}
				# query["source"]="snode"
				# query["purpose"]="uploaded"
				# query["hash"]=hash
				# query["filesize"]=filesize
				# query=json.dumps(query)

				# sock.send(query + "\n")

				# # sock.send("snode uploaded " + hash + " " + str(filesize) + "\n")
				# file = open("./storage/" + hash, 'r')
				# chunk = file.read()
				# data = ''
				# reply = sock.recv(1024)         #this reply contains the list of snodes where the given chunk can be uploaded
				# while reply:
				#     data += reply
				#     reply = sock.recv(1024)
				# sock.close()

				# #The part below needs to be modified for granular and random distribution of chunks to other snodes

				# # Upload duplicated to other SNodes
				# data = data.split(" ")
				# index = 0
				# snode_ips = []
				# while index < len(data):
				#     snode_ips += [(data[index], data[index+1])]
				#     index += 2

				# for snode in snode_ips:
				#     upload_chunk(snode, hash, chunk)
				# return

			# elif data.startswith("get", 7):
			elif repsonse["purpose"]=="get":
				hash = response["hash"]
				# hash = data.split(" ")[2]
				try:
					file = open("./storage/" + hash, 'r')
					data = file.read()
					self.wfile.write("OK " + data)
					file.close()
				except:
					self.wfile.write("ERR1")
				return

			else:
				print("Wrong Request")

		# elif data.startswith("mserver"):
		elif repsonse["source"]=="mserver":
			# if data.startswith("expect", 8):
			if response["purpose"]=="expect":
				token=response["token"]
				# token = data.split(" ")[2]
				expected_tokens.append(token)

		else:
			print("Wrong Request")


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
	pass

def addSNode(stub):
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("8.8.8.8", 80))
	HOST = s.getsockname()[0]
	s.close()
	sNodeId = raw_input("Please enter the desired Id for this storage node: ")
	sNodeDetails = classeur_pb2.SNodeDetails(
		ip = HOST, port = PORT, id = sNodeId)
	ack = stub.AddSNode(sNodeDetails)
	if ack.response == True:
		print("SNode %s:%s added successfully"%(HOST,PORT))
	else:
		print("Unable to add the SNode")

def run():
	if (len(sys.argv) < 2):
		print("Usage: %s MainServer IP" % sys.argv[0])
		sys.exit(1)

	mserver_host = sys.argv[1]
	mserver_host_port = mserver_host + ":" + str(MSERVER_PORT)

	with grpc.insecure_channel(mserver_host_port) as channel:
		stub = classeur_pb2_grpc.sNodeHandlerStub(channel)
		addSNode(stub)

def serverInstance():

	mserver_port = MSERVER_PORT
	try:
		server = ThreadedTCPServer((HOST, PORT), SNodeHandler)
		print "you reached till here!"
		server.serve_forever()
	except:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((mserver_host, mserver_port))

		query={}
		query["source"]="snode"
		query["purpose"]="drop"
		query["storageSpace"]=size
		query=json.dumps(query)

		sock.send(query + "\n")
		# sock.send("snode drop " + str(size) + "\n")
		sock.close()


if __name__ == "__main__":
	run()
	serverInstance()
# if (len(sys.argv) < 2):
#         print("Usage %s MainServerIP" % sys.argv[0])
#         sys.exit(0)

	# mserver_host = sys.argv[1]
	# mserver_port = 8080

	# sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	# sock.connect((mserver_host, mserver_port))
	# print "Connected to mserver"
	# query={}
	# query["source"]="snode"
	# query["purpose"]="add"
	# query["storageSpace"]=size
	# query=json.dumps(query)

	# sock.send(query + "\n")
	# print "query sent"
	# sock.send("snode add " + str(size) + "\n")
	# received = sock.recv(8)

	# print("received: %s" % received)
	# if "added" not in received:
	#     sys.exit(1)
	# sock.close()