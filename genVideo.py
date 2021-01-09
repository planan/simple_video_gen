import cv2
import os
from PIL import Image, ImageFilter
import numpy as np
from moviepy.editor import *

def convert_from_cv2_to_image(img: np.ndarray) -> Image:
    # return Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    return Image.fromarray(img)


def convert_from_image_to_cv2(img: Image) -> np.ndarray:
    # return cv2.cvtColor(numpy.array(img), cv2.COLOR_RGB2BGR)
    return np.asarray(img)

base_folder = 'D:/Documents/Downloads/images/test/'

image_folder = base_folder + 'Hashimoto Nanami'
video_hor_name = base_folder + 'video_hor.mp4'
video_ver_name = base_folder + 'video_ver.mp4'
audio_name = base_folder + '/result/You Raise Me Up.mp3'



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
        bk = Image.new('RGB', (self.width, self.height), (255, 255, 255))
        bk_img = img.copy()
        bk_img_big = bk_img.resize((img_width * 4, img_height * 4)).filter(ImageFilter.GaussianBlur(radius=6))
        bk_img_result = bk_img_big.crop([img_width, img_height, self.width + img_width, self.height + img_height])
        bk.paste(bk_img_result, (0, 0))
        bk.paste(img, (int(self.width/2 - img_width/2), int(self.height/2 - img_height/2)))
        return convert_from_image_to_cv2(bk)

    def gen_video(self):
        images = [img for img in os.listdir(self.image_folder)]
        video = cv2.VideoWriter(self.video_name,cv2.VideoWriter_fourcc('M','J','P','G'), 1/3, (self.width, self.height))
        for image in images:
            resized_image = self.backgrounded(self.image_resize(cv2.imread(os.path.join(self.image_folder, image))))
            video.write(resized_image)
        video.release()




videoG = videoGen(1920, 1080, image_folder, video_hor_name)
videoG.gen_video()
videoG1 = videoGen(1080, 1920, image_folder, video_ver_name)
videoG1.gen_video()

audioclip = AudioFileClip(audio_name)
new_audioclip = CompositeAudioClip([audioclip])

videoclip_hor = VideoFileClip(video_hor_name)
videoclip_hor.audio = new_audioclip
videoclip_hor.write_videofile(video_hor_name)

videoclip_ver = VideoFileClip(video_ver_name)
videoclip_ver.audio = new_audioclip
videoclip_ver.write_videofile(video_ver_name)