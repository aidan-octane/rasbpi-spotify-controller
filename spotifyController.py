import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random
import tkinter as tk

client_id = ""
client_secret = ""
redirect_uri = "http://localhost:8080"
scope = "playlist-read-private playlist-read-collaborative user-read-playback-state user-modify-playback-state"
#List of Context URIs
playlists=["spotify:playlist:4IkBIMPsrrSyAmgdbr263x", "spotify:playlist:2PM7p7H8L3hDcIxxAxuwwb"]
        #'stormy city night', 'ambience of an apocalypse'


#Initializing Spotipy client with an OAuth Manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope))

#Class that keeps track of the 'current playlist' 
class playlist_num_count:
    count=0
    
#Begins playing a playlist
def playPlaylist(sp,device,context_uri,offset,ms):
    sp.start_playback(device_id=device,context_uri=context_uri, offset=offset, position_ms=ms)

#Gets the total # of tracks in the playlist for the purpose of picking a random track to begin playing
def getNumOfTracks(sp, context_uri):
    numberOfTracks = int(str((sp.playlist_tracks(playlist_id = context_uri, fields='total')))[10:-1])
    return numberOfTracks

#GUI stuff
def button_click_left():
    if(current_playlist.count>0):
        current_playlist.count = current_playlist.count-1
    shuffle_and_play(sp, playlists[current_playlist.count])

def button_click_right():
    if(current_playlist.count < len(playlists)-1):
        current_playlist.count = current_playlist.count+1
    shuffle_and_play(sp, playlists[current_playlist.count])
   
def shuffle_and_play(sp, context_uri):
    offsetNumber = random.random() * getNumOfTracks(sp, context_uri)
    offset = {"position":offsetNumber}  

    #Stores the device at the top of the list of devices currently active on Spotify (my phone)
    res=sp.devices()
    first_device = res['devices'][0].get('id')

    #Prevents code from crashing in edge cases - namely, if no devices are running Spotify
    if first_device:
        try:
            playPlaylist(sp,first_device,context_uri,offset,ms=0)
        except Exception as e:
            print("ERROR: \n")
            print(e)

#Instantiates a playlist counter
current_playlist = playlist_num_count
#Begin program by playing the first playlist :3
shuffle_and_play(sp, playlists[current_playlist.count])
# Create the main window
window = tk.Tk()
window.title("PLAYER")

# Create a label widget to display text
label = tk.Label(window, text="CHANGE PLAYLIST")
label.pack()

# Create a button widget
button_one = tk.Button(window, text="<", command=button_click_left)
button_two = tk.Button(window, text=">", command=button_click_right)
button_one.pack()
button_two.pack()

# Start the main event loop
window.mainloop()




