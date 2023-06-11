import os

cmd = 'youtube-dl -o "./audio/%(title)s.%(ext)s" -x --audio-format mp3 https://youtu.be/{0} >/dev/null 2>&1' # add video id to end of string

def downloadVideo(videoId):
  os.system(cmd.format(videoId))
