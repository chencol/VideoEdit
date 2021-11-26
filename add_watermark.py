import moviepy.editor as mp

video_file = "diyaszhangben.mp4"
video = mp.VideoFileClip(video_file)
logo2 = (mp.ImageClip("logo5.JPG").set_duration(
    video.duration).resize(0.4).set_pos((lambda t: ('right', 70 + t))))

logo1 = (mp.ImageClip("logo2.JPG").set_duration(
    video.duration).resize(0.4).margin(right=10, top=10).set_pos(
        ("left", "top")))
# logo1 = (mp.ImageClip("logo5.JPG").set_duration(
#     video.duration).resize(0.4).set_pos(("right", "top")))
# logo2 = (mp.ImageClip("logo3.JPG").set_duration(
#     video.duration).resize(0.4).set_pos(("right", "bottom")))

# logo2 = (mp.ImageClip("logo5.JPG").set_duration(
#     video.duration).resize(0.4).set_pos((lambda t: ('right', 70 + t))))

# logo2 = (mp.ImageClip("logo5.JPG").set_duration(
#     video.duration).resize(0.2).set_pos((lambda t: ('right', 70 + t))))

# # logo1 = (mp.ImageClip("logo2.JPG").set_duration(
# #     video.duration).resize(0.4).margin(right=10, top=10).set_pos(
# #         ("left", "top")))

# # logo3 = (mp.ImageClip("logo8.PNG").set_duration(
# #     video.duration).resize(0.4).set_pos(("left", "top")))

# logo6 = (mp.ImageClip("masaike.JPG").set_duration(
#     video.duration).resize(0.38).set_pos(("right", "bottom")))

# logo3 = (mp.ImageClip("masaike.JPG").set_duration(
#     video.duration).resize(0.27).set_pos(("right", "bottom")))

# logo3 = (mp.ImageClip("logo8.PNG").set_duration(
#     video.duration).resize(0.4).margin(right=10, top=10).set_pos(
#         ("left", "top")))

# logo3 = (mp.ImageClip("logo8.PNG").set_duration(
#     video.duration).resize(0.4).set_pos(("left", "top")))

final = mp.CompositeVideoClip([video, logo1, logo2])
final.write_videofile(video_file + "_watermark.mp4",
                      audio_codec='aac',
                      threads=32,
                      verbose=False,
                      logger=None)
