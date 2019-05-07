import sys
import json
from shutil import copyfile
import MediaInfoDLL3
import func

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
#mediainfo
vedio_file_path=vedio_file_path.replace('"','/')
vedio_path=vedio_file_path+bt_name
print(vedio_path)
try:
    mi = MediaInfoDLL3.MediaInfo()
    mi.Open(vedio_path)
    info = mi.Inform()
    mi.Close()
except:
    info =''
#编辑上传信息
up_name='[动画]'+'['+ch_name+']'+'['+anime_name+'.'+anime_jishu+'.'+'TVRip.GB.'+fbl+'.MP4.'+anime_staff+']'
fubiaoti=fbt+'  ★10月新番'
imdblianjie=''
douban_url=''
jianjie=bgm_jj+'[color=red][size=4][b]视频信息[/b][/size][/color]'+'\n'+'[fold]'+'[code]'+info+'[/code]'+'[/fold]'
print(up_name)
print(fubiaoti)
print(jianjie)