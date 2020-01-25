修改时间：20200118 06 ：00
1、语音翻译（日语到中文）
2、识别语音中是否有人声音（此功能的不太准确，接下来继续修正）
3、test.py 单独的测试是否音频用是否有人声音
4、其他几个.py文件是一个整体，实现每五秒钟录取电脑中正在播放的音频，实现翻译功能

将voicetotext.py 文件中的190行将APPID,apikey,APISecret替换为自己的就可以了
wsParam = Ws_Param(APPID='xxxxxx', APIKey='xxxxxxxxxxx',
                        APISecret='xxxxxxxxxxxxxxxxx',
                        AudioFile=r'.\record\rec.wav')
translation.py 文件中的23行左右将APPID,apikey,APISecret替换为自己的就可以了
        # 应用ID（到控制台获取）
        self.APPID = "xxxx"
        # 接口APIKey（到控制台机器翻译服务页面获取）
        self.APIKey= "xxxxxxxxxxxxxxxx"
        # 接口APISercet（到控制台机器翻译服务页面获取）
        self.Secret = "xxxxxxxxxxxxxxxxxxxxxxx"
这里是使用的讯飞的API：它的网址https://www.xfyun.cn/
