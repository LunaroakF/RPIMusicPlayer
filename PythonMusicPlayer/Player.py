import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
import RPi.GPIO as GPIO
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import psutil as p
import os, re  
import subprocess
import threading
from pygame import mixer
import wave
import glob
import socket
import ctypes
import inspect

GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BCM)
channel = 18
GPIO.setup(channel, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.add_event_detect(channel, GPIO.RISING, bouncetime = 200)
GPIO.setup(23,GPIO.OUT)

IP="192.168.0.101"  #设备的内网IP
Port=23333  #监听的端口

if 1==1:   #Main
    Replay=False
    RST = None     
    DC = 23
    SPI_PORT = 0
    SPI_DEVICE = 0
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
    disp.begin()
    disp.clear()
    disp.display()
    width = disp.width
    height = disp.height
    image = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image)
    padding = -2
    top = padding
    bottom = height-padding
    maindate=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    maintime=time.strftime('%H:%M:%S',time.localtime(time.time()))
    x = 0
    draw.rectangle((0,0,width,height), outline=0, fill=0)
    mainroad='Fonts/'#'/home/pi/Documents/Programs/OLEDPrograms/Fonts/'
    retron=mainroad+'Retron2000.ttf'
    hanzi=mainroad+'Dengl.ttf'
    NowTimes=""
    AllTimes=""
    MusicName=""
    disp.clear()

def click():
    result = 0   #长按返回0，单击返回1，双击返回2
    for i in range(200):
        sig = GPIO.input(18)                             #输入的电平信号
        if sig == GPIO.LOW and result == 0:  #第一次发现没有在按着
            result = 1
        if result == 1 and sig == GPIO.HIGH:
            result = 2
            return result
        if i >= 100 and result != 0:  #如果不是长按，1秒内返回结果
            return result
        time.sleep(1.5)   
    return result

def Timeupdate():
    print("时钟已加载")
    while True:
        global maindate
        global maintime
        maindate=time.strftime('%Y-%m-%d',time.localtime(time.time()))
        maintime=time.strftime('%H:%M:%S',time.localtime(time.time()))
        
MainNext=False
def UserInput():
    return;#很迷的物理按钮控制，如果可以弄好就去掉前面的return
    print("用户控制已加载")
    mainbool=False   
    while True:
        click_time = click()
        if click_time !=1:
            mainbool=True
        else:
            GPIO.output(23,GPIO.LOW)
        if mainbool:
            global xiumianle
            global xiumiantime
            xiumiantime=0
            if xiumianle:
                xiumianle=False
            else:
                t_MusicPlay2 = threading.Thread(target=MusicPlay)
                global MainNext
                MainNext=True
                GPIO.output(23,GPIO.HIGH)
                time.sleep(0.01)
                GPIO.output(23,GPIO.LOW)
                global MusicName
                MusicName="Loading......"
                mainbool=False
                t_MusicPlay2.start() 
                try:
                    t_MusicPlay.stop()
                except:
                    print("")
                try:
                    t_MusicPlay3.stop()
                except:
                    print("")
                    
def ScreenUpdate():
    while True:
        global maindate
        global maintime
        global NowTimes
        global AllTimes
        global MusicName
        global Replay
        draw.rectangle((0,0,width,height), outline=0, fill=0)
        draw.text((x+85, top),maintime,  font=ImageFont.truetype(hanzi,12), fill=255)
        draw.text((x, top),maindate,  font=ImageFont.truetype(hanzi,12), fill=255)
        draw.text((x+10, top+40),NowTimes,  font=ImageFont.truetype(retron,13), fill=255)
        draw.text((x+90, top+40),AllTimes,  font=ImageFont.truetype(retron,13), fill=255)
        draw.text((x+11, top+20),MusicName,  font=ImageFont.truetype(hanzi,13), fill=255)
        if Replay:
            draw.text((x+42, top+50),"Replay",  font=ImageFont.truetype(retron,11), fill=255)
        global xiumiantime
        global xiumianle
        if xiumiantime<=5:#自动黑屏时间5秒
            disp.image(image)
            disp.display()
            xiumianle=False
        else:
            draw.rectangle((0,0,width,height), outline=0, fill=0)
            draw.text((x+11, top+20),"",  font=ImageFont.truetype(hanzi,13), fill=255)
            disp.image(image)
            disp.display()
            disp.clear()
            #xiumiantime=0
            xiumianle=True

timeint=-1
def MusicPlay():
    global timeint
    global AllWaveName
    if timeint == len(AllWaveName)-1:
        timeint=-1
    Name=AllWaveName[timeint+1]
    timeint=timeint+1
    f = wave.open(Name)
    secs = int(f.getnframes() / f.getframerate())
    mins=int(secs/60)
    lastsecs=secs-mins*60
    maintime=str(mins)+":"+str(lastsecs)
    frequency=f.getframerate()
    mixer.init(frequency)#,size=-16,channels=0)
    mixer.music.load(Name)
    mixer.music.play()
    costtime=0
    outputmins=0
    global MusicName
    global AllTimes
    MusicName=str(Name[6:-4])
    print(MusicName)
    while True:
        global MainNext
        if costtime<59:
            costtime=costtime+1
        else:
            costtime=0
            outputmins=outputmins+1
        global NowTimes
        global Replay
        NowTimes=str(outputmins)+":"+str(costtime)
        AllTimes=str(maintime)
        if NowTimes==AllTimes:
            time.sleep(1)
            if Replay:
                timeint=timeint-1
            MusicPlay()
            break
        time.sleep(1)
        if MainNext:
            MainNext=False
            break;
        #MusicPlayerScreen(maintime,str(outputmins)+":"+str(costtime),Name)

def MusicStop():
    mixer.music.stop()
    
xiumianle=False
xiumiantime=0
def xiumian():
    while True:
        global xiumianle
        global xiumiantime
        while xiumianle==False:
            xiumiantime=xiumiantime+1
            time.sleep(1)
            
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)

def Wificl():
    server=socket.socket()
    server.bind((IP,Port)) 
    while True:
        time.sleep(2)
        global xiumianle
        global xiumiantime
        global MainNext
        global timeint
        global Replay
        #socket.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1) 
#绑定要监听的端口
        try:
            server.listen() 
            print("监听已开始")
            conn,addr=server.accept()
            print(conn,addr)
            print("用户已连接")
            data=conn.recv(1024)
            maindata=str(data)
            print(maindata)
            conn.send(data.upper())
            if str(data)=="b'next'":
                t_MusicPlay3 = threading.Thread(target=MusicPlay)
                t_MusicPlay3.start()
                xiumianle=False
                xiumiantime=0
                MainNext=True
            elif str(data)=="b'light'":
                xiumianle=False
                xiumiantime=0
            elif str(data)=="b'up'":
                timeint=timeint-2
                t_MusicPlay3 = threading.Thread(target=MusicPlay)
                t_MusicPlay3.start()
                MainNext=True
                xiumianle=False
                xiumiantime=0
            elif str(data)=="b'replay'":
                if Replay:
                    Replay=False
                    print("Replay=False")
                elif Replay==False:
                    Replay=True
                    print("Replay=True")
        except:
            print("error")

AllWaveName=glob.glob(r"Music/*.wav")
print(AllWaveName)
print (len(AllWaveName))
t_MusicPlay = threading.Thread(target=MusicPlay)
t_xiumian = threading.Thread(target=xiumian)
t_Timeupdate = threading.Thread(target=Timeupdate)
t_ScreenUpdate = threading.Thread(target=ScreenUpdate)
t_UserInput = threading.Thread(target=UserInput)
t_Wificl = threading.Thread(target=Wificl)
t_MusicPlay.start()
t_xiumian.start()
t_Timeupdate.start()
t_ScreenUpdate.start()
t_UserInput.start()
t_Wificl.start()
#thread1 = MusicPlay("03 - The Calm.wav")
#thread2=UserInput()

#thread1.start()
#thread2.start()
#thread3.start()
# 添加线程到线程列表
#threads.append(thread1)
#threads.append(thread2)
#threads.append(thread3)
#thread1.start()
#thread2.start()

#thread1.join()
#thread2.join()
#thread3.join()

#_thread.start_new_thread(MusicPlay("03 - The Calm.wav"))
#_thread.start_new_thread(UserInput())
#_thread.start_new_thread1(Timeupdate())




