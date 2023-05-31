# ---------- LIBRARIES ----------
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os , time


# ---------- CHECK URL TYPE ----------
def main():
    url = input("Enter url: ");
    if not (url.startswith('https:')):
        url = "https://" + url
    if(url.startswith('https://youtube.com/') or url.startswith('https://youtu.be/')):
        try:
            yt = YouTube(url)
            youtube_extraction(yt)
        except VideoUnavailable:
            print(f'The Youtube video {url} is unavailable.')
    else:
        print('not youtube video')


# ---------- REDDIT ----------



# ---------- FACEBOOK ----------



# ---------- INSTAGRAM ----------



# ---------- YOUTUBE ----------
def youtube_extraction(yt):
    f2160 = 0; # If you want 2160p videos then make the value as 1
    f1440 = 0; # If you want 1440p videos then make the value as 1
    
    yt.streams.filter(abr="128kbps")[0].download(filename='audio.mp4')
    try:
        if(f2160 == 1):
            yt.streams.filter(res="2160p")[0].download(filename='video.mp4')
        else:
            raise IndexError
    except IndexError:
        try:
            if(f1440 == 1):
                yt.streams.filter(res="1440p")[0].download(filename='video.mp4')
            else:
                raise IndexError
        except IndexError:
            try:
                yt.streams.filter(res="1080p")[0].download(filename='video.mp4')
            except IndexError:
                try:
                    yt.streams.filter(res="720p")[0].download(filename='video.mp4')
                except IndexError:
                    yt.streams.filter(res="480p")[0].download(filename='video.mp4')
    video_clip = VideoFileClip("video.mp4")
    audio_clip = AudioFileClip("audio.mp4")
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile(yt.title + ".mp4")
    video_clip.close()
    audio_clip.close();
    os.remove('video.mp4')
    os.remove('audio.mp4')


# ---------- MAIN ----------
if __name__ == "__main__":
    main()