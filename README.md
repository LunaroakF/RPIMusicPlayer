# RPIMusicPlayer树莓派远程音乐播放器
# 介绍

## 作用
使用树莓派RaspBerry Pi制作一个可以远程控制的音乐播放器  
可以在你的Party上用  
## 缺点
媒体文件要是.wav文件  
## 传输
用的Socket
## 屏幕驱动
Adafruit_SSD1306  
## 走线
![Image text](https://github.com/LunaroakF/Images/blob/master/RaspberryPiMusicPlayer/Line.jpg)  
****
## 文件介绍  
MobileMusicControl文件夹为安卓控制软件的Android Studio的项目  
PythonMusicPlayer文件夹为主程序  
****
# 用法  
将128x64的I2C的OLED屏幕连接到树莓派  
确保驱动正常  
cd到文件夹  
将需要播放的16位的，44100Hz的.wav文件扔到Music目录里  
(可在电脑上用各种软件转换，我使用的AU)
运行Player.py即可  
## 音频输出  
耳机接口  
****
# 注意事项  
安卓软件上的输入框对应树莓派所处的IP  
![Image text](https://github.com/LunaroakF/Images/blob/master/RaspberryPiMusicPlayer/Android.jpg)  
