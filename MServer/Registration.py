import pymongo
from pymongo import MongoClient
from getpass import getpass

client = MongoClient('localhost', 27017)
db = client.classeur
users = db.users

if __name__=="__main__":
	print("Welcome to Classeur User Registration!\nPlease answer the following questions for successful registration\n")

	while 1:
		username = input("Username: ")
		password = getpass("Password: ")
		exists = users.find_one({'username':username})
		if exists==None:
			break
		else:
			print("This username is already in use!\nPlease choose again\n")

	users.inser_one({'username':username, 'password':password, 'files_owned':[], 'total_size':0})
	print('Registration Successful!')