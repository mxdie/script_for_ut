import sys
import json
from shutil import copyfile
import MediaInfoDLL3
import func
import requests
import time
import re
from urllib import request
#加载配置
with open('config.json','r') as f:
    config = json.load(f)
cookies = config['web']['cookies']
passkey = config['web']['passkey']
ut_save = config['path']['ut_save']
ut_load = config['path']['ut_load']

#参数
bt_name=sys.argv[1]
vedio_file_path=sys.argv[2]

# 移动种子
torrent_path=ut_save+bt_name+'.torrent'
copyfile(torrent_path,bt_name+'.torrent')

# 获取简介信息
anime_info = func.get_name_info(bt_name)
print(anime_info)
with open('data.json','r') as f:
    data = json.load(f)
if anime_info[1] in data['anime']:
    bgm_url = data['anime'][anime_info[1]]
    bgm_jj = func.get_bgm_jj(bgm_url)
else:
    search_name = anime_info[1]
    while 1:
        bgm_url = func.get_bgm_url(search_name)
        if not bgm_url:
            search_name = input('搜不到bgm链接，输入这个番更通俗易懂的名字叭：')
            continue
        bgm_jj = func.get_bgm_jj(bgm_url)
        confirm = input('中译名是'+bgm_jj[1]+'吗：(y/n)')
        if confirm in ('y','Y',''):
            break
        else:
            bgm_url = input('那直接输入bgm链接叭：')
            bgm_jj = func.get_bgm_jj(bgm_url)
            break
    data['anime'][anime_info[1]] = bgm_url
with open('data.json','w') as f:
    json.dump(data,f)
#mediainfo
vedio_file_path=vedio_file_path.replace('"','/')
vedio_path=vedio_file_path+bt_name
print(vedio_path)
#try:
mi = MediaInfoDLL3.MediaInfo()
mi.Open(vedio_path)
info = mi.Inform()
mi.Close()
print(info)
#except:
#    info =''
#编辑上传信息
up_name="{0[1]}.{0[2]}.TVRip.GB.{0[3]}.{0[4]}-{0[0]}".format(anime_info)
fubiaoti=bgm_jj[1]+' '+bgm_jj[2]
imdblianjie=''
douban_url=''
jianjie=bgm_jj[0]+'[color=red][size=4][b]视频信息[/b][/size][/color]'+'\n'+'[fold]'+'[code]'+info+'[/code]'+'[/fold]'
print(up_name)
print(fubiaoti)
print(jianjie)
#填写表单
files ={'file': open(bt_name+'.torrent', 'rb')}
data={"type":'403',
       "name":up_name,
       "small_descr":fubiaoti,
       "url":imdblianjie,
       "dburl":douban_url,
       "descr":jianjie,
       "uplver":'yes'}
#发布
headers= {'cookie':cookies}
opener = request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36')]
request.install_opener(opener)
upload_html=requests.post(url='https://nanyangpt.com/takeupload.php',headers=headers,data=data,files=files)
ny_id=''.join(re.findall('%3D(.+?)%26',upload_html.url)).strip()
timestamp=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
if ny_id!='':
    zz_url1='https://nanyangpt.com/download.php?id='
    zz_url2='&passkey='
    zz_url=zz_url1+ny_id+zz_url2+passkey
    try:
        print(zz_url)
        request.urlretrieve(zz_url,ut_load+bt_name+'.torrent')
        print('完事儿')
    except:
        print(bt_name+'\n'+'种子下载失败'+'\n'+timestamp)
        pause = input()
else: 
    print(bt_name+'\n'+'发布失败'+'\n'+timestamp)
    pause = input()
