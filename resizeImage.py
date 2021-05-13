from PIL import Image
import os, sys

path = ('C:/Users/markaustin/Desktop/Thesis/Datasets/Exp_Batch_12/IFMD//')
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((128,128), Image.ANTIALIAS)
            imResize.save(f + '.jpg', 'JPEG', quality=90)
            print('Successfully Resized ' + f)

resize()

path = ('C:/Users/markaustin/Desktop/Thesis/Datasets/Exp_Batch_12/CFMD//')
dirs = os.listdir( path )

def resize():
    for item in dirs:
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            f, e = os.path.splitext(path+item)
            imResize = im.resize((128,128), Image.ANTIALIAS)
            imResize.save(f + '.jpg', 'JPEG', quality=90)
            print('Successfully Resized ' + f)

resize()