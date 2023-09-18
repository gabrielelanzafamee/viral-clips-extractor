import os
import math
import subprocess
import moviepy.editor as mpe

from contents.stt import STT
from contents.face_cropping import crop_video

from utils.common import generate_random_string

def gen_subtitles(transcript, width, height):
    clips = []

    for (text, start_times, end_times) in transcript:
        t_item = mpe.TextClip(
            text,
            color='#fff',
            align="West",
            stroke_width=2 * 6,
            stroke_color='#000',
            font_size=36 * 6,
            interline=0,
            font='Arial-Black',
            kerning=3,
            method="caption",
            size=(680 * 6, '')
        )

        t_item = t_item.resize(0.16)
        t_item = t_item.with_start(start_times[0])
        t_item = t_item.with_end(end_times[-1])
        t_item = t_item.with_position((20, height - 250))

        clips.append(t_item)

    return clips

def segment_video(response, path) -> list[str]:
    paths = []

    for segment in response :
        start_time = math.floor(float(segment.get("start_time", 0)))
        end_time = math.ceil(float(segment.get("end_time", 0))) + 2
        output_file = f"tmp/{generate_random_string(16)}.mp4"
        command = f"ffmpeg -i {path} -ss {start_time} -to {end_time} -c copy {output_file}"
        subprocess.call(command, shell=True)
        paths.append(output_file)

    return paths

def build_reel_format_videos(video_paths: list[str]) -> list[str]:
    paths = []
    w, h = 720, 1280

    print("Start building process...")

    for idx, path in enumerate(video_paths):
        id = generate_random_string(16)

        tmp_audio = f"tmp/audio_{id}.wav"
        output_file = f"out/no_crop_{id}.mp4"
        clip = mpe.VideoFileClip(path, audio=True)

        clip = clip.resize(width=w)
        clip = clip.with_position(("center", "center"))
        # clip = clip.fx(mpe.vfx.mirror_x)

        audio = clip.audio
        audio.write_audiofile(tmp_audio)
        data = STT().__call_whisper__(tmp_audio)
        subtitles_points = []
        for i in range(0, len(data['segments']), 5):
            segments = data['segments'][i:i+5]
            for segment in segments:
                    words = ' '.join([x['text'] for x in segment['words']])
                    words_start_times = [x['start'] for x in segment['words']]
                    words_end_times = [x['end'] for x in segment['words']]
                    subtitles_points.append((words, words_start_times, words_end_times))

        subtitles = gen_subtitles(subtitles_points, w, h)

        final = mpe.CompositeVideoClip([clip] + subtitles, (w, h))
        final.write_videofile(output_file)

        try:
            tmp_cropped_output_file = f"tmp/crop_{id}.mp4"
            cropped_output_file = f"out/crop_{id}.mp4"
            crop_video(path, tmp_cropped_output_file)
            cropped_clip = mpe.VideoFileClip(tmp_cropped_output_file, audio=True)
            final_cropped = mpe.CompositeVideoClip([cropped_clip] + subtitles, (w, h))
            final_cropped.write_videofile(cropped_output_file)
            os.remove(tmp_cropped_output_file)
        except:
            print("Cropped video passed")

        os.remove(tmp_audio)
        paths.append(output_file)

    return paths
