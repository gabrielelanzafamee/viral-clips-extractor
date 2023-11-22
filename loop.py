import os
import time
import argparse

from core.app import generate_video
from core.utils.common import try_catch

parser = argparse.ArgumentParser(prog='python clips_extractor.py', description='Viral Clips Extractor - Extract the most viral clips from a youtube video', epilog='')
parser.add_argument('-p', '--path', help="Path of the file that contains the urls of the videos to process")
args = parser.parse_args()

if __name__ == "__main__":
    while True:
        urls = open(args.path, "r").readlines()

        if len(urls) == 0:
            time.sleep(1)
            continue

        url = urls.pop(0)
        
        print(f"Processing the url: {url}\n")
        
        try_catch(generate_video, url)
        print("Removing tmp files...")
        for f in os.listdir("tmp"):
            try_catch(os.remove, f"tmp/{f}")

        open(args.path, "w").write("\n".join(urls))
        print("Sleep 5 minutes for the next video...")
        time.sleep(300) # sleep for 5 minutes