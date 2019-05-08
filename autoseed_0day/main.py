import sys,info,MediaInfo
from time import strftime
from urllib import request
import re,json
import time
import requests
from shutil import copyfile
from NexusFunc import NexusFunc

f_path=sys.argv[1]
f_name=sys.argv[2]
f_name2=sys.argv[3]
if 'wiki' not in f_name and 'WIKI' not in f_name:
    sys.exit()
if f_name2:
    print('文件路径： '+f_path+'/'+f_name)
else:
    print('文件路径： '+f_path)

m_name = f_name
with open('config.json','r') as f:
    config = json.load(f)
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
nanyang = NexusFunc('nanyang')
TorId= nanyang.upload(files, data)
#下载种子
nanyang.download(TorId, ut_load)