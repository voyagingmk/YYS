
# -*- coding: utf-8 -*-

import cv2,numpy,time,os, random
from PIL import ImageGrab
from winsound import Beep

 #在背景查找目标图片，并返回查找到的结果坐标列表，target是背景，want是要找目标
def locate(target,want, show=0, msg=0):
    loc_pos=[]
    want,treshold,c_name=want[0],want[1],want[2]
    result=cv2.matchTemplate(target,want,cv2.TM_CCOEFF_NORMED)
    location=numpy.where(result>=treshold)

    if msg:  #显示正式寻找目标名称，调试时开启
        print(c_name,'searching... location', location)

    h,w=want.shape[:-1] #want.shape[:-1]

    n,ex,ey=1,0,0
    for pt in zip(*location[::-1]):    #其实这里经常是空的
        #print('pt', pt)
        x,y=pt[0]+int(w/2),pt[1]+int(h/2)
        if (x-ex)+(y-ey)<15:  #去掉邻近重复的点
            continue
        ex,ey=x,y

        cv2.circle(target,(x,y),10,(0,0,255),3)

        if msg:
            print(c_name,'we find it !!! ,at',x,y)
            
        x,y=int(x),int(y)
        loc_pos.append([x,y])

    if show:  #在图上显示寻找的结果，调试时开启
        cv2.imshow('we get',target)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

    if msg and len(loc_pos)==0:
        print(c_name,'not find')

    return loc_pos


#按【文件内容，匹配精度，名称】格式批量聚聚要查找的目标图片，精度统一为0.85，名称为文件名
def load_imgs():
    mubiao = {}
    path = os.getcwd() + '/jpg'
    file_list = os.listdir(path)

    for file in file_list:
        name = file.split('.')[0]
        file_path = path + '/' + file
        a = [ cv2.imread(file_path) , 0.85, name]
        mubiao[name] = a

    return mubiao

#蜂鸣报警器，参数n为鸣叫资料
def alarm(n):
    frequency = 1500
    last = 500

    for n in range(n):   
        Beep(frequency,last)
        time.sleep(0.05)

#裁剪图片以缩小匹配范围，screen为原图内容，upleft、downright是目标区域的左上角、右下角坐标
def cut(screen,upleft,downright): 

    a,b=upleft
    c,d=downright
    screen=screen[b:d,a:c]

    return screen

#随机偏移坐标，防止游戏的外挂检测。p是原坐标，w、n是目标图像宽高，返回目标范围内的一个随机坐标
def cheat(p, w, h):
    a,b = p
    w, h = int(w/4), int(h/4)
    c,d = random.randint(-w, w),random.randint(-h, h)
    e,f = a + c, b + d
    y = [e, f]
    return(y)