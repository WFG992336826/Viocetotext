# _*_ coding: utf-8 _*_

# 录音机，用于录制声卡播放的声音(内录)

import os
import pyaudio
import threading
import wave
import time
from datetime import datetime
import sounddevice as sd

#录音类 
class Recorder():
    def __init__(self, chunk=1024, channels=1, rate=16000):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []

    #获取内录设备序号,在windows操作系统上测试通过，hostAPI = 0 表明是MME设备
    def findInternalRecordingDevice(self,p):
        #要找查的设备名称中的关键字
        target = "立体声混音"
        #获取全部声音设备  扬声器  立体声混音
        devices = sd.query_devices()
        #print(devices)
        
        #逐一查找声音设备  p.get_device_count()
        for i in range(len(devices)):
            if devices[i]["name"].find(target)>=0 and devices[i]['hostapi'] == 0 :      
                #print('已找到内录设备,序号是 ',i)
                return i
        print('无法找到内录设备!')
        return -1

    #开始录音，开启一个新线程进行录音操作
    def start(self):
        threading._start_new_thread(self.__record, ())

    #执行录音的线程函数
    def __record(self):
        self._running = True
        self._frames = []

        p = pyaudio.PyAudio()
        #查找内录设备
        dev_idx = self.findInternalRecordingDevice(p)
        if dev_idx < 0 :            
            return
        #在打开输入流时指定输入设备
        stream = p.open(input_device_index=dev_idx,
                        format=self.FORMAT,
                        channels=self.CHANNELS,
                        rate=self.RATE,
                        input=True,
                        frames_per_buffer=self.CHUNK)
        #循环读取输入流
        while(self._running):
            data = stream.read(self.CHUNK)
            self._frames.append(data)

        #停止读取输入流  
        stream.stop_stream()
        #关闭输入流
        stream.close()
        #结束pyaudio
        p.terminate()
        return
 
    #停止录音
    def stop(self):
        self._running = False
 
    #保存到文件
    def save(self, fileName):   
        #创建pyAudio对象
        p = pyaudio.PyAudio()
        #打开用于保存数据的文件
        wf = wave.open(fileName, 'wb')
        #设置音频参数
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        #写入数据
        wf.writeframes(b''.join(self._frames))
        #关闭文件
        wf.close()
        #结束pyaudio
        p.terminate()

    def run_rec(self):
        #检测当前目录下是否有record子目录
        if not os.path.exists('record'):
            os.makedirs('record')

        #print("\npython 录音机 ....\n")
        #print("提示：按 r 键并回车 开始录音\n")    
        
        #i = input('请输入操作码:')
        i = "r"
        if i == 'r':           
            #rec = Recorder()
            begin = time.time()

            #print("\n开始录音,按 s 键并回车 停止录音，自动保存到 record 子目录\n")
            self.start()

            running = True
            while running:
                #i = input("请输入操作码:")
                #i = "s"
                t = time.time() - begin
                #if i == 's':
                if t >= 5:
                    running =False
                    #print("录音已停止")
                    self.stop()               
                    #print('录音时间为%ds'%t)
                    #以当前时间为关键字保存wav文件
                    #rec.save("record/rec_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".wav")
                    self.save("record/rec.wav")       
'''
if __name__ == "__main__":
    run_rec()
'''