import json
from urllib import request
import os,sys
from time import sleep
try:
        with open('config.json','r') as f:
                config = json.load(f)
                cookies = config['web']['cookies']
                passkey = config['web']['passkey']

        # 判断cookie
        print('少女祈祷中...')
        print('')
        headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                  'cookie':cookies}
        try:
                html_request=request.Request(url='https://nanyangpt.com/index.php',headers=headers)
                html_text=request.urlopen(html_request).read().decode('utf-8')
                if html_text.find('登录')==-1:
                        print('cookies可以用。')
                else:
                        print('cookies不能用。')

        except:
                print('无法访问网站检查cookies，请确认网络连接,如果可以正常访问，请前往论坛报错。')
        sleep(1)
        print('')
        print('少女继续祈祷中...')
        print('')
        opener = request.build_opener()
        opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')]
        request.install_opener(opener)
        zz_url1='https://nanyangpt.com/download.php?id='
        zz_url2='&passkey='
        zz_url=zz_url1+'19839'+zz_url2+passkey
        list_zz=[]
        def  huizhi(a,b,c):
                list_zz.append(a)
        A=request.urlretrieve(zz_url,'temp.torrent',huizhi)
        if len(list_zz) >=3:
                print('passkey可以用。')
        else:
                print('passkey有问题，或者网络有问题，确认没问题的话来论坛报错。')
        print('')
        sleep(1)
        print('少女祈祷完毕。')
        print('')
        os.remove('temp.torrent')

except:
        print('找不到配置文件，或者有权限问题。')
sys.exit()
print('10秒 后')
sleep(1)
print('9秒  自')
sleep(1)
print('8秒  动')
sleep(1)
print('7秒  关')
sleep(1)
print('6秒  闭')
sleep(1)
print('5秒  窗')
sleep(1)
print('4秒  口')
sleep(1)
print('3秒  .')
sleep(1)
print('2秒  .')
sleep(1)
print('1秒  .')
sleep(1)
