from cv2 import cv2
import os
from PIL import Image, ImageFilter
import numpy as np
from moviepy.editor import *

def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    # return np.asarray(img)

video_prefix = '[105]Tamami Sakaguchi'
base_folder = 'D:/Documents/Downloads/images/' + video_prefix + '/'
image_folder = base_folder + 'full/'
audio_name = base_folder + '爱你就像爱生命.mp3'
video_hor_name = video_prefix + '_hor.mp4'
video_ver_name = video_prefix + '_ver.mp4'
video_hor_path = base_folder + video_hor_name
video_ver_path = base_folder + video_ver_name




# class of video generator
class videoGen:
    def __init__(self, width, height, image_folder, video_name):
        self.width = width
        self.height = height
        self.image_folder = image_folder
        self.video_name = video_name

    def image_resize(self, image_file):
        height, width, channels = image_file.shape
        ratio = 0.0
        if height / self.height > width / self.width:
            ratio = self.height / height
        else:
            ratio = self.width / width
        return cv2.resize(image_file, (int(width * ratio), int(height * ratio)))

    def backgrounded(self, image_file):
        img_height, img_width, channels = image_file.shape
        img = convert_from_cv2_to_image(image_file)
        bk = Image.new('RGB', (self.width, self.height), (0, 0, 0))
        # bk_img_big = bk_img.resize((img_width * 4, img_height * 4)).filter(ImageFilter.GaussianBlur(radius=6))
        # bk_img_big = convert_from_cv2_to_image(cv2.xphoto.oilPainting(cv2.resize(image_file, (img_width * 4, img_height * 4), interpolation = cv2.INTER_AREA), 7, 1))
        bk.paste(img, (int(self.width/2 - img_width/2), int(self.height/2 - img_height/2)))
        return convert_from_image_to_cv2(bk)

    def gen_video(self):
        images = [img for img in os.listdir(self.image_folder)]
        video = cv2.VideoWriter(self.video_name,cv2.VideoWriter_fourcc('M','J','P','G'), 1/3, (self.width, self.height))
        for image in images:
            print(image)
            resized_image = self.backgrounded(self.image_resize(cv2.imread(os.path.join(self.image_folder, image))))
            video.write(resized_image)
        video.release()

videoG = videoGen(1920, 1080, image_folder, video_hor_path)
videoG.gen_video()
videoG1 = videoGen(1080, 1920, image_folder, video_ver_path)
videoG1.gen_video()

if os.path.isdir(base_folder + video_prefix):
    print("当前目录下存在 result 文件夹")
else:
    print("当前目录下不存在 result 文件夹，调用 mkdir 创建该文件夹")
    os.mkdir(base_folder + video_prefix)

videoclip_hor = VideoFileClip(video_hor_path)
videoclip_ver = VideoFileClip(video_ver_path)
audioclip = AudioFileClip(audio_name)
new_audioclip = CompositeAudioClip([audioclip])

videoclip_hor.audio = new_audioclip
videoclip_hor.write_videofile(base_folder + video_prefix + '/' + video_hor_name)

videoclip_ver.audio = new_audioclip
videoclip_ver.write_videofile(base_folder + video_prefix + '/' + video_ver_name)

os.remove(video_hor_path)
os.remove(video_ver_path)
