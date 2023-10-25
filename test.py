import random
import time
from core.utils.tiktok import Tiktok
from core.utils.video import get_top_longest_videos

tt = Tiktok()
paths = ['out/no_crop_0_7dA3633e73baEdBC.mp4', 'out/no_crop_1_86AEC0B31A6EEB54.mp4', 'out/no_crop_2_0554BB1f4E754Baa.mp4', 'out/no_crop_3_1Af2Fe15F1A39660.mp4', 'out/no_crop_4_01Be862afBdB34A0.mp4', 'out/no_crop_5_fcd4b9ECC37C53bC.mp4', 'out/no_crop_6_eE1B72074Ce0Ff7d.mp4', 'out/no_crop_7_9Bfb9C6dc95B8AB6.mp4', 'out/no_crop_8_FcE733F8F9F7d472.mp4', 'out/no_crop_9_aC8b1af0EcDDe6dd.mp4', 'out/no_crop_10_B3fc10f4e3DF2D8E.mp4']
for video, video_duration in get_top_longest_videos(paths, 4):
    print(f"Uploading video {video}")
    video_id = Tiktok.upload([video, "#fyp #ai #random"])
    print(f"Video uploaded with id {video_id}")
    time.sleep(random.randint(10, 20)) # Sleep between 10 and 20 seconds