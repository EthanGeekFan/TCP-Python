import socket
import time
import RPi.GPIO as GPIO

'''Internet default settings: '''
HOST = ""
PORT = "12345"
BUFSIZE = 1024
Server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# SystemMessages:
SUCCESS = "Connection established successfully!"
PROCESS = "Data Processing..."
DISPLAY = "Message Displaying"
CONVEYED = "Message has been fully displayed!"
FINISHED = "FINISHED"


'''GPIO Hardware Settings: '''
SIG_0 = 12
SIG_1 = 16
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(SIG_0, GPIO.OUT)
GPIO.setup(SIG_1, GPIO.OUT)


# Codes Convert: FanSCII:
FanSCII = {"a": "1011", "b": "1100", "c": "1101", "d": "1110", "e": "1111",
           "f": "10000", "g": "10001", "h": "10010", "i": "10011", "j": "10100",
           "k": "10101", "l": "10110", "m": "10111", "n": "11000", "o": "11001",
           "p": "11010", "q": "11011", "r": "11100", "s": "11101", "t": "11110",
           "u": "11111", "v": "100000", "w": "100001", "x": "100010", "y": "100011",
           "z": "100100",
           "A": "100101", "B": "100110", "C": "100111", "D": "101000", "E": "101001",
           "F": "101010", "G": "101011", "H": "101100", "I": "101101", "J": "101110",
           "K": "101111", "L": "110000", "M": "110001", "N": "110010", "O": "110011",
           "P": "110100", "Q": "110101", "R": "110110", "S": "110111", "T": "111000",
           "U": "111001", "V": "111010", "W": "111011", "X": "111100", "Y": "111101",
           "Z": "111110",
           "0": "0", "1": "1", "2": "10", "3": "11", "4": "100",
           "5": "101", "6": "110", "7": "111", "8": "1000", "9": "1001",
           " ": "00", "\n": "000", "!": "01", "\"": "010", "#": "011", "$": "0100",
           "%": "0101", "&": "0110", "\'": "0111", "(": "01000", ")": "01001",
           "*": "01010", "+": "01011", ",": "01100", "-": "01101", ".": "01110",
           "/": "01111", ":": "010000", ";": "010001", "<": "010010", "=": "010011",
           ">": "010100", "?": "010101", "@": "010110", "[": "010111", "\\": "011000",
           "]": "011001", "^": "011010", "_": "011011", "{": "011100", "|": "011101",
           "}": "011100", "~": "011111", }

# Definitions of Functions:
"""
In this part imported functions are defined;
They are used to ensure the program work as intended
"""


def convert(s):
    return FanSCII[s]


def output(s):
    if s is "0":
        GPIO.output(SIG_0, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(SIG_0, GPIO.LOW)
        time.sleep(0.2)
    elif s is "1":
        GPIO.output(SIG_1, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(SIG_1, GPIO.LOW)
        time.sleep(0.2)
    else:
        time.sleep(1)
    pass


def process(data):
    encoded = ""
    for e in list(data):
        encoded += convert(e)
    return encoded


def display(encoded):
    signal = list(encoded)
    for e in signal:
        output(e)
    pass


# Customize the PORT connecting
dest = input("Port?(default:12345)>")
if dest:
    PORT = (int)(dest)
else:
    PORT = 12345

# Combine HOST & PORT Together and Bind to the socket:
ADDR = (HOST, PORT)
Server.bind(ADDR)
Server.listen(5)

# Start the infinite loop to work as a SERVER:
while True:
    print("Waiting for connection...")
    clientSocket, clientAddress = Server.accept()
    start = time.clock()
    print("Connection from ", clientAddress)
    print("Connecting...")
    print(SUCCESS)
    print("")
    clientSocket.send(SUCCESS.encode())
    while True:
        DATA = clientSocket.recv(BUFSIZE).decode()
        if not DATA:
            break
        print("DATA RECEIVED!")
        print("[%s]Data:" % time.ctime(), DATA)
        clientSocket.send(PROCESS.encode())
        print(PROCESS)
        Encoded = process(DATA)
        clientSocket.send(DISPLAY.encode())
        print(DISPLAY)
        print(Encoded)
        display(Encoded)
        clientSocket.send(CONVEYED.encode())
        print(CONVEYED)
        clientSocket.send(FINISHED.encode())
    print("")
    format = "%Y-%m-%d %H-%M-%S"
    print(">>>Connection Closed at %s<<<" % time.ctime())
    end = time.clock()
    SerTime = end - start
    print("Served for %s Seconds in Total" % SerTime)
    print("")

clientSocket.close()
Server.close()
print(">>>Server On Closing<<<")
print(">>>Cleaning GPIO<<<")
print("")
GPIO.cleanup()
