import os
import time
import random
import argparse

from core.utils.video import segment_video, build_reel_format_videos, get_top_longest_videos
from core.utils.common import generate_random_string, try_catch
from core.utils.youtube import get_video
from core.utils.tiktok import Tiktok
from core.contents.stt import STT
from core.extractor import analyze_transcript

global tmp_files

parser = argparse.ArgumentParser(prog='python clips_extractor.py', description='Viral Clips Extractor - Extract the most viral clips from a youtube video', epilog='')
parser.add_argument('-u', '--url', help="Url of the video where to extract the clips")
args = parser.parse_args()

def main():
    global tmp_files
    tmp_files = []
    
    time_start = time.time()

    video_url = args.url
    input_video = f"tmp/{generate_random_string(16)}.mp4"
    tmp_files.append(input_video)

    video_id, title, author = get_video(video_url, input_video)
    print(video_id, title, author)

    data, transcript, audio_duration = STT().get_transcript(input_video)
    tmp_files += list(dict.fromkeys([d[0] for d in data]))
    print(transcript)

    transcript_out = f"tmp/transcript_{generate_random_string(16)}.txt"
    tmp_files.append(transcript_out)
    print(f"Writing transcript in this file: {transcript_out}")

    with open(transcript_out, "w") as f:
        print(transcript, file=f)

    contents = analyze_transcript(transcript)
    print("Contents: ", contents)

    video_paths = segment_video(contents, input_video)
    tmp_files += video_paths
    print("Paths: ", video_paths)

    reel_paths = build_reel_format_videos(video_paths, crop=False)
    print("Reel Paths: ", reel_paths)

    # upload only the longest video and the top 3 videos by duration
    for video, video_duration in get_top_longest_videos(reel_paths, 4):
        print(f"Uploading video {video}")
        video_id = Tiktok.upload([video, "#fyp #ai #random"])
        print(f"Video uploaded with id {video_id}")
        time.sleep(random.randint(10, 20)) # Sleep between 10 and 20 seconds

    print(f"Result ended in {time.time() - time_start} seconds")
    return reel_paths, tmp_files


if __name__ == "__main__":
    try_catch(main)
    print("Removing tmp files...", tmp_files)
    for f in tmp_files:
        try_catch(os.remove, f)
