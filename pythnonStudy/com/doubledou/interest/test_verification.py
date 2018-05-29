##-*- coding: utf-8 -*-
__author__ = 'liudoudou'

import random
import string
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

number=4


#生成随机字符串
def rnd_str(number):
    source = list(string.letters)

    for index in range(1, 10):
        source.append(str(index))
    return "".join(random.sample(source, number))


#生成随机颜色
def rnd_color():
    return (random.randint(64, 255), random.randint(64,255), random.randint(64,255))


def rnd_line(draw,width,height):
    begin = (random.randint(0, width), random.randint(0, height))
    end = (random.randint(0, width), random.randint(0, height))
    draw.line([begin, end], fill = rnd_color())

#生成字符验证码图片
def rnd_picture(height, width, index):
    image = Image.new('RGB', (width, height), (255, 255, 255))  #绘制白色画布
    draw = ImageDraw.Draw(image)    #绘画对象
    # for i in range(width):      #随机逐像素填充背景颜色
    #     for j in range(height):
    #         draw.point((i, j), fill=rnd_color())

    font = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", 25)     #设置验证码的字体和大小
    text = rnd_str(number)
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text, font=font, fill=rnd_color())  #文本绘画

    rnd_line(draw,width,height)  #绘制干扰线
    image = image.transform((width+30, height+10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)  #图片放射和双线性
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强
    image.save('D://test//image//code' + str(index) + '.png')  #保存验证码图片
    #image.show()


if __name__ == "__main__":
    for index in range(0,100):
        rnd_picture(30, 100, index)









