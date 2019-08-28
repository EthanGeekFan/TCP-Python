import socket
import time

'''Internet default settings: '''
HOST = "127.0.0.1"
PORT = "12345"
BUFSIZE = 1024
Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SystemMessages:
SUCCESS = ">>>Connection established successfully!<<<"
PROCESS = ">>>Data Processing...<<<"
DISPLAY = ">>>Message Displaying<<<"
CONVEYED = ">>>Message has been fully displayed!<<<"
FINISHED = ">>>FINISHED<<<"

# Customize the HOST connection
host = input("Address?(default:127.0.0.1)>")
if host:
    HOST = host
else:
    pass

# Customize the PORT connection
dest = input("Port?(default:12345)>")
if dest:
    PORT = (int)(dest)
else:
    PORT = 12345

# Combine HOST & PORT Together and Bind to the socket:
ADDR = (HOST, PORT)
# Client.bind(ADDR)

# Connect with the server:
Client.connect(ADDR)
print(">>>Attempting to communicate with Server...<<<")

confirm = Client.recv(BUFSIZE).decode
if not confirm:
    print(">>>[ERR]Connection Failed!!!<<<")
else:
    print(SUCCESS)
    print("")
    while True:
        mes = input("发送>")
        if not mes:
            continue
        if mes == "quit()":
            break
        Client.send(mes.encode())
        while True:
            back = Client.recv(BUFSIZE).decode()
            print(">>>" + back + "<<<")
            if back == "FINISHED":
                break
print(">>>Client Closed<<<")
print(">>>See You Next Time<<<")
print("")
Client.close()
