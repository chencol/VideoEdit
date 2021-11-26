import os

cur_dir = os.getcwd()
file_list = os.listdir(cur_dir)
for file in file_list:
    if 'png' in file or ("mp4" in file and 'pianwei'
                         not in file) or 'wav' in file or 'array' in file:
        os.remove(file)