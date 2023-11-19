""" improving the transcript analysis and clips extraction """

import re
import tiktoken

from core.contents.stt import STT
from core.utils.youtube import get_video
from core.utils.common import generate_random_string
from core.contents.chatgpt import completion

# video_url = "https://www.youtube.com/watch?v=bympMYTNS1s&ab_channel=NDL"
# input_video = f"tmp/{generate_random_string(16)}.mp4"

# video_id, title, author = get_video(video_url, input_video)
# print(video_id, title, author)

# # improving transcript extraction
# transcript = STT().get_transcript(input_video).get('transcript')
transcript = open("transcript.txt", "r").read()

idx = 0
tokens = 0
content = ""
transcript_iter = iter(transcript.split("\n"))
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
        open(f"transcript_{idx}.json", "w").write(completion(content))
        content = ""
        tokens = 0

    idx += 1

open("transcript.cleaned.txt", "w").write(content)

# now we should get more info about the transcript like
#  - the type of video
#  - the context of the video
#  - the topic of the video

# after that we should summarize and remove the parts useless of the transcript
#  - remove the parts where the speaker is not talking
#  - remove the parts where the speaker is talking but is not saying anything important
#  - remove the parts where the speaker is talking but is saying something not related to the video

# after all these considerations we can know create multiple prompt for different type of
# type, context and topic of the transcript and choose the correct duration and parts to extract

# some prompts could be like: