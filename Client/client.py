# client.py
import socket
import os
import hashlib
import sys
from itertools import cycle
import pickle
import json

CHUNK_SIZE=64*1024               #chunk size = 64KB
mserver_host = 'localhost'
mserver_port = 8080
snode_port = 8081

class Files:
    """for persistent storage of file metadata"""
    def __init__(self):
        try:
            pkl_file = open('data.pkl', 'rb')
            self.hash_data = pickle.load(pkl_file)
            pkl_file.close()
        except:
            self.hash_data = {}

    def add_file(self, file, filename):
        """Calculate the hashes and save it in the structure"""
        if filename in self.hash_data:
            print("Updating existing file")

        sha1 = hashlib.sha1()

        hashes = []
        while True:
            data = file.read(CHUNK_SIZE)
            if not data:
                break
            sha1.update(data)
            hashes += [format(sha1.hexdigest())]

        self.hash_data[filename] = hashes
        pkl_file = open('data.pkl', 'wb')
        pickle.dump(self.hash_data, pkl_file)
        pkl_file.close()
        return hashes

    def remove_file(self, filename):
        if filename in self.hash_data:
            del self.hash_data[filename]
            pkl_file = open('data.pkl', 'wb')
            pickle.dump(self.hash_data, pkl_file)
            pkl_file.close()

    def get_files(self):
        return self.hash_data.keys()

    def get_hashes(self, filename):
        if filename in self.hash_data:
            return self.hash_data[filename]
        return None

def upload_chunk(snode, hash, chunk):
    sock = socket.socket()
    sock.connect((snode[0], snode_port))
    upload = "client upload " + hash + " " + snode[1] + "\n" + chunk
    sock.send(upload)
    sock.close()

def get_chunk_snode(hash):
    sock = socket.socket()
    try:
        sock.connect((mserver_host, mserver_port))
    except:
        print("Unable to connect to Main server")
    query={}
    query["source"]="client"
    query["purpose"]="get"
    query["hash"]=hash
    query=json.dumps(query)
    sock.send(query)
    snode = sock.recv(1024)
    if snode.startswith("ERR1"):
        return None;
    return snode

def get_chunk(snode, hash):
    sock = socket.socket()
    try:
        sock.connect((snode, snode_port))
    except:
        print("Unable to connect to Snode")
        return
    sock.send("client get " + hash + "\n")
    reply = sock.recv(1024)

    if reply.startswith("OK"):
        reply = reply[3:]
    else:
        return None

    data = ''
    if reply == "":
        reply = sock.recv(1024)

    while reply:
        data += reply
        reply = sock.recv(1024)
    return data

def allocate_snodes(hashes):
    """ query to the MServer """
    #query = "client allocate " + str(len(hashes))
    # Creating query
    query = {}
    query["source"]="client"
    query["purpose"]="allocate"
    query["chunk_count"]=len(hashes)
    query["chunks"]=[]
    for hash in hashes:
        # query += " " + hash
        query["chunks"].append(hash)
    query = json.dumps(query)

    sock = socket.socket()
    try:
        sock.connect((mserver_host, mserver_port))
    except:
        print("Unable to connect to Main server")
    # sock.send(query + "\n")
    sock.send(query)

    data = ''
    reply = sock.recv(1024)
    while reply:
        data += reply
        reply = sock.recv(1024)
    data = json.loads(data)
    snode_ips = data["snodes"]
    # data = data.split(" ")
    # index = 0
    # snode_ips = []
    # while index < len(data)-1:
    #     snode_ips += [(data[index], data[index+1])]
    #     index += 2
    sock.close()
    return snode_ips

def upload_file():
    filepath = raw_input("Enter file path: ")
    filename = os.path.basename(filepath)
    file = open(filepath, 'rb')
    filesize = os.path.getsize(filepath)
    if filesize == 0:
        print("File size is 0B")
        return

    filechunks = (filesize / CHUNK_SIZE) + 1
    hashes = files.add_file(file, filename)

    try:
        snode_ips = allocate_snodes(hashes)

        # upload chunks to snodes
        file.seek(0, 0)
        chunk = file.read(CHUNK_SIZE)
        index = 0
        while chunk:
            upload_chunk(snode_ips[index], hashes[index], chunk)
            index += 1
            chunk = file.read(CHUNK_SIZE)
        print("Uploaded " + filename)

    except e:
        print("Upload of " + filename + " failed")
        files.remove_file(filename)


def get_file():
    filelist = files.get_files()
    print("Files:-")
    index = 1
    for file in filelist:
        print(str(index) + ". " + file)
        index += 1
    filename = filelist[input("Enter number of the file to download: ") - 1]
    hashes = files.get_hashes(filename)
    data = ''
    for hash in hashes:
        snode = get_chunk_snode(hash)
        if snode is None:
            print("SNode IP record missing for Chunk " + hash)
            return

        chunk = get_chunk(snode, hash)
        if chunk is None:
            print("Chunk " + hash + " not found on SNode " + snode)
            return
        data += chunk

    file = open(filename, 'wb')
    file.write(data)
    print("Downloaded file " + filename)
    file.close()


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage %s MainServerIP" % sys.argv[0])
        sys.exit(0)

    mserver_host = sys.argv[1]

    files = Files()
    print("Connected to Main Server")
    print("1. Upload file\n2. Get file")
    option = input("Select one of the following: ")

    if option == 1:
        upload_file()
    elif option == 2:
        get_file()
    else:
        print("Unrecognised option")
