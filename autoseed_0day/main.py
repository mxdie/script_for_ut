import sys,info,MediaInfo
from time import strftime
from urllib import request
import re,json
import time
import requests
from shutil import copyfile
f_path=sys.argv[1]
f_name=sys.argv[2]
f_name2=sys.argv[3]
if 'wiki' not in f_name and 'WIKI' not in f_name:
    sys.exit()
print(f_path)
print(f_name)
print(f_name2)
m_name = f_name
with open('config2.json','r') as f:
    config = json.load(f)
cookies = config['web']['cookies']
passkey = config['web']['passkey']
ut_save = config['path']['ut_save']
ut_load = config['path']['ut_load']
if not f_name2:
    m_name.replace('.mp4','')
    m_name.replace('.mkv','')
up_name = m_name
#获取名字
now_year=int(strftime("%Y"))
f_name_=f_name.split('-')
f_name_list=f_name_[0].split('.')
if '.' in f_name_[1]:
    team=f_name_[1].split('.')[0]
else:
    team=f_name_[1]
f_name_list.reverse()
for year in range(now_year,1888,-1):
    now_year_str=str(year)
    if now_year_str in f_name_list:
          m_year=now_year_str
          m_year_index=f_name_list.index(now_year_str)
          break
f_name_list.reverse()
m_name=' '.join(f_name_list[0:len(f_name_list)-m_year_index-1])
print(m_name+' '+m_year)
#获取db链接
db_url=info.get_douban_url(m_name,m_year)
#获取简介
if db_url=='https://movie.douban.com/subject/':
    db_url=input('自动搜索失败，输入豆瓣链接(https://movie.douban.com/subject/xx)\n:')
name_ch,imdblianjie,jianjie=info.get_douban_jj(db_url)
'''
check=input(name_ch+'(y/n)')
if check=='n' or check=='N':
    db_url=input('输入豆瓣链接(https://movie.douban.com/subject/xx)\n:')
    name_ch,imdblianjie,jianjie=info.get_douban_jj(db_url)
'''
jianjie=jianjie+'\n'+'\n'+info.douban_hj(db_url)
#获取mediainfo
if f_name2:
    mi=MediaInfo.get_mediainfo(f_path+'/'+f_name)
else:
    try:
        mi=MediaInfo.get_mediainfo(f_path+'/'+f_name+'.mkv')
    except:
        mi = ''
jianjie=jianjie+'\n'+'\n'+mi
print(jianjie)
# 移动种子
torrent_path=ut_save+f_name+'.torrent'
copyfile(torrent_path,f_name+'.torrent')
#填写表单
files ={'file': open(f_name+'.torrent', 'rb')}
data={"type":'401',
       "name":up_name,
       "small_descr":name_ch,
       "url":imdblianjie,
       "dburl":db_url,
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
        request.urlretrieve(zz_url,ut_load+up_name+'.torrent')
        print('完事儿')
    except:
        print(up_name+'\n'+'种子下载失败'+'\n'+timestamp)
        pause = input()
else: 
    print(up_name+'\n'+'发布失败'+'\n'+timestamp)
    pause = input()

