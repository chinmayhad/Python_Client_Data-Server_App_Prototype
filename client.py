import socket,sys

HOST = '127.0.0.1'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    while True:
        print("\nSelect: \n")
        cInput = input ("1. Find customer \n2. Add customer \n3. Delete customer \n4. Update customer age \n5. Update customer address \n6. Update customer phone \n7. Print Report \n8: Exit\n\n")

        if (cInput != '8'):

            if (cInput == '1'):
                s.send(bytes(cInput, 'UTF-8'))#sending the choice of option
                cName = input("\nEnter customer's name you want to search : ")
                s.send(bytes(cName, 'UTF-8'))  # sending the name to search in dict
                cData = s.recv(5024)
                cData = cData.decode('UTF-8')
                if(cData == 'CNF'):
                    print("\nCustomer not fund!")
                else:
                    print(cData)

            elif (cInput == '2'):
                s.send(bytes(cInput, 'UTF-8'))#sending the choice of option
                cName = input("\nEnter new customer's name : ").strip()
                while(cName.isspace() or len(cName)<1 or cName.isnumeric()):
                    cName = input("\nName cannot be empty or a number. Enter new customer's name : ").strip()
                s.send(bytes(cName, 'UTF-8'))  # sending the name to see if already exists
                cResp = s.recv(5024)
                cResp = cResp.decode('UTF-8')
                if(cResp == 'CAE'):
                    print("\nCustomer Already Exists!")
                else:

                    while True:
                        try:
                            cAge = (input("\nEnter Age. You can press 'Enter' to skip this field. ").strip())
                            if len(cAge) != 0 and int(cAge) < 0:
                                raise ValueError
                        except ValueError:
                            print("\nNot a valid age. Try again.")
                            continue
                        else:
                            break

                    cAdrs = input("\nEnter address. You can press 'Enter' to skip this field. ").strip()

                    cPhn = str(input("\nEnter Phone#. You can press 'Enter' to skip this field. "))

                    cData = cName+"|"+cAge+"|"+cAdrs+"|"+cPhn
                    s.send(bytes(cData, 'UTF-8'))  # sending data to add
                    cMsg = s.recv(5024)
                    cMsg = cMsg.decode('UTF-8')
                    print(cMsg)

            elif (cInput == '3'):
                s.send(bytes(cInput, 'UTF-8'))#sending the choice of option
                cName = input("\nEnter customer's name that you want to delete : ").strip()
                s.send(bytes(cName, 'UTF-8'))  # sending the name to see if it exists
                cResp = s.recv(5024)
                cResp = cResp.decode('UTF-8')
                if (cResp == 'CNF'):
                    print("\nCustomer not found!")
                else:
                    print(cResp)

            elif (cInput == '4'):
                s.send(bytes(cInput, 'UTF-8'))#sending the choice of option
                cName = input("\nEnter customer's name whose age you want to update : ").strip()
                while True:
                    try:
                        cAge = (input("\nEnter Age. You can press 'Enter' to skip this field. ").strip())
                        if len(cAge) != 0 and int(cAge) < 0:
                            raise ValueError
                    except ValueError:
                        print("\nNot a valid age. Try again.")
                        continue
                    else:
                        break

                cAge = str(cAge)
                cData = cName + "|" + cAge
                s.send(bytes(cData, 'UTF-8'))  # sending data to update age
                cResp = s.recv(5024)
                cResp = cResp.decode('UTF-8')

                if (cResp == 'CNF'):
                    print("\nCustomer not found!")
                else:
                    print(cResp)

            elif (cInput == '5'):
                s.send(bytes(cInput, 'UTF-8'))#sending the choice of option
                cName = input("\nEnter customer's name whose address you want to update : ").strip()
                cAddr = input("\nEnter customer's address : ").strip()
                cData = cName + "|" + cAddr
                s.send(bytes(cData, 'UTF-8'))  # sending data to update address
                cResp = s.recv(5024)
                cResp = cResp.decode('UTF-8')

                if (cResp == 'CNF'):
                    print("Customer not found!")
                else:
                    print(cResp)

            elif (cInput == '6'):
                s.send(bytes(cInput, 'UTF-8'))#sending the choice of option
                cName = input("\nEnter customer's name whose phone# you want to update : ").strip()
                cPhn = input("\nEnter customer's phone# : ")
                cData = cName + "|" + cPhn
                s.send(bytes(cData, 'UTF-8'))  # sending data to update phone#
                cResp = s.recv(5024)
                cResp = cResp.decode('UTF-8')

                if (cResp == 'CNF'):
                    print("\nCustomer not found!")
                else:
                    print(cResp)

            elif (cInput == '7'):
                s.send(bytes(cInput, 'UTF-8'))#sending the choice of option

                cResp = s.recv(5024)
                cResp = cResp.decode('UTF-8')

                cResp = cResp.split(",")
                cResp = cResp[0:]
                for x in cResp:
                    print("-------------------------------------------------------")
                    if(x.find("\n")):
                        print(x[2:-3])
                    else:
                        print(x[2:-2])
                print("-------------------------------------------------------")
            else:
                print("That's not a valid choice. Please enter a valid choice from given options.")

        else:
            s.send(bytes(cInput, 'UTF-8'))#sending the choice of option
            data = s.recv(5024)
            print(data.decode('UTF-8'),'\n')
            s.close()
            #break;
            sys.exit();
