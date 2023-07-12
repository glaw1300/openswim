import os 
from dotenv import load_dotenv
import requests
import json
import re

load_dotenv()

# search Youtube v3 Data API for a video
def searchVideo(query):
    # get API key from .env
    API_KEY = os.environ.get("YOUTUBE_API_KEY")
    
    # create request
    request = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=1&q={query}&key={API_KEY}"
    
    # send request
    response = requests.get(request)
    print(response.json())
    # return video id
    if response.status_code != 200:
        print(f"ERROR: {response.status_code, response.reason}")
        return None
    try:
        return response.json()['items'][0]['id']['videoId']
    except:
        print(f"ERROR with JSON: {response.json()}")
        return None

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

def lengthTextToMilliseconds(lengthText):
    parts = lengthText.split(':')
    if len(parts) == 3:
        hours = int(parts[0])
        minutes = int(parts[1])
        seconds = int(parts[2])
    else:
        hours = 0
        minutes = int(parts[0])
        seconds = int(parts[1])
    return hours * 60 * 60 * 1000 + minutes * 60 * 1000 + seconds * 1000
    

def searchVideoRequests(query, ogDuration):
    params = {'search_query':query.replace(' ', '+')}
    r = requests.get('https://www.youtube.com/results', params=params)
    js = json.loads(re.findall('ytInitialData.*?({.*?});', r.text)[0])
    # get video id and duration for the video in the first 3 results closest to the duration of the song
    minDif = 1.
    minInd = 0
    for i in range(3):
        try:
            videoInfo = js['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][i]['videoRenderer']
        except:
            print(f"Unable to find {query} at index {i}")
            continue
        videoDuration = lengthTextToMilliseconds(videoInfo['lengthText']['simpleText'])
        minDif = min(minDif, abs(videoDuration - ogDuration)/ogDuration)
        if minDif == abs(videoDuration - ogDuration)/ogDuration:
            minInd = i
    if minDif > 0.05:
        print(f"ERROR: {query} not found with manual search. Closest video has a duration of {videoDuration} compared to {ogDuration}")
        return None
    videoInfo = js['contents']['twoColumnSearchResultsRenderer']['primaryContents']['sectionListRenderer']['contents'][0]['itemSectionRenderer']['contents'][minInd]['videoRenderer']
    if (minInd != 0):
        print(f"WARNING: {query} not found at index 0. Found at index {minInd}")
    return videoInfo['videoId']

#print(getVideoDuration(searchVideo("Build Me Up Buttercup by The Foundations")))