import serial

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)

def readlineCR(port):
    rv = ""
    while True:
        ch = port.read()
        if ch=='\r':
            return rv
        rv += ch
def init():
    port.write("\r\nSerial port is setup\r\n")
    
def read_card():
    card_id = readlineCR(port)
    if(card_id <> ""):
        return card_id
    else:
        return "No card"