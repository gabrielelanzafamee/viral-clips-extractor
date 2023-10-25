import json
import time
import random
import argparse

from core.utils.video import segment_video, build_reel_format_videos
from core.utils.common import generate_random_string
from core.utils.youtube import get_video
from core.utils.tiktok import Tiktok

from core.contents.chatgpt import analyze_transcript
from core.contents.stt import STT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='python clips_extractor.py', description='Viral Clips Extractor - Extract the most viral clips from a youtube video', epilog='')
    parser.add_argument('-u', '--url', help="Url of the video where to extract the clips")
    args = parser.parse_args()

    time_start = time.time()

    video_url = args.url
    input_video = f"tmp/{generate_random_string(16)}.mp4"

    video_id, title, author = get_video(video_url, input_video)
    print(video_id, title, author)

    data, transcript, audio_duration = STT().get_transcript(input_video)
    print(transcript)

    transcript_out = f"tmp/transcript_{generate_random_string(16)}.txt"
    print(f"Writing transcript in this file: {transcript_out}")

    with open(transcript_out, "w") as f:
        print(transcript, file=f)

    start = 0
    size = STT.calc_chunks_size(audio_duration)
    chunk_size = int(len(data) / size)
    contents = []
    chunks = [(transcript.split("\n")[i:i+size], analyze_transcript(transcript.split("\n")[i:i+size])) for i in range(0, len(transcript.split("\n")), size)]

    print("Transcript analysis")
    print(size)
    print(chunk_size)
    print(contents)
    print(chunks)

    for (transcript_data, interesting_segment) in chunks:
        try:
            contents_chunk = json.loads(interesting_segment["content"])
            contents += contents_chunk
        except Exception as e:
            print(f"Exception: {e}")
            continue

    print(contents)

    video_paths = segment_video(contents, input_video)
    print("Paths: ", video_paths)

    reel_paths = build_reel_format_videos(video_paths, crop=False)
    print("Reel Paths: ", reel_paths)

    # upload only the longest video and the top 3 videos by duration

    for video in reel_paths:
        print(f"Uploading video {video}")
        video_id = Tiktok.upload([video, "#fyp #ai #random"])
        print(f"Video uploaded with id {video_id}")
        time.sleep(random.randint(10, 20)) # Sleep between 10 and 20 seconds

    print(f"Result ended in {time.time() - time_start} seconds")