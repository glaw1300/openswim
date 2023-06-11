import os 
from dotenv import load_dotenv
import requests

load_dotenv()

# search Youtube v3 Data API for a video
def searchVideo(query):
    
    # get API key from .env
    API_KEY = os.environ.get("YOUTUBE_API_KEY")
    
    # create request
    request = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={API_KEY}"
    
    # send request
    response = requests.get(request)
    
    # return video id
    if response.status_code != 200:
        print(f"ERROR: {response.status_code, response.reason}")
        return None

    return response.json()['items'][0]['id']['videoId']

# get video duration
def getVideoDuration(videoId):
      
      # get API key from .env
      API_KEY = os.environ.get("YOUTUBE_API_KEY")
      
      # create request
      request = f"https://www.googleapis.com/youtube/v3/videos?part=contentDetails&id={videoId}&key={API_KEY}"
      
      # send request
      response = requests.get(request)

      if response.status_code != 200:
        print(f"ERROR: {response.status_code, response.reason}")
        return None
      
      # return video duration
      return iso8601toMilliseconds(response.json()['items'][0]['contentDetails']['duration'])

def iso8601toMilliseconds(iso8601):
    # remove 'PT' from string
    iso8601 = iso8601[2:]

    # convert to milliseconds
    milliseconds = 0

    # get hours
    if 'H' in iso8601:
        hours = int(iso8601.split('H')[0])
        milliseconds += hours * 60 * 60 * 1000
        iso8601 = iso8601.split('H')[1]

    # get minutes
    if 'M' in iso8601:
        minutes = int(iso8601.split('M')[0])
        milliseconds += minutes * 60 * 1000
        iso8601 = iso8601.split('M')[1]

    # get seconds
    if 'S' in iso8601:
        seconds = int(iso8601.split('S')[0])
        milliseconds += seconds * 1000

    return milliseconds

#print(getVideoDuration(searchVideo("Build Me Up Buttercup by The Foundations")))