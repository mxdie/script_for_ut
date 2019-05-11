from urllib import request
from urllib import parse
import re
import time
from bs4 import BeautifulSoup
'''
def get_name_info(vedio_name: str)-> tuple:

    我也看不懂这个屎一样的分词是啥意思
    ←_←看懂也不想改了

    vedio_name= vedio_name.replace('.mkv','')
    vedio_name= vedio_name.replace('.MKV','')
    vedio_name= vedio_name.replace('.mp4','')
    vedio_name= vedio_name.replace('.MP4','')
    if vedio_name.find('1080')!=-1:
        anime_fbl='1080P'
    else:
        anime_fbl='720P'
    if 'MKV' in vedio_name or 'mkv' in vedio_name:
        anime_gs='MKV'
    else:
        anime_gs='MP4'
    vedio_name_list=vedio_name.split(']')
    anime_staff=vedio_name_list[0].strip('[')
    vedio_name_list.pop(0)
    vedio_name_list=']'.join(vedio_name_list)
    vedio_name_list=vedio_name_list.split('[')
    if vedio_name_list[0]=='':
        anime_name=vedio_name_list[1].strip(']')
        anime_jishu=vedio_name_list[2].strip(']')
    else:
        anime_name=vedio_name_list[0].strip('.')
        anime_jishu=vedio_name_list[1].strip(']')
    return (anime_staff,anime_name,anime_jishu,anime_fbl,anime_gs)

def editdistance(str1: str,str2: str)-> int:

    计算编辑距离

    edit = [[i+j for j in range(len(str2)+1)] for i in range(len(str1)+1)]
    for i in range(1,len(str1)+1):
        for j in range(1,len(str2)+1):
            if str1[i-1] == str2[j-1]:
                d=0
            else:
                d=1
            edit[i][j] = min(edit[i-1][j]+1,edit[i][j-1]+1,edit[i-1][j-1]+d)
    return edit[len(str1)][len(str2)]
'''
def get_bgm_url(anime_name: str)-> str:
    '''
    搜索bgm链接
    '''

    anime_year=time.strftime('%Y',time.localtime(time.time()))
    # url转义
    anime_name_search=parse.quote(anime_name)
    anime_name_search=anime_name_search.replace(' ','+')

    # 获取搜索关键字
    url_p2=anime_name_search

    # 拼接url
    url_p1='http://bgm.tv/subject_search/'
    url_p3='?cat=2'
    anime_name_url=url_p1+url_p2+url_p3

    # 定义获取html函数
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    anime_name_html=request.Request(url=anime_name_url,headers=headers)
    html=request.urlopen(anime_name_html).read().decode('utf-8')

    # 抓取ID和年份
    bgm_id=re.findall(r'/subject/(.+?)" class="l"',html)
    if not bgm_id:return ''
    bgm_year=re.findall(r'info tip">(.+?)年',html,re.S)
    bgm_year=''.join(bgm_year).strip(',\n')
    bgm_year=bgm_year.split('\n')

    # 匹配年份
    if anime_year in bgm_year:
        year_number=bgm_year.index(anime_year)
    else:
        year_number=0

    # 选择ID
    id_number=bgm_id[year_number]
    print(id_number)
    # 组装url
    if id_number=='' :
        bgm_url=''
    else:
        id_url='http://bgm.tv/subject/'
        bgm_url=id_url+id_number

    return bgm_url

def get_bgm_jj(bgm_url:str)-> tuple:

    # 打开url
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    bgm_html=request.Request(url=bgm_url,headers=headers)
    html=request.urlopen(bgm_html).read().decode('utf-8')

    # 美丽肥皂
    soup=BeautifulSoup(html,"html.parser")
    anime_info_=soup.find_all(id="infobox")
    rank_info_=soup.find_all(property="v:average")
    vote_info_=soup.find_all(property="v:votes")
    cast_info_=soup.find_all(id="browserItemList")
    jj_info_=soup.find_all(id="subject_summary")
    tucao_info_=soup.find_all(class_="text")
    mainpic_info_=soup.find_all('a',class_="thickbox cover")

    # 获取封面
    mainpic_info_=','.join(str(v) for v in mainpic_info_)
    mainpic_url=re.findall(r'href="//(.+?)"',mainpic_info_)
    mainpic='[img='+'http://'+''.join(mainpic_url)+']'

    #获取staff
    anime_info_=''.join(str(v) for v in anime_info_)
    soup2=BeautifulSoup(anime_info_,"html.parser")
    anime_info_zl=soup2.find_all(class_="tip")
    anime_info_zl=''.join(str(v) for v in anime_info_zl)
    soup3=BeautifulSoup(anime_info_zl,"html.parser")
    xiangmulist=[]
    suoyoulist=[]
    for string in soup3.stripped_strings:
        a_linshi=repr(string)
        xiangmulist.append('$'+a_linshi.strip("'"))
    for string in soup2.stripped_strings:
        b_linshi=repr(string)
        suoyoulist.append('$'+b_linshi.strip("'"))
    suoyou=''.join(suoyoulist)
    jieguo=[]
    for xiangmu in xiangmulist:
        c_linshi=suoyou.split(xiangmu)
        if c_linshi[0]!='':
            jieguo.append(c_linshi[0])
        c_linshi.pop(0)
        suoyou=xiangmu.join(c_linshi)
    jieguo.append(suoyou)
    xiangmulist_str='++'.join(xiangmulist)
    xiangmulist_str=xiangmulist_str.replace('$','')
    xiangmulist=xiangmulist_str.split('++')
    jieguo_str='++'.join(jieguo)
    jieguo_str=jieguo_str.replace('$','')
    jieguolist=jieguo_str.split('++')
    anime_ch=''
    if '中文名:' in xiangmulist:
        anime_ch=jieguolist[xiangmulist.index('中文名:')]
    staff=[]
    for i in range(0,len(xiangmulist)):
        d_linshi='[b]'+xiangmulist[i]+'[/b]'+jieguolist[i]
        staff.append(d_linshi)
    #获取声优   
    cast_info=''.join(str(v) for v in cast_info_)
    divlist=re.findall(r'"userContainer">(.+?)</div',cast_info,re.S)
    castlist=[]
    for div in divlist:
        picurl='[img='+'http:'+''.join(re.findall(r'//.+\.jpg',div))+']'
        actor=''.join(re.findall(r'title="(.+?)"',div))
        cast=''.join(re.findall(r'starring">(.+?)</a',div))
        e_linshi=picurl+' '+'[b]'+actor+'[/b]   配音 : '+cast
        castlist.append(e_linshi)
    #获取简介
    jj_info_=','.join(str(v) for v in jj_info_)
    jj_info=re.findall(r'summary">(.+?)</div',jj_info_,re.S)
    jj_info=''.join(jj_info)
    jj_info=jj_info.replace('<br/>','')
    #抓一个吐槽
    tucao_info=''.join(str(v) for v in tucao_info_)
    tucaolist=re.findall(r'<p>(.+?)</p>',tucao_info)
    if tucaolist!=[]:
        tucao=tucaolist[0]+'——来自BGM吐槽箱'
    else:
        tucao='抓取不到吐槽，这东西真有人看？'
    #获取评分
    rank_info=''.join(str(v) for v in rank_info_)
    rank=re.findall(r'>(.+?)<',rank_info)
    rank=''.join(rank)
    vote_info=''.join(str(v) for v in vote_info_)
    vote=re.findall(r'>(.+?)<',vote_info)
    vote=''.join(vote)
    #拼接
    bgm_jj1=mainpic+'\n'+'\n'+'♥bgm链接	'+bgm_url+'\n'+'♥bgm评分	'+rank+'/10 from '+vote+' users'+'\n'+'\n'+'[color=red][size=4][b]故事简介[/b][/size][/color]'+'\n'+jj_info+'\n'+'\n'
    bgm_jj2='[color=red][size=4][b]角色介绍[/b][/size][/color]'+'\n'+'\n'.join(castlist)+'\n'+'\n'
    bgm_jj3='[color=red][size=4][b]动画信息[/b][/size][/color]'+'\n'+'\n'.join(staff)+'\n'+'\n'
    bgm_jj=bgm_jj1+bgm_jj2+bgm_jj3

    return (bgm_jj,anime_ch,tucao)
