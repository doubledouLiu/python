##-*- coding: utf-8 -*-
__author__ = 'liudoudou'

import random
import string
import sys
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter


#生成随机字符串
def rnd_str(number):
    source = list(basestring.letters)

    for index in range(1, 10):
        source.append(str(index))
    return "".join(random.sample(source, number))


#生成随机颜色
def rnd_color():
    return (random.randint(64, 255), random.randint(64,255), random.randint(64,255))


#生成字符验证码图片
def rnd_picture(height, width):
    image = Image.new('RGB', (width, height), (255, 255, 255))  #绘制白色画布
    draw = ImageDraw.Draw(image)    #绘画对象
    for i in range(width):      #随机逐像素填充背景颜色
        for j in range(height):
            draw.point((i, j), fill=rnd_color())







