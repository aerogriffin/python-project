import os
import numpy as np
import face_recognition

from PIL import Image
from moviepy.editor import AudioFileClip, TextClip, VideoFileClip, VideoClip
from moviepy.video import fx
from moviepy.video.fx import all as vfx
from moviepy.video.fx import speedx, colorx
import cv2
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

def apply_slow_motion_effect(input_path, output_path, factor):
    clip = VideoFileClip(input_path).fx(colorx, factor=0)  # Setting factor to 0 makes the video black and white
    clip.write_videofile(output_path)



def apply_color_filter(video_path, output_path, color="sepia"):
    video_clip = VideoFileClip(video_path)
    
    # Function to apply color filter to each frame
    def apply_filter(frame):
        # Adjust the color filter here
        if color == "sepia":
            # Apply a simple sepia filter
            sepia_filter = np.array([[0.393, 0.769, 0.189],
                                     [0.349, 0.686, 0.168],
                                     [0.272, 0.534, 0.131]])
            frame = np.dot(frame, sepia_filter.T).reshape(frame.shape)

        return np.clip(frame, 0, 255).astype(np.uint8)

    # Apply the color filter to each frame
    filtered_frames = [apply_filter(frame) for frame in video_clip.iter_frames()]

    # Create the target directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Create a new video clip with the filtered frames
    filtered_video = VideoClip(lambda t: filtered_frames[int(t * video_clip.fps)], duration=video_clip.duration)
    audio_clip = AudioFileClip(video_path)
    filtered_video = filtered_video.set_audio(audio_clip)
    filtered_video.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=video_clip.fps)



def apply_grayscale_filter(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(fx.grayscale)
    filtered_video.write_videofile(output_path)

def apply_vignette_filter(video_path, output_path, strength=0.5):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(vfx.vignette, intensity=strength)
    filtered_video.write_videofile(output_path)

def apply_blur_filter(video_path, output_path, radius=5):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(fx.blur, size=radius)
    filtered_video.write_videofile(output_path)

def apply_sharpen_filter(video_path, output_path, amount=1.5):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(fx.sharpen, amount=amount)
    filtered_video.write_videofile(output_path)

def apply_contrast_enhancer_filter(video_path, output_path, factor=1.5):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(fx.contrast, amount=factor)
    filtered_video.write_videofile(output_path)

def apply_brightness_enhancer_filter(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(fx.brightness)
    filtered_video.write_videofile(output_path)

# filter with face recognition
def apply_face_detection(video_path, output_path):
    video_capture = cv2.VideoCapture(video_path)
    width = int(video_capture.get(3))
    height = int(video_capture.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, 30.0, (width, height))
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        for face_location in face_locations:
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        output_video.write(frame)

    video_capture.release()
    output_video.release()
