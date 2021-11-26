from pytube import YouTube

video_file = "https://www.youtube.com/watch?v=OfhO3UX8elc"
yt = YouTube(video_file)
yt.streams.filter(progressive=True,
                  file_extension='mp4').order_by('resolution')[-1].download()

#you-get --format=mp4hd2v2 https://v.youku.com/v_show/id_XNDE3MDIzNTM3Ng==.html?spm=a2h0c.8166622.PhoneSokuUgc_2.dtitle