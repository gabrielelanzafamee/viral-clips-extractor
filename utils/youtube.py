from pytube import YouTube
from youtube_transcript_api import YouTubeTranscriptApi

def get_video(url, filename):
    yt = YouTube(url)

    video = yt.streams.filter(file_extension='mp4', progressive='True').order_by('resolution').desc().first()
    video.download(filename=filename)

    return yt.video_id, yt.title, yt.author

def get_transcript(video_id):
    formatted_transcript = ''
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=('en', 'it', ))

    for entry in transcript:
        start_time = "{:.2f}".format(entry['start'])
        end_time = "{:.2f}".format(entry['start'] + entry['duration'])
        text = entry['text']
        formatted_transcript += f"{start_time} - {end_time} : {text}\n"

    return formatted_transcript