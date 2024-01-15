import os
from PIL import Image
from moviepy.editor import AudioFileClip, TextClip, VideoFileClip
from moviepy.video import fx
from moviepy.video.fx import all as vfx
import face recognition
import numpy as np
from moviepy.editor import VideoFileClip
from ESRGAN import esrgan_predict

def apply_slow_motion_effect(input_path, output_path, factor=0.5):
    clip = VideoFileClip(input_path).fx(fx.speedx, factor)
    clip.write_videofile(output_path)

def apply_grayscale_filter(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(vfx.grayscale)
    filtered_video.write_videofile(output_path)

def apply_vignette_filter(video_path, output_path, strength=0.5):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(vfx.vignette, intensity=strength)
    filtered_video.write_videofile(output_path)

def apply_blur_filter(video_path, output_path, radius=5):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(vfx.blur, size=radius)
    filtered_video.write_videofile(output_path)

def apply_sharpen_filter(video_path, output_path, amount=1.5):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(vfx.sharpen, amount=amount)
    filtered_video.write_videofile(output_path)

def apply_contrast_enhancer_filter(video_path, output_path, factor=1.5):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(vfx.contrast, amount=factor)
    filtered_video.write_videofile(output_path)

def apply_brightness_enhancer_filter(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(vfx.brightness)
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

# filter with neural network
def apply_super_resolution(video_path, output_path):
    video_clip = VideoFileClip(video_path)
    frames = [frame for frame in video_clip.iter_frames(fps=video_clip.fps)]
    processed_video = VideoFileClip(video_path)

    for i, frame in enumerate(frames):
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_sr = esrgan_predict(frame_bgr)
        frame_rgb = cv2.cvtColor(frame_sr, cv2.COLOR_BGR2RGB)
        processed_video = processed_video.set_frame(frame_rgb, i / video_clip.fps)

    processed_video.write_videofile(output_path, codec="libx264", audio_codec="aac")
