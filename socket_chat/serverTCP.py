
# Import librarys
from socket import * # sockets
from threading import Thread # thread
import os
# Store information about connected clients
clients = []
# Thread to receive inputs from the server terminal
def listClients(serverSocket):
	while 1:
		somethin = raw_input('Type "list()" to list users or "close()" to close the server:\n')
		# List all connections
		if somethin == "list()":
			for i in range(0, len(clients)):
				# Check which clients are connected
				if clients[i][2]==0:
					print "name: %s ip: %s port: 12000"%(clients[i][1],clients[i][3]) 
		# Finish
		#Ainda precisa terminar porque o programa fica preso no "ServerSocket.accept()" la em baixo
		elif somethin == "close()":
			for i in range(0, len(clients)):
				if clients[i][2]==0:
					clients[i][0].close()
			break
	serverSocket.close()
	os._exit(0)

# Thread to manage each client separetly
def clientManager(connectionSocket,t_id):
	try:
		# Receive the clients nick
		sentence = connectionSocket.recv(1024) 
		# Nick stays at position 1 
		clients[t_id][1] = sentence
		identification = "Cliente %s has logged in." % (sentence)
		print identification
		connectionSocket.send(identification) 
	
		while 1:	
			message = connectionSocket.recv(1024) 
			serv_response = "%s sent: %s" % (clients[t_id][1],message)
			print "%s sent: %s"%(clients[t_id][1],message)
			# Change nickname
			if "name(" in message:
				new_name = message.split('name(')
				new_name = new_name[1].split(')')
				new_name = new_name[0]	
				nick_change = "%s changed to: %s"%(clients[t_id][1],new_name)
				clients[t_id][1] = new_name
				print "New nick is: %s"%new_name
				for i in range(0, len(clients)):
					if clients[i][2]==0:
						clients[i][0].send(nick_change)
			# Send list of connected clients
			elif "list()" in message:
				for i in range(0, len(clients)):
					if clients[i][2]==0:
						send_list = "name: %s ip: %s port: 12000\n"%(clients[i][1],clients[i][3]) 
						clients[t_id][0].send(send_list)
			#Send the message to all clients for a global chat
			else:
				for i in range(0, len(clients)):
					if clients[i][2]==0 and t_id!=i:
						clients[i][0].send(serv_response)
				if message == "close()":
					clients[t_id][2]=-1
					print "Client %s left the room."%clients[t_id][1]
					break
		connectionSocket.close() # Finishes the socket connection
	except:
		os._exit(0)
	

# Server IP
serverName = '' 
# Server port to connect
serverPort = 12000 
# TCP protocol
serverSocket = socket(AF_INET,SOCK_STREAM) 
# Bind the Server IP with its port
serverSocket.bind((serverName,serverPort)) 
# Ready to receive connections
serverSocket.listen(1) 
print "TCP Server waiting connections at port %d ..." % (serverPort)
t = Thread(target=listClients, args=(serverSocket,))
t.start()
counter = 0
try:
	while 1:
		# Accept clients connections
		connectionSocket, addr = serverSocket.accept()
		# Information order: Socket object, client Nick, Is connected, IP
		clients.append([connectionSocket,0,0,addr])
		# Call thread to manage client
		t = Thread(target=clientManager, args=(connectionSocket,counter,))
		t.start()
		counter += 1
	# Finish server Socket
	serverSocket.close()
except:
	os._exit(0)
