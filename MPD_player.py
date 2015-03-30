from mpd import MPDClient
from time import sleep
import RPi.GPIO as GPIO
import sys
import os

#Project modules
import MPD_module
import RFID_module

def FolderToPlaylist(foldername):
    client.clear()
    print("Adding music to playlist:")
    print (os.path.exists("/home/pi/MP3Files/" + foldername))
    for filename in client.lsinfo(foldername):
        print "Adding: " + filename["file"]
        client.add(filename["file"])
    #print(client.playlist())

def StartPlaying():
    client.play() # play the playlist
    print "Start playing playlist"
	#print client.status()
 
def Next():

    if (int(client.status()['song']) < int((client.status()['playlistlength']))-1): #check if there is a next song
        print "Next song"
        client.next()
    else:
        print "Fail: No next song"

def Previous():

    if (int(client.status()['song']) > 0): #check if there is a next song
        print "Previous song"
        client.previous()
    else:
        print "Fiil: No previous song"	

def PlayButtonFunction(channel):
    print "Play button is pressed"

def NextButtonFunction(channel):
    print "Next button is pressed"
    Next()

def PreviousButtonFunction(channel):
    print "Previous button is pressed"
    Previous()
	
def SetupGPIO():
    GPIO.setmode(GPIO.BCM)
	#GPIO.setup(23, GPIO.OUT)
    GPIO.setup(18, GPIO.IN, pull_up_down = GPIO.PUD_UP)	#Play button
    GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_UP)	#Play button
    GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)	#Play button
	
    GPIO.add_event_detect(18, GPIO.FALLING, callback=PlayButtonFunction, bouncetime=300)
    GPIO.add_event_detect(23, GPIO.FALLING, callback=NextButtonFunction, bouncetime=300)
    GPIO.add_event_detect(24, GPIO.FALLING, callback=PreviousButtonFunction, bouncetime=300)

def main(argv):
    SetupGPIO()
    MPD_module.MPD_init()
    RFID_module.init()

    sleep(5)
    #GPIO.output(23, False)
	
    MPD_module.client.stop()
	
    while(True):
        current_card_id = RFID_module.read_card()
        print current_card_id
        if (current_card_id <> "No card"):
            print "adding: " + current_card_id
            print MPD_module.FolderToPlaylist(current_card_id)
            MPD_module.StartPlaying()
        
        
    pass

if __name__ == "__main__":
    main(sys.argv)