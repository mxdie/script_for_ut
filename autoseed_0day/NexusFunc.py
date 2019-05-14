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
    def __init__(self, WebSiteConf: str):
        '''
        读取配置参数
        WebSiteConf = {url,cookie}
        添加cookie
        '''
        self.res ={'msg':'666', 'torid':''}
        self.url = WebSiteConf['url']
        self.cookie = WebSiteConf['cookie']
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
                break
            except:
                if i == 2: 
                    self.res['msg'] = 'upload http error' #upload网络连接失败
                    return
        TorId=''.join(re.findall('%3D(.+?)%26',upload_reponse.url)).strip()
        if not TorId: 
            self.res['msg'] = 'upload torrent error' #upload种子上传失败
            return
        self.res['torid'] = TorId
    
    def download(self, TorId='', DlPath='', DlUrl= '' ):
        if not TorId: 
            TorId = self.res['torid']
            if not TorId:
               self.res['msg'] = 'torid error'  #没有获取到种子id
               return
        if not DlUrl: DlUrl= self.url+ 'download.php?id=' +TorId
        for i in range(3):
            try:
                request.urlretrieve(DlUrl, DlPath+ TorId+'.torrent')
                return
            except:                
                if i == 2: 
                    self.res['msg'] = 'tor download error' #种子下载失败
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