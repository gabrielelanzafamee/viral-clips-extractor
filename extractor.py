import os
import argparse

from core.app import generate_video
from core.utils.common import try_catch

parser = argparse.ArgumentParser(prog='python clips_extractor.py', description='Viral Clips Extractor - Extract the most viral clips from a youtube video', epilog='')
parser.add_argument('-u', '--url', help="Url of the video where to extract the clips")
args = parser.parse_args()

if __name__ == "__main__":
    try_catch(generate_video, args.url)
    print("Removing tmp files...")
    for f in os.listdir("tmp"):
        try_catch(os.remove, f"tmp/{f}")