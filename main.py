from spotify import getAlJkPlaylist
from youtube import searchVideo, getVideoDuration
from youtube_dl import downloadVideo

if __name__ == "__main__":
    tracks = getAlJkPlaylist()

    for i, track in enumerate(tracks):
        if (i + 1) % 10 == 0:
            print(f"PROGRESS: {i + 1}/{len(tracks)}")
        videoId = searchVideo(track['title'])
        if videoId is None:
            print(f"ERROR: {track['title']} not found")
            continue
        duration = getVideoDuration(videoId)

        # if percent difference of duration and track[duration] is greater than 10%, print error
        if abs(duration - track['duration']) / track['duration'] > 0.1:
            print(f"ERROR: {track['title']} has a duration of {track['duration']} but the video has a duration of {duration}")
            continue
        downloadVideo(videoId)
            