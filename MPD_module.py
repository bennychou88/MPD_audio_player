from mpd import MPDClient

client = MPDClient() # instantiate the client object

def MPD_init():
    client.connect(host="localhost", port=6600) # connect to the mpd daemon
    client.clear()
    client.update() # update the mpd database with the files in our books folder
    print "init MPD"

def FolderToPlaylist(foldername):
    client.clear()
    try:
        print("Adding music to playlist:")
        for filename in client.lsinfo(foldername):
            print "Adding: " + filename["file"]
            client.add(filename["file"])
        return True
    except:
        print "Error: folder does not exists"
        return False
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
