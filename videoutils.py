import os

from PIL import Image
from moviepy.editor import AudioFileClip, TextClip, VideoFileClip
from moviepy.video import fx
from moviepy.video.fx import all as vfx
from moviepy.video.io.ffmpeg_tools import concatenate_videoclips


def cut_video(input_path, output_path, start, end):
    clip = VideoFileClip(input_path).subclip(start, end)
    clip.write_videofile(output_path)


def join_videos(input_paths, output_path):
    clips = [VideoFileClip(path) for path in input_paths]
    final_clip = concatenate_videoclips(clips)
    final_clip.write_videofile(output_path)


def apply_slow_motion_effect(input_path, output_path, factor):
    clip = VideoFileClip(input_path).fx(fx.speedx, factor)
    clip.write_videofile(output_path)


def add_text_to_video(input_path, output_path, texto, posicion="bottom", duracion=None):
    clip = VideoFileClip(input_path)
    texto_clip = TextClip(texto, fontsize=24, color="white", bg_color="black")
    video_editado = clip.set_pos(posicion).set_duration(duracion).overlay(texto_clip, position=(10, 10))
    video_editado.write_videofile(output_path)


def add_music_to_video(video_path, music_path, output_path):
    video_clip = VideoFileClip(video_path)
    music_clip = AudioFileClip(music_path)

    video_with_music = video_clip.set_audio(music_clip)
    video_with_music.write_videofile(output_path)


def resize_video(video_path, output_path, new_width, new_height):
    video_clip = VideoFileClip(video_path)
    resized_video = video_clip.resize(width=new_width, height=new_height)
    resized_video.write_videofile(output_path)


def apply_color_filter(video_path, output_path, color="sepia"):
    video_clip = VideoFileClip(video_path)
    filtered_video = video_clip.fx(vfx.colorx, factor=0.5, rgb=color)
    filtered_video.write_videofile(output_path)


def split_into_frames(video_path, output_folder):
    video_clip = VideoFileClip(video_path)
    frames = video_clip.iter_frames(fps=1, dtype="uint8")

    for i, frame in enumerate(frames):
        image = Image.fromarray(frame)
        image.save(os.path.join(output_folder, f"frame_{i}.png"))


def overlay_videos(video1_path, video2_path, output_path):
    video1_clip = VideoFileClip(video1_path)
    video2_clip = VideoFileClip(video2_path)

    overlaid_video = video1_clip.set_pos(("center", "center")).set_duration(video2_clip.duration)
    overlaid_video = overlaid_video.overlay(video2_clip, position=("center", "center"))

    overlaid_video.write_videofile(output_path)
