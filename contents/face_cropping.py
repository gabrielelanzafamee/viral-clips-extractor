import cv2
import time

import numpy as np
import mediapipe as mp
import moviepy.editor as mpe

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def crop_video(input_video, output_video, size=(720, 1280)):
    global current_face
    global current_face_start_time
    global last_frame

    clip = mpe.VideoFileClip(input_video, audio=True)

    width = int(clip.size[1] * size[0] / clip.size[0])
    height = clip.size[1]

    frames = []
    d = 1 / clip.duration
    x, w = 0, 0

    output_resolution = (width, height)

    last_frame = None
    current_face = None  # Initialize the current face
    current_face_start_time = None  # Initialize the start time of the current face
    duration_threshold = 3

    def crop_video_frame(frame):
        global last_frame
        global current_face
        global current_face_start_time

        im = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(im, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

        if len(faces) > 0:
            if current_face is None:
                current_face = faces[0]
                current_face_start_time = time.time()

            elapsed_time = time.time() - current_face_start_time
            if elapsed_time >= duration_threshold:
                current_face = faces[0]
                current_face_start_time = time.time()

            x, y, w, h = current_face

            left = max(x - (output_resolution[0] - w) // 2, 0)
            right = min(x + w + (output_resolution[0] - w) // 2, frame.shape[1])

            cropped_frame = frame[:, left:right]
            resized_frame = cv2.resize(cropped_frame, output_resolution)

            last_frame = resized_frame
            return resized_frame
        else:
            if isinstance(last_frame, np.ndarray):
                return last_frame
            else:
                return np.zeros((output_resolution[1], output_resolution[0], 3), dtype=np.uint8)


    clip = clip.image_transform(crop_video_frame)
    clip = clip.with_audio(clip.audio)
    clip = clip.resize(width=size[0], height=size[1])
    clip.write_videofile(output_video, fps=clip.fps)