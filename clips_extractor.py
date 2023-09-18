import json
import time
import argparse

from utils.video import segment_video, build_reel_format_videos
from utils.common import generate_random_string
from utils.youtube import get_video

from contents.chatgpt import analyze_transcript
from contents.stt import STT

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='python clips_extractor.py', description='Viral Clips Extractor - Extract the most viral clips from a youtube video', epilog='')
    parser.add_argument('-u', '--url')
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

    print(f"\nChunking the transcript...")
    print(f"Single Chunk Size: {chunk_size}")
    print(f"Item x Chunk: {size}\n")

    for _ in range(0, size):
        chunk = "\n".join(transcript.split("\n")[start:start+chunk_size])
        interesting_segment = analyze_transcript(chunk)

        try:
            contents_chunk = json.loads(interesting_segment["content"])
            print(contents_chunk)
            contents += contents_chunk
        except:
            print(interesting_segment["content"])
        
        start += chunk_size

    print(contents)

    video_paths = segment_video(contents, input_video)
    print("Paths: ", video_paths)

    reel_paths = build_reel_format_videos(video_paths, title, author)
    print("Reel Paths: ", reel_paths)

    print(f"Result ended in {time.time() - time_start} seconds")