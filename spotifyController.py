import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
import random

client_id = ""
client_secret = ""
redirect_uri = "http://localhost:8080"
scope = "playlist-read-private playlist-read-collaborative user-read-playback-state user-modify-playback-state"
context_uri= ""


#Initializing Spotipy client with an OAuth Manager
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope))

#Begins playing a playlist
def playPlaylist(sp,device,context_uri,offset,ms):
    sp.start_playback(device_id=device,context_uri=context_uri, offset=offset, position_ms=ms)

#Gets the total # of tracks in the playlist for the purpose of picking a random track to begin playing
def getNumOfTracks(sp, context_uri):
    numberOfTracks = int(str((sp.playlist_tracks(playlist_id = context_uri, fields='total')))[10:-1])
    return numberOfTracks

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
        print (e)



