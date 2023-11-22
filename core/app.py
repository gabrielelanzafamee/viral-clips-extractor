import time
import random

from core.utils.video import segment_video, build_reel_format_videos, get_top_longest_videos
from core.utils.common import generate_random_string
from core.utils.youtube import get_video
from core.utils.tiktok import Tiktok
from core.contents.stt import STT
from core.extractor import analyze_transcript

def generate_video(video_url):
    time_start = time.time()

    input_video = f"tmp/{generate_random_string(16)}.mp4"

    video_id, title, author = get_video(video_url, input_video)
    print(video_id, title, author)

    transcript = STT().get_transcript(input_video).get('transcript')
    print(transcript)

    transcript_out = f"tmp/transcript_{generate_random_string(16)}.txt"
    print(f"Writing transcript in this file: {transcript_out}")

    with open(transcript_out, "w") as f:
        print(transcript, file=f)

    contents = analyze_transcript(transcript)
    print("Contents: ", contents)

    video_paths = segment_video(contents, input_video)
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