from mpd import MPDClient
from time import sleep
import RPi.GPIO as GPIO
import sys
import os
import math
from ConfigParser import SafeConfigParser
from mutagen.mp3 import MP3


#Project modules
import MPD_module
import RFID_module
import LCD_module

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
    parser = SafeConfigParser()
    parser.read('audiofiles.ini')
    current_tag = ""
    percentage = 0
    
    LCD_module.display_playing(5,15,50)

    print parser.get('Folders', '0727FBCC')
    SetupGPIO()
    MPD_module.MPD_init()
    RFID_module.init()
    while True:
        
        print "reading rfid"
        read_tag = str(RFID_module.read_card_id())
        if ((read_tag <> "None") and (read_tag <> current_tag)):
            parser.read('audiofiles.ini')
            try:   
                tag_dir = parser.get('Folders', read_tag)
                print "Parser dir: " + tag_dir
                MPD_module.client.stop()
                MPD_module.FolderToPlaylist(tag_dir)
                MPD_module.StartPlaying()
                current_tag = read_tag
                
            except:
                print "Folder not found"
            
        playlistlength = MPD_module.client.status()['playlistlength']
        try: 
            song = int(MPD_module.client.status()['song']) + 1
            #print MPD_module.client.status()
            percentage = math.trunc(float(MPD_module.get_elapsed()) / float(MPD_module.get_duration()) * 100)
            
            print MPD_module.get_elapsed()
            print MPD_module.get_duration()
        except:
            song = 0
        print  percentage    
        LCD_module.display_playing(song,playlistlength,percentage)
        
    sleep(5) 
    
    pass

if __name__ == "__main__":
    try:
        main(sys.argv)
    except KeyboardInterrupt:
        GPIO.cleanup()