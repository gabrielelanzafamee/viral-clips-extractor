import re
import json
import tiktoken

from core.contents.chatgpt import extract_clips

def analyze_transcript(transcript: str) -> list[dict]:
    idx = 0
    tokens = 0
    content = ""
    transcript_iter = iter(transcript.split("\n"))
    clips: list[dict] = []

    while line := next(transcript_iter, -1):
        if line == -1:
            break

        match = re.match(r"Text:\s+(.+)\sTimestamp:\s(.+)\s-\s(.+)", line)
        if match == None: continue

        text = match.group(1)
        timestamp_start = match.group(2)
        timestamp_end = match.group(3)

        print(f"Content: {text}")
        print(f"Timestamp Start: {timestamp_start}")
        print(f"Timestamp End: {timestamp_end}\n")

        if idx > 0 and text.lower() != re.match(r"Text:\s+(.+)\sTimestamp:\s(.+)\s-\s(.+)", transcript.split("\n")[idx-1]).group(1).lower():
            c = f"Text: {text} Timestamp: {timestamp_start} - {timestamp_end}\n"
            content += c
            tokens += len(tiktoken.encoding_for_model("gpt-3.5-turbo").encode(c))

        print("Total token: ", tokens)
        if tokens > 3500:
            try:
                clips += json.loads(extract_clips(content))
            except Exception as e:
                print("Error while extracting clips from transcript: ", e)

            content = ""
            tokens = 0

        idx += 1

    return clips