import SocketServer
import socket
import json
from uuid import uuid4

snode_port = 8081

class SNode:

    def __init__(self, max_size):
        self.max_size = max_size
        self.curr_size = 0

class SNodeList:

    def __init__(self):
        self.snodes = {}
        self.index = -1

    def add_node(self, addr, size):
        if addr in self.snodes:
            print("The SNode " + addr + " is already present")
            return

        self.snodes[addr] = SNode(size)

    def delete_node(self, addr):
        if addr in self.snodes:
            del self.snodes[addr]
            if self.index == len(self.snodes):
                self.index = (self.index + 1) % len(self.snodes)
        else:
            print("SNode " + addr + " not found in DB")

    def get_node(self):
        assert (self.index < len(self.snodes)), "Index out of range"
        node = self.snodes.keys()[self.index]
        self.index = (self.index + 1) % len(self.snodes)
        return [node]

    def increment_size(self, addr, incr):
        if addr in self.snodes:
            self.snodes[addr].curr_size += incr

    def get_length(self):
        return len(self.snodes)


class StorageData():

    def __init__(self):
        self.storageMaps = {}

    def allocate_node(self, hash, avoid=None):
        node = snodeList.get_node()
        if (avoid is not None) and snodeList.get_length() > 1:
            while avoid in node:
                node = snodeList.get_node()

        # store node list for each chunk and if the entry is valid of not
        if hash in self.storageMaps:
            self.storageMaps[hash] += node
        else:
            self.storageMaps[hash] = node
        token = str(uuid4())
        return (node[0], token)

    def get_node(self, hash):
        if hash in self.storageMaps:
            return self.storageMaps[hash][0]
        return None

    def remove_node(self, addr):
        for hash in self.storageMaps:
            if addr in self.storageMaps[hash]:
                self.storageMaps[hash].remove(addr)

class MServerHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        data = self.rfile.readline().strip()
        request = json.loads(data)
        print "{} wrote:".format(self.client_address[0])
        print request

        # if data.startswith("snode"):
        if request["source"]=="snode":
            # if data.startswith("add", 6):
            if request["purpose"]=="add":
                self.wfile.write("added")
                size = [int(s) for s in data.split() if s.isdigit()][0]
                snodeList.add_node(self.client_address[0], size)
                print("SNode {} added".format(self.client_address[0]))
                return

            # elif data.startswith("drop", 6):
            elif request["purpose"]=="drop":
                size = [int(s) for s in data.split() if s.isdigit()][0]
                snodeList.delete_node(self.client_address[0])
                storageData.remove_node(self.client_address[0])
                print("SNode {} dropped".format(self.client_address[0]))

            # elif data.startswith("uploaded", 6):
            elif request["purpose"]=="uploaded":
                chunk_size = [int(s) for s in data.split() if s.isdigit()][0]
                snodeList.increment_size(self.client_address[0], chunk_size)
                hash = data.split()[2]
                addr, token = storageData.allocate_node(hash, avoid=self.client_address[0])
                result = "{} ".format(addr) + token
                self.wfile.write(result)
                sock = socket.socket()
                sock.connect((addr, snode_port))
                
                query = {}
                query["source"] = "mserver"
                query["purpose"] = "expect"
                query["token"] = token
                query = json.dumps(query)
                sock.send(query)
                # sock.send("mserver expect " + token + "\n")
                sock.close()

            # elif data.startswith("duplicated", 6):
            elif request["purpose"]=="duplicated":
                chunk_size = [int(s) for s in data.split() if s.isdigit()][0]
                snodeList.increment_size(self.client_address[0], chunk_size)

            else:
                print("Wrong Request")

        # elif data.startswith("client"):
        elif request["source"]=="client":
            if request["purpose"]=="allocate":
            # if data.startswith("allocate", 7):
                numChunks = request["numChunks"]
                # numChunks = [int(s) for s in data.split() if s.isdigit()][0]
                hashes = request["hashes"]
                # hashes = data.split(" ")[3:]
                result = ""
                for hash in hashes:
                    addr, token = storageData.allocate_node(hash)
                    result = result + "{} ".format(addr) + token + " "
                    sock = socket.socket()
                    sock.connect((addr,snode_port))

                    query = {}
                    query["source"] = "mserver"
                    query["purpose"] = "expect"
                    query["token"] = token
                    query = json.dumps(query)
                    sock.send(query)
                    # sock.send("mserver expect " + token + "\n")
                    sock.close()
                self.wfile.write(result)
                return

            # elif data.startswith("get", 7):
            elif request["purpose"]=="get":
                hash = request["hash"]
                # hash = data.split(" ")[2]
                result = "{}".format(storageData.get_node(hash))
                if result:
                    self.wfile.write(result)
                else:
                    self.wfile.write("ERR1")
                return

            else:
                print("Wrong Request")

        else:
            print("Wrong Request")

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    HOST, PORT = s.getsockname()[0], 8080
    s.close()


    server = ThreadedTCPServer((HOST, PORT), MServerHandler)
    snodeList = SNodeList()
    storageData = StorageData()

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
