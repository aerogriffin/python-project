from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import colorx


def brightness_filter(video_path, factor):
    clip = VideoFileClip(video_path)
    return clip.fx(colorx, factor=factor)
