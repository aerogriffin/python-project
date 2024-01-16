import face_recognition
import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
import cv2
from moviepy.editor import VideoFileClip, ImageSequenceClip
from moviepy.video.fx.all import colorx, speedx, mirror_x, rotate, blackwhite, invert_colors


def brightness_filter(video_path, factor):
    clip = VideoFileClip(video_path)
    brightness_clip = clip.fx(colorx, factor=factor)
    return brightness_clip

def slow_motion_filter(video_path, factor):
    clip = VideoFileClip(video_path)
    slowed_clip = clip.fx(speedx, factor=factor)
    return slowed_clip

def mirror_filter(video_path):
    clip = VideoFileClip(video_path)
    mirrored_clip = clip.fx(mirror_x)
    return mirrored_clip

def rotate_filter(video_path, angle):
    clip = VideoFileClip(video_path)
    rotated_clip = clip.fx(rotate, angle=angle)
    return rotated_clip

def black_and_white_filter(video_path):
    clip = VideoFileClip(video_path)
    bw_clip = clip.fx(blackwhite)
    return bw_clip

def invert_colors_filter(video_path):
    clip = VideoFileClip(video_path)
    inverted_clip = clip.fx(invert_colors)
    return inverted_clip

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
    
    result_clip = clip.fl_image(process_frame)
    
    return result_clip


def load_esrgan_model():
    esrgan_model_url = "https://tfhub.dev/captain-pool/esrgan-tf2/1"
    esrgan_model = hub.load(esrgan_model_url)
    return esrgan_model

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

    processed_clip = ImageSequenceClip(processed_frames, fps=video_clip.fps)
    
    return processed_clip
