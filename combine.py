import moviepy.editor as mp
import os
from PIL import Image
import subprocess
from moviepy.editor import *
import numpy as np
import IPython.display as ipd
import librosa
import matplotlib.pyplot as plt
import pandas as pd
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.io.VideoFileClip import VideoFileClip
from pytube import YouTube

clips_to_be_combined = [VideoFileClip("1.mp4"), VideoFileClip("2.mp4")]

# clips_to_be_combined.append(VideoFileClip("newpianwei.mp4"))
print("Combining video.......................")
video = concatenate_videoclips(clips_to_be_combined, method='compose')
video.write_videofile('wangchuqinyuanlicen.mp4', threads=32)
