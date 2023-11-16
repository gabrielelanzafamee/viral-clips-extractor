import json

from core.contents.chatgpt import completion

response_obj='''[
  {
    "start_time": 97.19, 
    "end_time": 127.43,
    "description": "Put here a simple description of the context in max 10 words"
    "duration":36 #Length in seconds
  },
]'''

def analyze_transcript(transcript: str):
    data: list = transcript.split("\n")
    chunks: list[tuple] = []
    contents: list = []
    content: str = ""

    print(data)
    print(f"\nChunking the transcript...")

    # chunk the transcript in multiple parts of a max of 3000 characters
    for i in range(0, len(data)):
        content += data[i] + "\n"
        if len(content) > 3000:
            print("Processing content: ", content)
            chunks.append((content, completion(content)))
            content = ""

    print(chunks)

    for (transcript_data, interesting_segment) in chunks:
        print(transcript_data, interesting_segment)
        try:
            contents_chunk = json.loads(interesting_segment)
            contents += contents_chunk
        except Exception as e:
            print(f"Ignored Exception: {e}")
            continue
        
    return contents