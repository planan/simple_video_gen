#Combine videos and musics
import librosa
import os
from moviepy.video.fx import resize
from cv2 import cv2
from moviepy.editor import *

video_src = "C:/kakaverna/"
music_src = "D:/videosMake/music/midi2/"
result = "D:/videosMake/result"

def checkAndCreate(file_path):
    if os.path.isdir(file_path):
        print("当前目录下存在 result 文件夹")
    else:
        print("当前目录下不存在 result 文件夹，调用 mkdir 创建该文件夹")
        os.mkdir(file_path)

def emptyFile(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

def timeFormat(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "%d:%02d:%02d" % (h, m, s)

def musicMerge():
    infos = []
    total_duration = 0
    for root, dirs, files in os.walk(music_src):
        for filename in files:
            duration = librosa.get_duration(filename=os.path.join(music_src, filename))
            musicStart = timeFormat(total_duration)
            info = str(musicStart) + " - " + filename.split(".mp3")[0]
            print(info)
            infos.append(info)
            total_duration += duration
        l1 = [os.path.join(music_src, filename) for filename in files]
        checkAndCreate(music_src + 'merge/')
        emptyFile(os.path.join(music_src + 'merge/', 'music.mp3'))
        cmd = ('ffmpeg -i "concat:%s" -acodec copy %s' % ('|'.join(l1), os.path.join(music_src + 'merge/', 'music.mp3')))
        os.popen(cmd)
    return infos

def videoMerge():
    checkAndCreate(video_src + "merge/")
    emptyFile(video_src + "merge/" + "target.mp4")
    # 定义一个数组
    L = []
    # 访问 video 文件夹 (假设视频都放在这里面)
    for root, dirs, files in os.walk(video_src):
        # 按文件名排序
        files.sort()
        # 遍历所有文件
        for file in files:
            # 如果后缀名为 .mp4
            if os.path.splitext(file)[1] == '.mp4':
                # 拼接成完整路径
                L.append(VideoFileClip(os.path.join(root, file)).resize(height = 1080).on_color(size = (1920, 1080)))
    final_clips = concatenate_videoclips(L)
    # 生成目标视频文件
    final_clips.to_videofile(video_src + "merge/" + "result.mp4", fps=24, remove_temp=False, audio=False)
    

def genVideo():
    emptyFile(os.path.join(result,  "result.mp4"))
    cmd = ('ffmpeg -stream_loop -1 -i %s -i %s -shortest -map 0:v:0 -map 1:a:0 -y -c copy %s' % (os.path.join(video_src+'merge/',  "target.mp4"), os.path.join(music_src + 'merge/', 'music.mp3'), os.path.join(result,  "result.mp4")))
    os.popen(cmd)

def videoGen(infos):
    emptyFile(os.path.join(result,  "result1.mp4"))
    img = cv2.imread(os.path.join(video_src,  "cover1.jpg"))
    font = cv2.FONT_HERSHEY_SIMPLEX
    imgzi = cv2.resize(img, (1920, 1080))
    height = 40
    width = 5
    for info in infos:
        imgzi = cv2.putText(imgzi, info, (width, height), font, 1, (255, 255, 255), 2)
        height += 30
        if height >= 1080:
            height = 40
            width = 900
    cv2.imwrite(os.path.join(video_src,  "cover.jpg"), imgzi)
    cmd = ('ffmpeg -r 1 -loop 1 -i %s -i %s -acodec copy -r 1 -shortest -vf scale=1920:1080 %s' % (os.path.join(video_src,  "cover.jpg"), os.path.join(music_src + 'merge/', 'music.mp3'), os.path.join(result,  "result1.mp4")))
    os.popen(cmd)
    
    

# infos = musicMerge()
# videoGen(infos)
videoMerge()
# genVideo()