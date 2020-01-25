# _*_ coding: utf-8 _*_

# 录音机，用于录制声卡播放的声音(内录)
import os
import pyaudio
import _thread as thread
import wave
import time
import math
import struct
from datetime import datetime
import sounddevice as sd


#录音类 
class Recorder():
    def __init__(self, chunk=1024, channels=1, rate=16000, Threshold=50):
        self.CHUNK = chunk
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = channels
        self.RATE = rate
        self._running = True
        self._frames = []
        #Assuming Energy threshold upper than 30 dB
        self.Threshold = Threshold
        self.SHORT_NORMALIZE = (1.0/32768.0)
        self.swidth = 2
        #录制音频的最大时长
        self.Max_Seconds = 10
        self.TimeoutSignal = ((self.RATE / self.CHUNK * self.Max_Seconds) + 2)
        self.silence = True

        self.Flag_save = True



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
        return True

    def rms(self, frame):
        count = len(frame)/self.swidth
        format = "%dh"%(count)
        # short is 16 bit int
        shorts = struct.unpack(format, frame)

        sum_squares = 0.0
        for sample in shorts:
            n = sample * self.SHORT_NORMALIZE
            sum_squares += n*n
        # compute the rms 
        rms = math.pow(sum_squares/count,0.5);
        return rms * 1000

    def KeepRecord(self, stream, LastBlock):
        self._frames = []
        Time = 0

        self._frames.append(LastBlock)
        for i in range(0, int(self.TimeoutSignal)):
            data = stream.read(self.CHUNK)
            rms_value = self.rms(data)
            if (rms_value < self.Threshold):
                Time = Time + 1
                if (Time > self.TimeoutSignal/5):
                    break
            #I chage here (new Ident)
            self._frames.append(data)

        #print("end record after timeout")
        #print("write to File")
          

    def listen(self):
        #print("waiting for Speech")
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
        while self.silence:
            input = stream.read(self.CHUNK)
            rms_value = self.rms(input)
            if (rms_value > self.Threshold):
                self.silence = False
                LastBlock=input
                #print("hello ederwander I'm Recording....")
                self.KeepRecord(stream, LastBlock)
        #停止读取输入流  
        stream.stop_stream()
        #关闭输入流
        stream.close()
        #结束pyaudio
        p.terminate()

    def run_rec(self):
        self.listen()
        #fileName = "record/rec_"+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".wav"
        fileName = "record/rec.wav"
        flag_save = self.save(fileName)
        return flag_save

    def save_success(self):
        if(self.silence == True):
            return True
        else:
            return False 
'''
if __name__ == "__main__":
    while True:
        run_rec()
'''