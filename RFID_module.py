import serial

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=2.0)

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        rv += ch
        if ch=='\r' or ch=='':
            return rv

def init():
    port.write("\r\nSerial port is setup\r\n")
    
def read_card():
    card_id = readlineCR(port)
    if(card_id <> ""):
        return card_id
    else:
        return "No card"