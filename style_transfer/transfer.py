from cv2 import cv2
import time
import os
 
def style_transfer(pathIn='',model='',width=None):
 
    '''
    pathIn: 原始图片的路径
    pathOut: 风格化图片的保存路径
    model: 预训练模型的路径
    width: 设置风格化图片的宽度，默认为None, 即原始图片尺寸
    jpg_quality: 0-100，设置输出图片的质量，默认80，越大图片质量越好
    '''
 
    ## 读入原始图片，调整图片至所需尺寸，然后获取图片的宽度和高度
    img = cv2.imread(pathIn)
    (h, w) = img.shape[:2]
    if width is not None:
        img = cv2.resize(img, (width, round(width*h/w)), interpolation=cv2.INTER_CUBIC)
        (h, w) = img.shape[:2]
    
    ## 从本地加载预训练模型
    print('加载预训练模型......%s'%model)
    net = cv2.dnn.readNetFromTorch(model)
    
    ## 将图片构建成一个blob：设置图片尺寸，将各通道像素值减去平均值（比如ImageNet所有训练样本各通道统计平均值）
    ## 然后执行一次前馈网络计算，并输出计算所需的时间
    blob = cv2.dnn.blobFromImage(img, 1.0, (w, h), (103.939, 116.779, 123.680), swapRB=False, crop=False)
    net.setInput(blob)
    start = time.time()
    output = net.forward()
    end = time.time()
    print("风格迁移花费：{:.2f}秒".format(end - start))
 
    ## reshape输出结果, 将减去的平均值加回来，并交换各颜色通道
    output = output.reshape((3, output.shape[2], output.shape[3]))
    output[0] += 103.939
    output[1] += 116.779
    output[2] += 123.680
    output = output.transpose(1, 2, 0)
    
    return output
 
def main(model_dir,img_path,save_dir):
    model_name = os.listdir(model_dir)
    for name in model_name:
        if name.split(".")[-1] == "t7":
            model_path = os.path.join(model_dir,name)
            output = style_transfer(img_path, model_path, width=500)
            save_path = os.path.join(save_dir,name+".jpg")
            cv2.imwrite(save_path, output, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
 
if __name__ == "__main__":
    model_dir = "./models"
    img_path = './bk.jpeg'
    save_dir = "./saveimgs6"
    main(model_dir,img_path,save_dir)