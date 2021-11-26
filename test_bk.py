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


def download_video(link):
    yt = YouTube(link)
    yt.streams.filter(
        progressive=True,
        file_extension='mp4').order_by('resolution')[-1].download()


def save_energy_to_file(energy_array):
    file = open("energy_array.txt", "wb")
    # save array to the file
    np.save(file, energy_array)
    # close the file
    file.close


def load_energy_file_to_array():
    # open the file in read binary mode
    file = open("energy_array.txt", "rb")
    #read the file to numpy array
    arr1 = np.load(file)
    #close the file
    return arr1


def get_video_file():
    cur_dir = os.getcwd()
    file_list = os.listdir(cur_dir)
    video_file = ""
    audio_file_existed = False
    for file in file_list:
        if 'mp4' in file and not 'high' in file and not 'pianwei' in file:
            video_file = file
    return video_file


def show_graph():
    print("Generating graph for the video")
    cur_dir = os.getcwd()
    file_list = os.listdir(cur_dir)
    video_file = ""
    audio_file_existed = False
    energy_file_existed = False
    video_file = get_video_file()
    for file in file_list:
        if 'wav' in file:
            audio_file_existed = True
            audio_file = file
        if "energy_array" in file:
            energy_file_existed = True
    if not audio_file_existed:
        print("Processing file %s" % video_file)
        audio_file = video_file.split(".")[0] + ".wav"
        my_clip = mp.VideoFileClip(video_file)
        my_clip.audio.write_audiofile(audio_file)
        print("Audio file %s has been generated from %s" %
              (audio_file, video_file))
    if not energy_file_existed:
        x, sr = librosa.load(audio_file)
        print(sr)
        int(librosa.get_duration(x, sr) / 60)
        max_slice = 5
        window_length = max_slice * sr
        a = x[21 * window_length:22 * window_length]
        ipd.Audio(a, rate=sr)
        energy = sum(abs(a**2))
        print(energy)
        fig = plt.figure(figsize=(14, 8))
        energy = np.array([
            sum(abs(x[i:i + window_length]**2))
            for i in range(0, len(x), window_length)
        ])
        # import matplotlib.pyplot as plt
        print("Enerygy data %s" % energy)
        print("Type: %s" % type(energy))
        save_energy_to_file(energy)
    else:
        energy = load_energy_file_to_array()
    plt.hist(energy)
    # plt.show()
    save_energy_to_file(energy)

    return energy


# Generate higlight clip


def generate_thumbnail_from_video(video_file):
    clip = VideoFileClip(video_file)  #
    # fbs = clip.reader.fps  # return number of frame per second
    # nframes = clip.reader.nframes  # return number of frame in the video
    # duration = clip.duration  # return duration of the video in second
    # max_duration = int(clip.duration) + 1
    frame_at_second = 0.01  # here is the time where you want to take the thumbnail at second, it should be smaller than max_duration
    frame = clip.get_frame(
        frame_at_second
    )  # Gets a numpy array representing the RGB picture of the clip at time frame_at_second
    new_image = Image.fromarray(frame)  # convert numpy array to image
    new_image.save(video_file.split(".")[0] + ".png")  # save the image


def adding_thumbnail_to_video(video_file):
    subprocess.call([
        'ffmpeg', '-i', video_file, '-i',
        video_file.split(".")[0] + ".png", '-map', '0', '-map', '1', '-c',
        'copy', '-c:v:1', 'png', '-disposition:v:1', 'attached_pic',
        video_file.split(".")[0] + "_modified.mp4", '-y'
    ])


# video_file = get_video_file()
# energy = show_graph()


def determine_clips_number(energy, thresh, duration):
    df = pd.DataFrame(columns=['energy', 'start', 'end'])
    row_index = 0
    for i in range(len(energy)):
        value = energy[i]
        if (value >= thresh):
            i = np.where(energy == value)[0]
            df.loc[row_index, 'energy'] = value
            df.loc[row_index, 'start'] = i[0] * 5
            df.loc[row_index, 'end'] = (i[0] + 1) * 5
            row_index = row_index + 1

    temp = []
    i = 0
    j = 0
    n = len(df) - 2
    m = len(df) - 1
    while (i <= n):
        j = i + 1
        while (j <= m):
            if (df['end'][i] == df['start'][j]):
                df.loc[i, 'end'] = df.loc[j, 'end']
                temp.append(j)
                j = j + 1
            else:
                i = j
                break

    df.drop(temp, axis=0, inplace=True)

    start = np.array(df['start'])
    end = np.array(df['end'])
    count = 0
    number_of_clips = 0
    for i in range(len(df)):
        if (i != 0):
            start_lim = start[i] - 5
        else:
            start_lim = start[i]
        end_lim = end[i]
        if end_lim - start_lim >= duration:
            number_of_clips = number_of_clips + 1

    return number_of_clips


def generate_clips(energy, thresh, duration):
    print("Current thres is %s" % thresh)
    print("Current duration is %s" % duration)
    print("Gnerating clips.......")
    df = pd.DataFrame(columns=['energy', 'start', 'end'])
    # thresh = 10
    row_index = 0
    for i in range(len(energy)):
        value = energy[i]
        if (value >= thresh):
            i = np.where(energy == value)[0]
            df.loc[row_index, 'energy'] = value
            df.loc[row_index, 'start'] = i[0] * 5
            df.loc[row_index, 'end'] = (i[0] + 1) * 5
            row_index = row_index + 1

    temp = []
    i = 0
    j = 0
    n = len(df) - 2
    m = len(df) - 1
    while (i <= n):
        j = i + 1
        while (j <= m):
            if (df['end'][i] == df['start'][j]):
                df.loc[i, 'end'] = df.loc[j, 'end']
                temp.append(j)
                j = j + 1
            else:
                i = j
                break

    df.drop(temp, axis=0, inplace=True)

    start = np.array(df['start'])
    end = np.array(df['end'])
    count = 0
    # number_of_clips = 0
    # for i in range(len(df)):
    #     if (i != 0):
    #         start_lim = start[i] - 5
    #     else:
    #         start_lim = start[i]
    #     end_lim = end[i]
    #     if end_lim - start_lim >= duration:
    #         number_of_clips = number_of_clips + 1
    # print("Number of clips to generate: %s" % (len(df)))
    # proceed_to_generate_clips = input(
    #     "Proceed to generate clips for combination?:\n")
    # if proceed_to_generate_clips == "yes":

    ##############################
    ##############################
    # duration_clips = 8
    video_file = get_video_file()
    for i in range(len(df)):
        if (i != 0):
            start_lim = start[i] - 5
        else:
            start_lim = start[i]
        end_lim = end[i]
        if i < (len(df) - 1):
            if end_lim - start_lim >= duration:
                filename = "highlight" + str(count + 1) + ".mp4"
                print("Generating clip %s" % (filename))
                with VideoFileClip(video_file) as video:
                    new = video.subclip(start_lim, end_lim)
                    new.write_videofile(filename,
                                        audio_codec='aac',
                                        threads=32,
                                        verbose=False,
                                        logger=None,
                                        fps=24)
                    del new
                    generate_thumbnail_from_video(filename)
                    count = count + 1
        else:
            if end_lim - start_lim >= duration:
                filename = "highlight" + str(count + 1) + ".mp4"
                print("Generating clip %s" % (filename))
                with VideoFileClip(video_file) as video:
                    new = video.subclip(start_lim, end_lim)
                    new.write_videofile(filename,
                                        audio_codec='aac',
                                        threads=32,
                                        verbose=False,
                                        logger=None,
                                        fps=24)
                    del new
                    generate_thumbnail_from_video(filename)


def combine_clips():
    target_file_names = []
    cur_dir = os.getcwd()
    file_list = os.listdir(cur_dir)
    video_file = get_video_file()
    for file in file_list:
        if 'mp4' in file and "highlight" in file:
            target_file_names.append(file)

    target_file_names = sorted(
        target_file_names,
        key=lambda x: int(x.replace("highlight", "").split(".")[0]))
    print("sorted target file : %s" % (target_file_names))

    clips_to_be_combined = []
    for file in target_file_names:
        clips_to_be_combined.append(VideoFileClip(file))

    # clips_to_be_combined.append(VideoFileClip("newpianwei.mp4"))
    print("Combining video.......................")
    video = concatenate_videoclips(clips_to_be_combined, method='compose')
    video.write_videofile(
        "D:\\bilibili\\" + video_file + '_combined.mp4',
        threads=32,
        verbose=False,
        fps=24,
        logger=None,
    )


def get_combined_video_file_name():
    cur_dir = "D:\\bilibili\\"
    file_list = os.listdir(cur_dir)
    video_file = ""
    orignal_file_name = get_video_file()
    for file in file_list:
        if 'mp4' in file and not 'high' in file and not 'pianwei' in file and orignal_file_name in file:
            video_file = file
    print("Video need to be added with watermark is %s" % (video_file))
    return "D:\\bilibili\\" + video_file


def add_watermark():
    print("Adding watermark to the video................")
    video_file = get_combined_video_file_name()
    video = mp.VideoFileClip(video_file)
    logo1 = (mp.ImageClip("logo2.JPG").set_duration(
        video.duration).resize(0.4).set_pos(("right", "top")))

    # logo1 = (mp.ImageClip("logo.JPG").set_duration(
    #     video.duration).resize(1).margin(right=10, top=10).set_pos(
    #         ("right", "top")))

    logo2 = (mp.ImageClip("masaike.JPG").set_duration(
        video.duration).resize(0.27).set_pos(("left", "top")))

    logo3 = (mp.ImageClip("masaike.JPG").set_duration(
        video.duration).resize(0.27).set_pos(("right", "bottom")))

    # To be remove when not necessary
    #logo4 = (mp.ImageClip("masaike.JPG").set_duration(
    #video.duration).resize(0.6).set_pos(("right", "top")))

    final = mp.CompositeVideoClip([video, logo1, logo2, logo3])
    final.write_videofile("D:\\bilibili\\" + get_video_file() +
                          "_combined_watermark.mp4",
                          audio_codec='aac',
                          threads=32,
                          verbose=False,
                          logger=None,
                          fps=24)
    os.remove(video_file)


def calculate_thres_value(energy):
    video = mp.VideoFileClip(get_video_file())
    print("Total video duration : %s minutes" % (int(video.duration / 60)))
    minutes = int(video.duration / 60)
    if minutes < 10:
        lower_limit = int(minutes)
        upper_limit = int(minutes) + 1
    else:
        lower_limit = int(minutes / 10) * 10
        upper_limit = int((minutes / 10 + 1)) * 10
    print("Lower limit : %s" % lower_limit)
    print("Upper limit : %s" % upper_limit)
    proceed = True
    max_value = int(max(energy))
    print("Max value from energy %s" % max_value)
    thresh = max_value
    duration = 5
    while proceed:
        count = determine_clips_number(energy, thresh, duration)
        print("Thresh : %s with count %s" % (thresh, count))
        if count >= (lower_limit + upper_limit) / 2:
            # if count > lower_limit and count <= upper_limit:
            proceed = False
            return thresh, duration
        else:
            thresh = thresh - 1


def remove_everything():
    cur_dir = os.getcwd()
    file_list = os.listdir(cur_dir)
    for file in file_list:
        print(file)
        if 'png' in file or ("mp4" in file
                             and 'pianwei' not in file) or 'wav' in file:
            os.remove(file)


video_file = get_video_file()
if not video_file:
    link = "https://www.youtube.com/watch?v=RL2WT0dT2dk"
    download_video(link)
energy = show_graph()
toCombine = "No"
regenerate = True
first_round = True

while regenerate:
    toCombine = input("Proceed to combine?:\n")
    if toCombine == "yes":
        combine_clips()
        regenerate = False
    else:
        # print("Generate clips")
        # thresh = input("Please enter your thres value:\n")
        # duration = input("Please enter your duration value:\n")
        thresh, duration = calculate_thres_value(energy)
        generate_clips(energy, float(thresh), float(duration))

add_watermark()
