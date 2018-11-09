from rs import RSCodec
import codecs

CHUNK_SIZE=65536

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

	return rs.decode(enc_chunk,epos_arr).decode('latin-1')

if __name__=="__main__":
	try:
		file=codecs.open("black_panther.png",'r',encoding='latin-1')
	except Exception as e:
		raise e
	rs=RSCodec(51)

	snodes=input("Number of storage nodes: ")
	# corrupt=input("Which node to corrupt: ")

	filew=codecs.open('black_panther_copy.png','w',encoding='latin-1')

	i=1
	while 1:
		chunk=file.read(CHUNK_SIZE)
		if not chunk:
			break

		echunk_length=[0]*snodes
		# Encode the chunks using reed-solomon and divide it for 5 storage nodes
		chunk=bytearray(chunk, 'latin-1')
		echunk_arr,echunk_length,csize_div=encode_chunk(chunk, snodes)

		# Now send these encoded codes to the 5 storage nodes

		# erase data
		# echunk_arr[corrupt]=''

		# Retrieve the original chunk from the chunks received from storage nodes
		retrieved_chunk=decode_chunk(echunk_arr,echunk_length,csize_div,snodes)

		filew.write(retrieved_chunk)
		i+=1

	file.close()
	filew.close()