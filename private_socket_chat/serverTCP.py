"""
clients array:
0 - Socket
1 - nickname
2 - active client or not (0 active , -1 disconnected)
3 - client ip
4 - invited to private chat with someone (0 no ,1 yes)
5 - id of who invited/is connected
6 - is it in private chat?(0 - no , 1-yes)
"""


from socket import * # sockets
from threading import Thread # thread
import sys
import os
#store information of the clients
clients = []
#store clients in a private chat
privateChat = []
#thread that receives inputs at the server terminal 
def listClients():
	while 1:
		somethin = raw_input('see list?\n')
		#list all available connections
		if somethin == "list()":
			if len(clients) !=0:
				for i in range(0, len(clients)):
					#checks which clients are connected
					if clients[i][2]==0:
						print "name: %s ip: %s port: 12000"%(clients[i][1],clients[i][3])
			else: 
				print "no such clients logged" 
				
					
					
		elif somethin == "close()":
			for i in range(0, len(clients)):
				if clients[i][2]==0:
					try:
						clients[i][0].send("close")
					except:
						print "Logged out client"
			
			break
	serverSocket.close()	
	os._exit(0)
	sys.exit("Finished Execution")

#parallely manage clients
def clientManager(connectionSocket,t_id):
	#receive the nickname of the client
	good_name = "no"
	while good_name == "no":
		sentence = connectionSocket.recv(1024) 
		good_name = "yes"
		for i in range(0, len(clients)):
			if sentence == clients[i][1]:
				good_name = "no"
				connectionSocket.send("Name already in use, choose another nickname:")
				break
	
	clients[t_id][1] = sentence
	clients[t_id][4] = 0
	clients[t_id][5] = 404
	clients[t_id][6] = 0
	identification = "Cliente %s has logged in." % (sentence)
	print identification
	for i in range(0, len(clients)):
			if clients[i][2]==0:
				clients[i][0].send(identification)
	while 1:	
		try:
			message = connectionSocket.recv(1024) # 
		except:
			os._exit(0)	
		serv_response = "%s sent: %s" % (clients[t_id][1],message)
		#store the id of who sent the message
		clientSender = t_id
		print serv_response
		#change nickname
		if "name(" in message:
			new_name = message.split('name(')
			new_name = new_name[1].split(')')
			new_name = new_name[0]	
			good_name = "yes"
			for i in range(0, len(clients)):
				if new_name == clients[i][1]:
					good_name = "no"
					break
			if good_name == "no":
				clients[t_id][0].send("Name already in use, choose another nickname:")
			else:
				nick_change = "%s changed to: %s"%(clients[t_id][1],new_name)
				clients[t_id][1] = new_name
				print "New nick is: %s"%new_name
				for i in range(0, len(clients)):
					if clients[i][2]==0:
						clients[i][0].send(nick_change)
		#send list of connected users
		elif "list()" in message:
			for i in range(0, len(clients)):
				if clients[i][2]==0:
					send_list = "name: %s ip: %s port: 12000\n"%(clients[i][1],clients[i][3]) 
					clients[t_id][0].send(send_list)

		elif "private(" in message :
			#404 means target not found
			idTarget = 404
			clientTargetName = message.split('private(')
			clientTargetName = clientTargetName[1].split(')')
			clientTargetName = clientTargetName[0]
			#store the id of the user who requested the private chat
			clientInviteSourceId = clientSender
			privateInvitation = "%s invited you to a private chat. Accept(S/N)? " %(clients[clientSender][1])
			#store target id
			for i in range(0, len(clients)):
				if clients[i][1]==clientTargetName:
					idTarget = i
			#sending the message to the found client, if connected
			if idTarget != 404:
				#indicates that the client was requested to a private chat 
				clients[idTarget][4]=1
				#store the id of who sent the request and the one who is going to connect 
				clients[idTarget][5] = clientSender
				clients[clientSender][5] = idTarget
				clients[idTarget][0].send(privateInvitation)
				print clientSender
		#verifies if the next message came from a client who received the request of a private chat	
		elif clients[clientSender][4]==1 and clients[clientSender][6] == 0:
			if message=="N" :
				#return to the status of not invited to private chat
				clients[clientSender][4]=0
				idToReply = clients[clientSender][5]
				#erases the id of who requested the chat in the list
				clients[clientSender][5]=404
				#return message to the "requester"
				inviteReply = "Invite refused by %s" %(clients[clientSender][1])
				#send the message
				clients[idToReply][0].send(inviteReply)
			elif message == "S":
				#store the id of the two clients who are going to enter in a private chat
				client1 = clientSender
				client2 = clients[clientSender][5]
				privateChat.append([client1,client2])
				#change the status to keep track of the private chat
				clients[client1][6] = 1
				clients[client2][6] = 1
				clients[client1][0].send("You are in a private chat with %s" %(clients[client2][1]))
				clients[client2][0].send("You are in a private chat with %s" %(clients[client1][1]))

		elif clients[clientSender][6]==1:
			if message=="sair":
				id1 = clientSender
				id2 = clients[clientSender][5]
				#return to the configurations of not being in a private chat
				clients[id1][6] = 0
				clients[id2][6] = 0
				clients[id1][4] = 0
				clients[id2][4] = 0
				clients[id1][5] = 404
				clients[id2][5] = 404
				clients[id1][0].send("Chat privado encerrado")
				clients[id2][0].send("Chat privado encerrado")
			else :
				#send the private chat messages
				idToSendPrivateMessage = clients[clientSender][5]
				clients[idToSendPrivateMessage][0].send(serv_response)
		#send the message to all users
		else:

			if message == "close":
				clients[t_id][2]=-1
				serv_response = "Client %s left the room."%clients[t_id][1]
				print "Client %s left the room."%clients[t_id][1]
				for i in range(0, len(clients)):
					if clients[i][2]==0 and i!= clientSender:
						clients[i][0].send(serv_response)	
				break
			for i in range(0, len(clients)):
				if clients[i][2]==0 and i!= clientSender and clients[i][6]!=1:
					clients[i][0].send(serv_response)

						
			
	connectionSocket.close()
	

serverName = '' # server ip
serverPort = 12000 # port to be connected
global serverSocket
serverSocket = socket(AF_INET,SOCK_STREAM) # TCP socket creation
try:
	serverSocket.bind((serverName,serverPort)) # bind server ip with its port
except:
	print "Port already in use"
	serverSocket.close()
	os._exit(0)
t = Thread(target=listClients, args=())
t.start()
serverSocket.listen(1) 
print "TCP server waiting connections on port %d ..." % (serverPort)
counter = 0
while 1:
	#indicates if it was invited to a private chat
	flagInvP=0
	#inicializes who invited
	inviterID=0
	#inicializes who is in private chat
	inPrivateChat = 0
	try:
		connectionSocket, addr = serverSocket.accept() 
	except:
		serverSocket.close()
		os._exit(0)
	clients.append([connectionSocket,0,0,addr,flagInvP,inviterID,inPrivateChat])

	t = Thread(target=clientManager, args=(connectionSocket,counter,))
	t.start()
	counter += 1
serverSocket.close() 
