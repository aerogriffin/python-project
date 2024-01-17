import cv2
import face_recognition
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from moviepy.editor import ImageSequenceClip, VideoFileClip
from moviepy.video.fx.all import blackwhite, colorx, invert_colors, mirror_x, rotate, speedx


def brightness_filter(video_path, factor):
    clip = VideoFileClip(video_path)
    return clip.fx(colorx, factor=factor)


def slow_motion_filter(video_path, factor):
    clip = VideoFileClip(video_path)
    return clip.fx(speedx, factor=factor)


def mirror_filter(video_path):
    clip = VideoFileClip(video_path)
    return clip.fx(mirror_x)


def rotate_filter(video_path, angle):
    clip = VideoFileClip(video_path)
    return clip.fx(rotate, angle=angle)


def black_and_white_filter(video_path):
    clip = VideoFileClip(video_path)
    return clip.fx(blackwhite)


def invert_colors_filter(video_path):
    clip = VideoFileClip(video_path)
    return clip.fx(invert_colors)


def substitute_face(video_path, substitute_image_path):
    clip = VideoFileClip(video_path)
    substitute_clip = VideoFileClip(substitute_image_path)
    substitute_image = substitute_clip.get_frame(0)

    def process_frame(frame):
        frame = np.array(frame)
        face_locations = face_recognition.face_locations(frame)

        for face_location in face_locations:
            top, right, bottom, left = face_location
            substitute_face = substitute_clip.get_frame(0)[top:bottom, left:right].copy()
            frame[top:bottom, left:right, :] = substitute_face

        return frame

    return clip.fl_image(process_frame)


def load_esrgan_model():
    esrgan_model_url = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
    return hub.load(esrgan_model_url)


def apply_super_resolution(video_path):
    video_clip = VideoFileClip(video_path)
    frames = [frame for frame in video_clip.iter_frames(fps=video_clip.fps)]
    esrgan_model = load_esrgan_model()
    processed_frames = []

    for frame in frames:
        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        frame_lr = cv2.resize(frame_bgr, (frame_bgr.shape[1] // 4, frame_bgr.shape[0] // 4))
        frame_lr = frame_lr.astype(np.float32) / 255.0  # Convert to float32
        frame_sr = esrgan_model(tf.constant([frame_lr]), training=False)[0].numpy()
        frame_sr = np.clip(frame_sr * 255, 0, 255).astype(np.uint8)
        frame_rgb = cv2.cvtColor(frame_sr, cv2.COLOR_BGR2RGB)
        processed_frames.append(frame_rgb)

    return ImageSequenceClip(processed_frames, fps=video_clip.fps)
