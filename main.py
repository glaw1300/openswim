from spotify import getAlJkPlaylist
from youtube import searchVideo, getVideoDuration, searchVideoRequests
from youtube_dl import downloadVideo

if __name__ == "__main__":
    tracks = getAlJkPlaylist()
    cont = True
    contFrom = "Glory Days by Bruce Springsteen"

    for i, track in enumerate(tracks):
        if contFrom is not None and contFrom == track['title']:
            cont = False 
            print(f"CONTINUING FROM: {contFrom}")
            continue 
        if cont:
            continue
        if (i + 1) % 10 == 0:
            print(f"PROGRESS: {i + 1}/{len(tracks)}")
        videoId = searchVideo(track['title'])
        if videoId is None:
            videoId = searchVideoRequests(track['title'], track['duration'])
            if videoId is None:
                continue
            downloadVideo(videoId)
        else:
          duration = getVideoDuration(videoId)
          # if percent difference of duration and track[duration] is greater than 10%, print error
          if abs(duration - track['duration']) / track['duration'] > 0.1:
              print(f"ERROR: {track['title']} has a duration of {track['duration']} but the video has a duration of {duration}")
              continue
          downloadVideo(videoId)
            