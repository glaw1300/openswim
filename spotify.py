import requests
from dotenv import load_dotenv
import os

load_dotenv()

def getBearerToken():
  clientId = os.environ.get("SPOTIFY_CLIENT_ID")
  clientSecret = os.environ.get("SPOTIFY_CLIENT_SECRET")

  tokenHeaders = {
      'Content-Type': 'application/x-www-form-urlencoded'
  }

  tokenData = {
          'grant_type': 'client_credentials',
      'client_id': clientId,
      'client_secret': clientSecret
  }

  tokenUrl = "https://accounts.spotify.com/api/token"

  # send post request to get token
  tokenResponse = requests.post(tokenUrl, headers=tokenHeaders, data=tokenData)

  return tokenResponse.json()['access_token']

def getPlaylistPage(playlistId, next=None):
  token = getBearerToken()

  playlistHeaders = {
      'Authorization': 'Bearer ' + token
  }

  playlistData = {
      'fields': 'items(track(duration_ms,name,artists(name))),next'
  }

  playlistUrl = next or f"https://api.spotify.com/v1/playlists/{playlistId}/tracks"

  # send get request to get playlist tracks
  playlistResponse = requests.get(playlistUrl, headers=playlistHeaders, params=playlistData)

  return playlistResponse.json()

def getPlaylistTracks(playlistId):
  tracks = []
  next = None

  while True:
    playlistPage = getPlaylistPage(playlistId, next)
    tracks += playlistPage['items']

    if playlistPage['next'] is None:
      break

    next = playlistPage['next']    

  return tracks

def writePlaylistTracksToFile(playlistId, filename):
  tracks = getPlaylistTracks(playlistId)

  with open(filename, "w") as file:
    for track in tracks:
      # combine all artists into one string
      artists = ", ".join([artist['name'] for artist in track['track']['artists']])
      file.write(f"{track['track']['name']} by {artists}-{track['track']['duration_ms']}\n")

def getAlJkPlaylist():
  tracks = getPlaylistTracks(os.environ.get("PLAYLIST_ID"))
  ret = []

  for track in tracks:
    # combine all artists into one string
    artists = ", ".join([artist['name'] for artist in track['track']['artists']])
    ret.append({"title": f"{track['track']['name']} by {artists}", "duration":int(track['track']['duration_ms'])})
  
  return ret

#writePlaylistTracksToFile(os.environ.get("PLAYLIST_ID"), "aljk.txt")