import serial
import MFRC522

port = serial.Serial("/dev/ttyAMA0", baudrate=115200, timeout=3.0)
MIFAREReader = MFRC522.MFRC522()

continue_reading = True

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
        
def read_card_id(): 
        # Scan for cards    
        (status,TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

        # If a card is found
        if status == MIFAREReader.MI_OK:
            print "Card detected"
        
        # Get the UID of the card
        (status,uid) = MIFAREReader.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == MIFAREReader.MI_OK:

            # Print UID
            id_hex = (uid[3] << 24) + (uid[2] << 16) + (uid[1] << 8) + uid[0]
            print "UID = " + "%08X" % id_hex
            return "%08X" % id_hex
            
     