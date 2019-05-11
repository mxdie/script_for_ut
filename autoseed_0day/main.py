import sys,info,MediaInfo
from time import strftime
from urllib import request
import re,json
import time
import requests
from shutil import copyfile
from NexusFunc import NexusFunc
from fenci import fenci
import func
import MediaInfoDLL3
import bencode
f_path=sys.argv[1]
f_name=sys.argv[2]
f_name2=sys.argv[3]
nameinfo = fenci(f_name).res
print(f_name)
if nameinfo['msg'] !=666:
    print(nameinfo['msg'])
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
'''
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
'''
# 移动种子
torrent_path=ut_save+f_name+'.torrent'
copyfile(torrent_path,f_name+'.torrent')
if nameinfo['type'] == 401:
    #获取db链接
    db_url=''
    for i in range(3):
        try:
            db_url=info.get_douban_url_db(nameinfo['name'],nameinfo['year'])
            break
        except:
            pass
    if not db_url: db_url=info.get_douban_url(nameinfo['name'],nameinfo['year'])
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
    if f_name2:
        mi=MediaInfo.get_mediainfo(f_path+'/'+f_name)
    else:
        try:
            mi=MediaInfo.get_mediainfo(f_path+'/'+f_name+'.mkv')
        except:
            mi = ''
    jianjie=jianjie+'\n'+'\n'+mi
    print(jianjie)

    #填写表单
    files ={'file': open(f_name+'.torrent', 'rb')}
    data={"type":'401',
        "name":f_name,
        "small_descr":name_ch,
        "url":imdblianjie,
        "dburl":db_url,
        "descr":jianjie,
        "uplver":'yes'}
elif nameinfo['type'] == 403:
    
    with open('data.json','r') as f:
        data = json.load(f)
    file= open(f_name+'.torrent', 'rb')
    bt=bencode.decode(file.read())
    file.close()
    bt['announce']='https://tracker.nanyangpt.com/announce.php'
    bt['announce-list']=[['https://tracker.nanyangpt.com/announce.php']]
    file=open('temp.torrent', 'wb')
    file.write(bencode.encode(bt))
    file.close()
    if nameinfo['name'] in data['anime']:
        bgm_url = data['anime'][nameinfo['name']]
        bgm_jj = func.get_bgm_jj(bgm_url)
    else:
        search_name = nameinfo['name']
        while 1:
            bgm_url=func.get_bgm_url(search_name)
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
        data['anime'][nameinfo['name']] = bgm_url
    with open('data.json','w') as f:
        json.dump(data,f)

    #try:
    mi = MediaInfoDLL3.MediaInfo()
    if f_name2:
        mi.Open(f_path+'/'+f_name)
    else:
        try:
            mi.Open(f_path+'/'+f_name+'.mkv')
        except:
            pass
    spinfo = mi.Inform()
    mi.Close()
    print(spinfo)
    #except:
    #    info =''
    #编辑上传信息
    fubiaoti=bgm_jj[1]+' '+bgm_jj[2]
    imdblianjie=''
    douban_url=''
    jianjie=bgm_jj[0]+'[color=red][size=4][b]视频信息[/b][/size][/color]'+'\n'+'[fold]'+'[code]'+spinfo+'[/code]'+'[/fold]'
    print(nameinfo['upname'])
    print(fubiaoti)
    print(jianjie)
    #填写表单
    files ={'file': open('temp.torrent', 'rb')}
    data={"type":'403',
        "name":nameinfo['upname'],
        "small_descr":fubiaoti,
        "url":imdblianjie,
        "dburl":douban_url,
        "descr":jianjie,
        "uplver":'yes'}
#获取mediainfo

#发布
nanyang = NexusFunc('nanyang')
TorId= nanyang.upload(files, data)
#下载种子
nanyang.download(TorId, ut_load)