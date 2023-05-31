# ---------- LIBRARIES ----------
from pytube import YouTube
from pytube.exceptions import VideoUnavailable
from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips
import os , requests , json
import urllib.request


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
    elif(url.startswith('https://www.reddit.com/')):
        try:
            reddit_extraction(url)  
        except VideoUnavailable:
            print(f'The Reddit video {url} is unavailable.')
    else:
        print('Try Another Link')


# ---------- REDDIT ----------

def reddit_extraction(rd):
    rd=rd+".json"
    response = requests.get(rd)        
    if response.status_code == 200:
        json_data = response.text.strip()
        #print(json_data)
        text="fallback_url"
        index = json_data.find(text)
        text2="source=fallback"
        index2 = json_data.find(text2)        
        video_url=json_data[index+16:index2+15]
        audio_url=video_url.replace("DASH_1440", "DASH_audio")
        audio_url=audio_url.replace("DASH_1080", "DASH_audio")
        audio_url=audio_url.replace("DASH_720", "DASH_audio")
        audio_url=audio_url.replace("DASH_480", "DASH_audio")
        audio_url=audio_url.replace("DASH_360", "DASH_audio")
        print(video_url," heyyy ",audio_url)
        urllib.request.urlretrieve(video_url,filename="video.mp4")
        urllib.request.urlretrieve(audio_url,filename="audio.mp4")
        video_clip = VideoFileClip("video.mp4")
        audio_clip = AudioFileClip("audio.mp4")
        final_clip = video_clip.set_audio(audio_clip)
        final_clip.write_videofile("download.mp4")
        video_clip.close()
        audio_clip.close();
        os.remove('video.mp4')
        os.remove('audio.mp4')

    elif response.status_code == 429:
        print("Too Many Requests. Try again later")
    else:
        print("ERROR"+response.status_code)
        
    
    




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