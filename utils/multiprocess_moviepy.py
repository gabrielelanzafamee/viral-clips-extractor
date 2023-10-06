import os
import math
import ffmpeg
import multiprocessing
import threading
import moviepy as mp


class ClipRendererProcess(threading.Thread):
    def __init__(self, clip_gen, start_frame, end_frame, *args, **kwargs):
        super().__init__()

        self.clip_gen = clip_gen
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.fps = kwargs['fps']
        
        self.args = args
        self.kwargs = kwargs

    def run(self):
        print(self.args, self.kwargs)

        start_time = self.start_frame / self.fps
        end_time = self.end_frame / self.fps

        self.clip_gen().subclip(start_time, end_time).write_videofile(*self.args, **self.kwargs)


class MultiprocessingClipRenderer:
    def __init__(self, clip_gen, processes=1):
        self.clip_gen = clip_gen
        self.processes = processes

    def write_videofile(self, duration, *args, **kwargs):
        multiprocessing.set_start_method("spawn")

        fps = kwargs['fps']

        filename, ext = args[0].split('.')
        frames_count = round(duration * fps)
        frames_step = math.ceil(frames_count / self.processes)

        chunks = [(i, min(i + frames_step, frames_count)) for i in range(0, frames_count, frames_step)]
        video_files = [f"{filename}_tmp_{fs}_{fe}.{ext}" for (fs, fe) in chunks]

        processes = [ClipRendererProcess(self.clip_gen, fs, fe, f, **kwargs) for ((fs, fe), f) in zip(chunks, video_files)]
        [p.start() for p in processes]
        [p.join() for p in processes]

        merged_video_list_name = f"{filename}_tmp_video_list.txt"

        print(video_files)
        with open(merged_video_list_name, 'w') as f:
            for video_file in video_files:
                print(f"file {video_file}", file=f)

        f.close()
        ffmpeg.input(merged_video_list_name, format='concat', safe=0).output(args[0], c='copy').run(overwrite_output=True)

        os.remove(merged_video_list_name)
        for video_file in video_files:
            os.remove(video_file)


def multiprocessify(clip_gen, processes=1):
    clip = clip_gen()
    renderer = MultiprocessingClipRenderer(clip_gen, processes)

    def hook_write_videofile(*args, **kwargs):
        return renderer.write_videofile(clip.duration, *args, **kwargs)
    clip.write_videofile = hook_write_videofile

    return clip