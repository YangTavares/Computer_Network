# importacao das bibliotecas
from socket import *
from threading import Thread # thread
import sys
import os
import time

sentence = ""
#print messages parallelly from the server
def receiveMessage(clientSocket):
	try:
		while 1:
			msgRecebida = clientSocket.recv(1024) # receive server response
			print '%s' % (msgRecebida)
			if msgRecebida == "close":
				clientSocket.shutdown(socket.SHUT_RDWR) 
				clientSocket.close()
				os._exit(0)
				break
			
	except:
		os._exit(0)	

serverName = 'localhost' # server ip
serverPort = 12000 # connection port
clientSocket = socket(AF_INET,SOCK_STREAM) # TCP socket creation
clientSocket.connect((serverName, serverPort)) # connect the socket to the server
sentence = raw_input('Type your nickname: ')
clientSocket.send(sentence) # send the nickname to the server 
modifiedSentence = clientSocket.recv(1024) # receive server response
print 'The server (\'%s\', %d) responded with: %s' % (serverName, serverPort, modifiedSentence)
t = Thread(target=receiveMessage, args=(clientSocket,))
t.daemon = True
t.start()
while 1:
	try:
		sentence = raw_input('')
		if sentence == "close":
			clientSocket.send("sair") # leave private chat
			time.sleep(2)
			clientSocket.send("close") # leave global chat 
			clientSocket.shutdown(socket.SHUT_RDWR) 
			clientSocket.close()
			os._exit(0)
			#break
		clientSocket.send(sentence) 
	except:
		os._exit(0)	

