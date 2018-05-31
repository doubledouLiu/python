##-*- coding: utf-8 -*-
__author__ = 'liudoudou'

from PIL import Image, ImageDraw, ImageFont, ImageFilter


if __name__ == "__main__":

    #format：源文件的文件格式
    image = Image.open("D:\\test\\image\\code.png")
    print(image.format)


