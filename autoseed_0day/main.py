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
import bencode
import os

nanyang = NexusFunc('nanyang')
def fazhong(files,data,ut_load):
    nanyang.upload(files, data)
    if nanyang.res['msg'] !='666': return nanyang.res['msg']
    nanyang.download(DlPath = ut_load)
    return nanyang.res['msg']

if __name__ == "__main__":    
    f_path=sys.argv[1] #文件路径
    f_name=sys.argv[2] #文件名
    f_name_single=sys.argv[3] #单文件名
    #路径
    if f_name_single:
        file_path = f_path+'\\'+f_name
        vedio_name = f_name
    else:
        f_path_files = os.listdir(f_path)
        for files in f_path_files:
            files_name = files.lower()
            if 'mkv' in files_name or 'mp4' in files_name:
                file_path = f_path+'\\'+files
                vedio_name = files
                break
    if not file_path:
        print('error: file path error')
        sys.exit()
    print('文件路径： '+file_path)
    print('视频命名： '+vedio_name)
    #正则匹配
    nameinfo = fenci(vedio_name).res
    if nameinfo['msg'] !=666:
        print(nameinfo['msg'])
        sys.exit()
    print(nameinfo)
    #加载配置
    with open('config.json','r') as f:
        config = json.load(f)
    ut_save = config['path']['ut_save']
    ut_load = config['path']['ut_load']
    # 移动种子到当前目录
    torrent_path=ut_save+f_name+'.torrent'
    print('种子路径： '+torrent_path)
    copyfile(torrent_path,f_name+'.torrent')
    # 处理bug种子
    with open(f_name+'.torrent', 'rb') as f:
        bt=bencode.decode(f.read())
    bt['announce']='https://tracker.nanyangpt.com/announce.php'
    bt['announce-list']=[['https://tracker.nanyangpt.com/announce.php']]
    with open('temp.torrent', 'wb') as f:
        f.write(bencode.encode(bt))


    if nameinfo['type'] == 401:
        #获取db链接
        db_url=''
        for i in range(3):
            try:
                db_url=info.get_douban_url_db(nameinfo['name'],nameinfo['year'])
                break
            except:
                pass
        if not db_url: 
            try:
                db_url=info.get_douban_url(nameinfo['name'],nameinfo['year'])
            except:
                db_url='https://movie.douban.com/subject/'

        #获取简介
        if db_url=='https://movie.douban.com/subject/':
            db_url=input('自动搜索失败，输入豆瓣链接(https://movie.douban.com/subject/xx)\n:')
        name_ch,imdblianjie,jianjie=info.get_douban_jj(db_url)

        jianjie=jianjie+'\n'+'\n'+info.douban_hj(db_url)
        try:
            mi=MediaInfo.get_mediainfo(file_path)
        except:
            mi = ''
        warning="[quote]本资源为发种姬自动发布，发现问题可点击举报[/quote]"
        jianjie=warning+jianjie+'\n'+'\n'+mi
        # print(jianjie)
        print(name_ch + ' 简介已就绪')

        #填写表单
        files ={'file': open('temp.torrent', 'rb')}
        data={"type":'401',
            "name":nameinfo['upname'],
            "small_descr":name_ch +' [本资源发种姬自动发布，有问题请尽快举报]',
            "url":imdblianjie,
            "dburl":db_url,
            "descr":jianjie,
            "uplver":'yes'}
    elif nameinfo['type'] == 403:        
        with open('data.json','r') as f:
            data = json.load(f)
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

        #mediainfo
        try:
            mi=MediaInfo.get_mediainfo(file_path, gs= False)
        except:
            mi=''
        #编辑上传信息
        fubiaoti=bgm_jj[1]+' '+bgm_jj[2] + ' [本资源傲娇姬自动发布，有问题请尽快举报]'
        imdblianjie=''
        douban_url=''
        jianjie=bgm_jj[0]+'[color=red][size=4][b]视频信息[/b][/size][/color]'+'\n'+'[fold]'+'[code]'+mi+'[/code]'+'[/fold]'
        print(bgm_jj[1]+ ' 简介已就绪')

        #填写表单
        files ={'file': open('temp.torrent', 'rb')}
        data={"type":'403',
            "name":nameinfo['upname'],
            "small_descr":fubiaoti,
            "url":imdblianjie,
            "dburl":douban_url,
            "descr":jianjie,
            "uplver":'yes'}

    #发布
    i = 0
    while 1:
        i+=1
        msg = fazhong(files, data, ut_load)
        if msg == '666':
            print('发布完成')
            break
        elif msg == 'upload http error':
            print(msg)
            if i <= 3:
                time.sleep(5)
            else:
                resp = input('retry?(y/n)')
                if resp == 'n' or resp == 'N':
                    break
        else:
            print(msg)
            break
    #删临时文件
    try:
        files = os.listdir()
        for i in range(len(files)):
            if files[i][-7:] == 'torrent': 
                os.remove(files[i])
    except:
        pass
 
