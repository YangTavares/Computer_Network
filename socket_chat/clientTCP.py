# import libraries
from socket import *
from threading import Thread # thread
import os

sentence = ""

# Print the received messages from the server independently
def receiveMessage(clientSocket):
	try:
		while 1:
			msgRecebida = clientSocket.recv(1024) 
			print '%s' % (msgRecebida)
	except:
		os._exit(0);

serverName = 'localhost' 
serverPort = 12000 
clientSocket = socket(AF_INET,SOCK_STREAM) 
# Main configuration difference between client and server
clientSocket.connect((serverName, serverPort)) 
sentence = raw_input('Type your nickname: ')
clientSocket.send(sentence) 
# Receives server answer
modifiedSentence = clientSocket.recv(1024) 
print 'The server (\'%s\', %d) responded with: %s' % (serverName, serverPort, modifiedSentence)
t = Thread(target=receiveMessage, args=(clientSocket,))
t.start()
try:
	while 1:
		# Message input to the server
		sentence = raw_input('')
		clientSocket.send(sentence) 
		if sentence == "close()":
			clientSocket.close() 
			break
	# Finish client Socket
except:
	os._exit(0)

