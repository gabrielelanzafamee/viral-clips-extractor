import cv2
import time
import pytesseract

import numpy as np
import moviepy.editor as mpe
import speech_recognition as sr

from pydub import AudioSegment
from deepface import DeepFace
from pathos.multiprocessing import ThreadPool as Pool
from multiprocessing import set_start_method

from utils.multiprocess_moviepy import multiprocessify

recognizer = sr.Recognizer()

def is_face_talking(face: tuple[int, int, int, int], frame) -> bool:
    x, y, w, h = face
    face_roi = frame[y:y + h, x:x + w]
    gray_face = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)

    def handle_process(args):
        print(args)
        return args[1](args[0])

    # Use pytesseract to extract text from the face
    with sr.AudioFile("audio.wav") as source:
        [text, recognized_text] = Pool().map(handle_process, [
            (gray_face, pytesseract.image_to_string),
            (recognizer.record(source), recognizer.recognize_google)
        ])

    print(text, recognized_text)
    # Check if there is text in the face and if speech is detected
    if text and recognized_text != "Speech not recognized":
        print("Talking person detected!")
        return True

    print(recognized_text)
    return False

def get_face_actions(frame: np.ndarray) -> tuple[bool, list[int]]:
    try:
        faces = DeepFace.analyze(frame, detector_backend='mediapipe')
    except:
        return False, None

    j = 0

    if len(faces) < 0:
        return False, None

    for idx, face in enumerate(faces):
        is_t = is_face_talking(list(map(face['region'].get, face['region'].keys())), frame)
        if is_t and faces[idx]['dominant_emotion'] != face['dominant_emotion'] and face['dominant_emotion'] == 'happy':
            j = idx
    
    status, face = True, list(map(faces[j]['region'].get, faces[j]['region'].keys()))
    return status, face

def crop_video_frame(frame):
    global last_frame
    global current_face
    global current_face_start_time
    global left
    global right
    global output_resolution
    global duration_threshold

    # face detection
    detected, face = get_face_actions(frame)

    if not detected:
        if isinstance(last_frame, np.ndarray):
            # left = max(output_resolution[0], left)
            # right = min(left + output_resolution[0], right)
            print('Face not detected, using these ranges: ', left, right)
            cropped_frame = frame[:, left:right]
            resized_frame = cv2.resize(cropped_frame, output_resolution)
            return resized_frame
        else:
            return np.zeros(
                (output_resolution[1], output_resolution[0], 3), dtype=np.uint8
            )

    if current_face is None:
        current_face = face
        current_face_start_time = time.time()

    elapsed_time = time.time() - current_face_start_time
    if elapsed_time >= duration_threshold:
        current_face = face
        current_face_start_time = time.time()

    x, y, w, h = current_face

    # if the difference between old_left and new_left is more than 10 change face
    if abs(left - max(x - (output_resolution[0] - w) // 2, 0)) > 10:
        left = max(x - (output_resolution[0] - w) // 2, 0)
        right = min(x + w + (output_resolution[0] - w) // 2, frame.shape[1])

    cropped_frame = frame[:, left:right]
    resized_frame = cv2.resize(cropped_frame, output_resolution)
    last_frame = resized_frame

    print(f"Resized frame from {left} to {right}")
    return resized_frame

def crop_video(input_video, output_video, size=(720, 1280)):
    global current_face
    global current_face_start_time
    global last_frame
    global left
    global right
    global output_resolution
    global duration_threshold

    clip = mpe.VideoFileClip(input_video, audio=True)

    width = int(clip.size[1] * size[0] / clip.size[0])
    height = clip.size[1]
    left = 0
    right = width

    frames = []
    d = 1 / clip.duration
    x, w = 0, 0

    output_resolution = (width, height)

    last_frame = None
    current_face = None  # Initialize the current face
    current_face_start_time = None  # Initialize the start time of the current face
    duration_threshold = 3

    clip.audio.write_audiofile("audio.wav")

    import os
    cpu_count = os.cpu_count() - 1

    print("CPU Count", cpu_count)
    final = multiprocessify(composite_clip_wrapper, cpu_count)
    print("Start writing the video")
    final.write_videofile(output_video, fps=clip.fps)

def composite_clip_wrapper():
    return composite_clip(mpe.VideoFileClip("input.mp4"), (720, 1280))

def composite_clip(clip, size):
    clip = clip.subclip(0, 10)
    clip = clip.with_audio(clip.audio)
    clip = clip.resize(width=size[0], height=size[1])
    # clip = clip.image_transform(crop_video_frame)
    return clip

if __name__ == "__main__":
    crop_video("input.mp4", "output.mp4")
