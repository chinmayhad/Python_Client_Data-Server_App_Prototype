import socket #,sys,time,json

HOST = '127.0.0.1'
PORT = 9999

dictionary = {}
try:
	with open("data.txt", "r") as f:
	   for line in f:
		   #print(line)
		   if(line.find("|") == 0):
			   continue;
		   else:
			   chunks = line.split("|",1)
			   dictionary[chunks[0]] = line
except:
	print("data.txt not found. Dictionary is empty.")



#print('Dictionary : ',dictionary,'\n')
print("Server started.")

while True:
	try:
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind((HOST, PORT))
			s.listen()
			conn, addr = s.accept()
			with conn:
				print('A new connection is made by : ', addr,'\n')
				while True:
					data = conn.recv(5024)
					data = data.decode('UTF-8')
					print("client told me to : ", data)

					if(data == '8'):
						print('Received exit command.')
						data = 'Good bye'
						conn.sendall(bytes(data, 'UTF-8'))
						conn.close()
						break;
					else:
						if(data == '1'):
							cName = conn.recv(5024)
							cName = cName.decode('UTF-8')
							print("Searching  for : ", cName)
							if(cName in dictionary):
								conn.sendall(bytes(dictionary[cName], 'UTF-8'))#send it to client
							else:
								conn.sendall(bytes("CNF", 'UTF-8'))  # tell client we don't have it

						elif(data == '2'):
							cName = conn.recv(5024)
							cName = cName.decode('UTF-8')
							if (cName in dictionary):
								# we already have it
								conn.sendall(bytes("CAE", 'UTF-8'))  # send it to client
								continue;
							else:
								conn.sendall(bytes("CNF", 'UTF-8'))  # tell client we can add it

							cData = conn.recv(5024)
							line = cData.decode('UTF-8')
							line = line.lstrip()
							if (line.find("|") == 0):
								print("SKIPPING. BLANK_NAME")
								conn.sendall(bytes("\nERROR : This record could not be saved as name cannot be empty!", 'UTF-8'))  # tell client we did it
							else:
								chunks = line.split("|", 1)
								dictionary[chunks[0]] = line
								conn.sendall(bytes("\nCustomer added succesfully!", 'UTF-8'))  # tell client we did it

						elif(data == '3'):
							cName = conn.recv(5024)
							cName = cName.decode('UTF-8')
							if (cName in dictionary):
								# we can delete it
								del dictionary[cName]
								conn.sendall(bytes("\nCustomer deleted succesfully!", 'UTF-8'))  # tell client we did it
							else:
								conn.sendall(bytes("CNF", 'UTF-8'))  # tell client we don't have it

						elif(data == '4'):
							cData = conn.recv(5024)
							cData = cData.decode('UTF-8')
							cName = cData.split("|")[0]
							cAge = cData.split("|")[1]

							if (cName in dictionary):
								#we can update age
								line = dictionary[cName].split("|")
								line[1] = cAge
								separator = "|"
								newRec = separator.join(line)
								print("new rec : ",newRec)
								dictionary[cName] = newRec
								conn.sendall(bytes("\nCustomer age updated succesfully!", 'UTF-8'))  # tell client we did it
							else:
								print("CNF")
								conn.sendall(bytes("CNF", 'UTF-8'))  # tell client we don't have it
							
						elif(data == '5'):
							cData = conn.recv(5024)
							cData = cData.decode('UTF-8')
							cName = cData.split("|")[0]
							cAddr = cData.split("|")[1]

							if (cName in dictionary):
								# we can update address
								line = dictionary[cName].split("|")
								line[2] = cAddr
								separator = "|"
								newRec = separator.join(line)
								print("new rec : ", newRec)
								dictionary[cName] = newRec
								conn.sendall(bytes("\nCustomer address updated succesfully!", 'UTF-8'))  # tell client we did it
							else:
								print("CNF")
								conn.sendall(bytes("CNF", 'UTF-8'))  # tell client we don't have it

						elif(data == '6'):
							cData = conn.recv(5024)
							cData = cData.decode('UTF-8')
							cName = cData.split("|")[0]
							cPhn = cData.split("|")[1]

							if (cName in dictionary):
								# we can update phone#
								line = dictionary[cName].split("|")
								line[3] = cPhn
								separator = "|"
								newRec = separator.join(line)
								print("new rec : ", newRec)
								dictionary[cName] = newRec
								conn.sendall(bytes("\nCustomer phone# updated succesfully!", 'UTF-8'))  # tell client we did it
							else:
								print("CNF")
								conn.sendall(bytes("CNF", 'UTF-8'))  # tell client we don't have it

						elif (data == '7'):
							#report
							#sendRep = json.dumps(dictionary)
							sendRep = str(sorted(dictionary.values()))
							conn.sendall(bytes(sendRep, 'UTF-8'))#send it to client

						#conn.sendall(bytes(data, 'UTF-8'))
	except:
		print("Client has been terminated forcibly")