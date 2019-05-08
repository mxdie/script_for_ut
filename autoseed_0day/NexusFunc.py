'''
放一些跟nexusphp搭建的pt站有关的函数
mxdie@nypt
'''
from urllib import request
import json
import requests
import time
import re
class NexusFunc():
    def __init__(self, WebSiteName: str):
        '''
        读取配置参数
        添加cookie
        '''
        #config
        with open('config.json','r') as f:
            config = json.load(f)
        self.url = config[WebSiteName]['url']
        self.cookie = config[WebSiteName]['cookie']
        #header
        opener = request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'),
                        ('cookie',self.cookie)]
        request.install_opener(opener)

    
    def upload(self, files, data, UpUrl =''):
        '''
        上传函数
        files ={'file': open('1.torrent', 'rb')}
        data= {"type":'403',
                "name":'1',
                "small_descr":'1',
                "url":'1',
                "dburl":'1',
                "descr":'1',
                "uplver":'yes'}
        '''
        if not UpUrl: UpUrl= self.url+ 'takeupload.php'
        headers= {'cookie':self.cookie}
        for i in range(3):
            try:
                upload_reponse= requests.post(url=UpUrl ,headers=headers, data=data, files=files, timeout= 30)
                upload_reponse.raise_for_status()
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ' upload网络连接成功')
                break
            except:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ' upload网络连接失败'+ str(i+1)+ '次')
                if i == 2: 
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ' upload网络连接没救了')
                    return
        TorId=''.join(re.findall('%3D(.+?)%26',upload_reponse.url)).strip()
        if not TorId: 
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ' upload种子上传失败')
            return
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ' upload成功 ID:'+ TorId)
        return TorId
    
    def download(self, TorId, DlPath='', DlUrl= '' ):
        if not DlUrl: DlUrl= self.url+ 'download.php?id=' +TorId
        for i in range(3):
            try:
                request.urlretrieve(DlUrl, DlPath+ TorId+'.torrent')
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ' 种子下载成功')
                return
            except:
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ' 种子下载失败'+ str(i+1)+ '次')
                if i == 2: 
                    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+ ' 种子下载没救了')
                    return

        
if __name__ == "__main__":
    files ={'file': open('1.torrent', 'rb')}
    data= {"type":'403',
            "name":'1',
            "small_descr":'1',
            "url":'1',
            "dburl":'1',
            "descr":'1',
            "uplver":'yes'}
    nanyang = NexusFunc('nanyang')
    nanyang.download('70785')