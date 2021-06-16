import numpy as np
import random
import cv2
import os
import shutil
def GaussianBlur(source, var):
    src = cv2.imread(source)
    #第二个参数：高斯核的宽和高（建议是奇数），越大越模糊
    #第三个参数：x和y轴的标准差，标准差越大越模糊
    result = cv2.GaussianBlur(src, (45, 45), var)
    return result
    #

def sp_noise(image,prob):
    '''
    添加椒盐噪声
    prob:噪声比例
    '''
    output = np.zeros(image.shape, np.uint8)
    thres = 1 - prob
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            rdn = random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = image[i][j]
    cv2.imwrite('result/result.jpg', output)


def gasuss_noise(image, mean=0, var=0.001):
    '''
        添加高斯噪声
        mean : 均值
        var : 方差
    '''
    image = np.array(image/255, dtype=float)
    noise = np.random.normal(mean, var ** 0.5, image.shape)
    out = image + noise
    if out.min() < 0:
        low_clip = -1.
    else:
        low_clip = 0.
    out = np.clip(out, low_clip, 1.0)
    out = np.uint8(out*255)
    return out


def image_process(path, worker, label):
    blur_var = np.linspace(1, 10, 10)
    # noise_var = np.linspace(0, 0.01, 10)
    i = 0
    for source in path:
        new_name = str(i) + 'sample' + str(label) + '.jpg'
        des = os.path.join('./dataset/'+str(worker), new_name)
        print(des)
        blur = GaussianBlur(source, blur_var[i])
        # result = gasuss_noise(blur, mean=0, var = noise_var[i])
        cv2.imwrite(des, blur)
        i = i + 1

#
# dict = {'n02106662': 0, 'n02109961': 1, 'n02110341': 2, 'n02111277': 3}  #规定的类别顺序

if __name__ == '__main__':
    # label = 0
    # for root, ds, fs in os.walk('E:\Crowdsourced Data\ImageNet_Dog'):
    #     if len(fs) > 0:
    #         image_list = random.sample(fs, 200)
    #         for i in range(20):
    #             ten = image_list[i*10: i*10+10]
    #             path = []
    #             for name in ten:
    #                 path.append(os.path.join(root, name))
    #             image_process(path, i, label)
    #         label += 1

    # 对于每一类图片，应该增加模糊，作为增加任务的难度，设置一半的任务都比较模糊，可以设置梯度模糊，
    dogs = ['n02085936', 'n02088364', 'n02091134', 'n02087046']
    for j in range(4):
        for root, ds, fs in os.walk('E:\CrowdsourcedData\ILSVRC2012\\' + dogs[j]):
            image_list = random.sample(fs, 150) #每个类别选择100个任务，50个保持原样，50个进行模糊处理
            for i in range(50):
                path = os.path.join(root, image_list[i])
                shutil.copy(path, 'E:\CrowdsourcedData\ILSVRC2012\selfpaced4\\' + str(j+1) + '_清晰')
            for i in range(50, 150):
                path = os.path.join(root, image_list[i])
                blur = GaussianBlur(path, 8)

                cv2.imwrite(os.path.join('E:\CrowdsourcedData\ILSVRC2012\selfpaced4\\' + str(j+1) + '_blur', image_list[i]), blur)








