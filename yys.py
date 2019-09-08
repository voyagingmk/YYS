# -*- coding: utf-8 -*-

import cv2,numpy,time,random
import os,sys,pyautogui, traceback
from PIL import ImageGrab, Image
import action
import win32gui, win32ui, win32con
import win32api
import win32con

# 读取文件 精度控制   显示名字
imgs = action.load_imgs()
pyautogui.PAUSE = 0.1

start_time = time.time()
print('程序启动，现在时间', time.ctime())


#获取后台窗口的句柄，注意后台窗口不能最小化
hWnd = win32gui.FindWindow("Win32Window0",None) #窗口的类名可以用Visual Studio的SPY++工具获取
#返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
hWndDC = win32gui.GetWindowDC(hWnd)
#创建设备描述表
mfcDC = win32ui.CreateDCFromHandle(hWndDC)
#创建内存设备描述表
saveDC = mfcDC.CreateCompatibleDC()
#获取句柄窗口的大小信息
left, top, right, bot = win32gui.GetWindowRect(hWnd)
width = right - left
height = bot - top
#创建位图对象准备保存图片
saveBitMap = win32ui.CreateBitmap()
#为bitmap开辟存储空间
saveBitMap.CreateCompatibleBitmap(mfcDC,width,height)

def sim_click(x, y):
    lParam = win32api.MAKELONG(x, y)
    win32api.SendMessage(hWnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lParam)
    win32api.SendMessage(hWnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, lParam)

def screenshot():
    #将截图保存到saveBitMap中
    saveDC.SelectObject(saveBitMap)
    #保存bitmap到内存设备描述表
    saveDC.BitBlt((0,0), (width,height), mfcDC, (0, 0), win32con.SRCCOPY)
    ###获取位图信息
    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)
    ###生成图像
    im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
    ##方法二（第二部分）：PIL保存
    ###PrintWindow成功,保存到文件,显示到屏幕
    im_PIL.save("screen.jpg", 'jpeg')


#以上启动，载入设置
##########################################################

def log(f):
    def wrap(*agrs, **kwagrs):
        try:
            ans = f(*agrs, **kwagrs)
            return ans
        except:
            traceback.print_exc()
            time.sleep(60)

    return wrap

@log
def select_mode():
    print(u'''\n菜单：  鼠标移动到最右侧中止并返回菜单页面, 
        1 结界自动合卡，自动选择前三张合成 
        2 自动通关魂十，自动接受组队并确认通关
        3 自动通关业原火，单刷
        4 自动刷组队狗粮（打手模式），          
        5 单刷探索副本，无法区分经验BUFF
        ''')
    #action.alarm(1)
   #raw = input(u"选择功能模式：")
    index = 2#int(raw)

    mode = [0, card, yuhun, yeyuanhuo, goliang, solo]
    comand = mode[index]
    comand()

##########################################################
#合成结界卡，较简单，未偏移直接点
def card():
    while True:
        #鼠标移到右侧中止    
        # if pyautogui.position()[0] >= pyautogui.size()[0] * 0.7:
        #     select_mode()
            
        x, y, z = (370, 238), (384, 385), (391, 525)  #前三张卡的位置
        zz = (840, 605)               #合成按钮位置
        for i in [x, y, z ,zz]:
            pyautogui.click(i[0] + random.randint(0,30),i[1] + random.randint(0,30) )
            time.sleep(0.1)
        time.sleep(2)


########################################################
#魂十通关
def yuhun():
    while True :
        #鼠标移到最右侧中止    
        # if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
        #     sys.exit(0)

        print('ImageGrab.grab',time.ctime())
        screenshot()
        screen = cv2.imread('screen.jpg')


        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1150, 690) #上部并排

        a,b = upleft
        c,d = downright
        #screen = screen[b:d,a:c]

        print('screen shot ok',time.ctime())
        
        #设定目标，开始查找
        #这里是自动接受组队
        # for i in ['jieshou2',"jieshou"]:
        #     want = imgs[i]
        #     size = want[0].shape
        #     h, w , ___ = size
        #     x1,x2 = upleft, (430, 358)
        #     target = action.cut(screen, x1, x2)
        #     pts = action.locate(target,want,0)
        #     if not len(pts) == 0:
        #         print('接受组队')
        #         xx = pts[0]
        #         xx = action.cheat(xx, w, h)
        #         if xx[0] > 120:           
        #             pyautogui.click(xx)
        #             t = random.randint(40,80) / 100
        #             time.sleep(t)
        #             break
        #         else:
        #             pass
        #         continue

        mini = {
            'jixu1': (500, 400 ),
        }
        offset = {
            'shuju': (340, 360 ),
        }
        sleep_delay = {
            'tiaozhan': random.randint(500, 1000)/1000,
            'shuju': random.randint(1000, 1500)/1000,
        }
        #自动点击通关结束后的页面
        #for i in ['hun11_0','hun11_1','hun11_2','hun11_3','jiangli2','gou','zhunbei' ]:
        #for i in ['tiaozhan','ying','gu','damo','gu2','jixu1' ]:#单刷
        #for i in ['tiaozhan','gu','shuju','jixu1']:#单刷
        for i in ['tianzhan11','gu','shuju']:#魂11队长
        #for i in ['gu','shuju','jixu1']:#队员刷
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            if i in mini:
                c,d = mini[i]
                target = target[b:d,a:c]
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                for pt in pts:
                    pt = action.cheat(pt, w, h)
                    if i in offset:
                        pt[0] += offset[i][0]
                        pt[1] += offset[i][1]
                    #pyautogui.click(pt)
                    print 'click', pt
                    sim_click(pt[0], pt[1])
                    time.sleep(sleep_delay.get(i,random.randint(100, 200)/1000))
                    break

########################################################
#业原火通关
def yeyuanhuo():
    while True :   #直到取消，或者出错
        #鼠标移到最右侧中止    
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            sys.exit(0)


        screen = ImageGrab.grab()
        screen.save('screen.jpg')
        screen = cv2.imread('screen.jpg')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1426, 798)

        a,b = upleft
        c,d = downright
        #screen = screen[b:d,a:c]

        print('screen shot ok',time.ctime())
        
        #设定目标，开始查找

        #过关
        for i in ['tiaozhan','ying','jiangli','jiangli2','333','ok' ]:
            want=imgs[i]
            size = want[0].shape
            h, w , ___ = size
            #print 'h', h, 'w',w, want[1], want[2]
            target=screen
            pts=action.locate(target,want,0,1)
            print 'pts', pts
            if not len(pts)==0:
                for pt in pts:
                    pt = action.cheat(pt, w, h)
                    print('click',pt[0],pt[1],want[2])
                    pyautogui.click(x=pt[0], y=pt[1],clicks=2)
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    t = random.randint(100,200) / 100
                    time.sleep(t)
                    break
                break
        

########################################################
    #狗粮通关
def goliang():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.jpg')
        screen = cv2.imread('screen.jpg')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 768)
        downright2 = (2550, 768)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        print('screen shot ok',time.ctime())
        
        #设定目标，开始查找
        #进入后
        want = imgs['guding']

        x1 = (785, 606)
        x2 = downright
        target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['xiao']
            x1,x2 = (5, 405), (119, 560)
            target = action.cut(screen, x1, x2)
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('组队状态中')
            else:
                print('退出重新组队')
                
                for i in ['queren', 'tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    x1,x2 = upleft, (965, 522)
                    target = action.cut(screen, x1, x2)
                    pts = action.locate(target,want,0)
                    if not len(pts) == 0:
                        print('退出中')
                        try:
                            queding = pts[1]
                        except:
                            queding = pts[0]
                        queding = action.cheat(queding, w, h)
                        pyautogui.click(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        want = imgs['jieshou']
        size = want[0].shape
        h, w , ___ = size
        x1,x2 = upleft, (250, 380)
        target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('接受组队')
            xx = pts[0]
            xx = action.cheat(xx, w, h)
            if xx[0] > 120:           
                pyautogui.click(xx)
                t = random.randint(40,80) / 100
                time.sleep(t)
            else:
                pass
            continue

        for i in ['ying','jiangli','jixu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('领取奖励')
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                break

########################################################
#单人探索
def solo():
    while True:   #直到取消，或者出错
        if pyautogui.position()[0] >= pyautogui.size()[0] * 0.98:
            select_mode()

        screen = ImageGrab.grab()
        screen.save('screen.jpg')
        screen = cv2.imread('screen.jpg')

        #截屏，并裁剪以加速
        upleft = (0, 0)
        downright = (1358, 768)
        downright2 = (2550, 768)

        a,b = upleft
        c,d = downright
        screen = screen[b:d,a:c]

        print('screen shot ok',time.ctime())
        
        #设定目标，开始查找
        #进入后
        want=imgs['guding']

        x1 = (785, 606)
        x2 = downright
        target = action.cut(screen, x1, x2)
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('正在地图中')
            
            want = imgs['left']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                right = (854, 527)
                right = action.cheat(right, 10, 10)
                pyautogui.click(right)
                t = random.randint(50,80) / 100
                time.sleep(t)
                continue

            want = imgs['jian']
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('点击小怪')
                xx = action.cheat(pts[0], 10, 10)        
                pyautogui.click(xx)
                time.sleep(0.5)
                continue
            else:
                for i in ['queren', 'tuichu']:
                    want = imgs[i]
                    size = want[0].shape
                    h, w , ___ = size
                    x1,x2 = upleft, (965, 522)
                    target = action.cut(screen, x1, x2)
                    pts = action.locate(target,want,0)
                    if not len(pts) == 0:
                        print('退出中')
                        try:
                            queding = pts[1]
                        except:
                            queding = pts[0]
                        queding = action.cheat(queding, w, h)
                        pyautogui.click(queding)
                        t = random.randint(50,80) / 100
                        time.sleep(t)
                        break
                continue

        for i in ['ying','jiangli','jixu']:
            want = imgs[i]
            size = want[0].shape
            h, w , ___ = size
            target = screen
            pts = action.locate(target,want,0)
            if not len(pts) == 0:
                print('领取奖励')
                xy = action.cheat(pts[0], w, h-10 )
                pyautogui.click(xy)
                t = random.randint(15,30) / 100
                time.sleep(t)
                break

        want = imgs['tansuo']
        size = want[0].shape
        h, w , ___ = size
        target = screen
        pts = action.locate(target,want,0)
        if not len(pts) == 0:
            print('进入地图')
            xy = action.cheat(pts[0], w, h-10 )
            pyautogui.click(xy)
            t = random.randint(15,30) / 100
            time.sleep(t)

####################################################
if __name__ == '__main__':
    select_mode()

