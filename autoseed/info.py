import re
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import pyperclip

########################获取豆瓣地址########################
def get_douban_url(film_name,film_year):
    # url转义
    film_name_search=parse.quote(film_name)
    film_name_search=film_name_search.replace('.','+')
    # 获取搜索关键字
    url_p2=film_name_search

    # 拼接url
    url_p1='https://movie.douban.com/j/subject_suggest?q='
    film_name_url=url_p1+url_p2

    # 定义获取html函数
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    film_name_html=request.Request(url=film_name_url,headers=headers)
    html=request.urlopen(film_name_html).read().decode('utf-8')

    # 抓取url和year
    douban_id=re.findall(r"subject(.+?)suggest",html)
    douban_id=''.join(douban_id).strip('\/?')
    douban_id=douban_id.split('\/?\/')
    douban_year=re.findall(r"year(.+?)sub_title",html)
    douban_year=''.join(douban_year).strip('":",')
    douban_year=douban_year.split('","":"')

    # 判断year
    if film_year in douban_year:
        year_number=douban_year.index(film_year)
    else:
       year_number=0

    # 选择id
    id_number=douban_id[year_number]

    # 组装url
    id_url='https://movie.douban.com/subject/'
    douban_url=id_url+id_number

    # 输出url
    return douban_url
########################获取豆瓣简介########################
def get_douban_jj(douban_url):
    # 打开url
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    douban_html=request.Request(url=douban_url,headers=headers)
    html=request.urlopen(douban_html).read().decode('utf-8')

    # 美丽肥皂
    soup=BeautifulSoup(html,"html.parser")
    mainpic_info_=soup.find_all(id='mainpic')
    film_info_=soup.find_all(id='info')
    film_jj_=soup.find_all(property="v:summary")
    name_name=soup.find_all(title="点击看更多海报",rel="v:image")
    year_year=soup.find_all(class_="year")
    fenshu=soup.find_all(property="v:average")
    renshu=soup.find_all(property="v:votes")
    #获取中文名
    name_ch=''.join(str(v) for v in soup.title.string)
    name_ch=name_ch.replace('(豆瓣)','')
    name_ch=name_ch.replace(' ','').strip('\n')
    #获取人数
    renshu_string=','.join(str(v) for v in renshu)
    film_renshu=re.findall(r'>(.+?)<',renshu_string)
    film_renshu=''.join(film_renshu)
    #获取分数
    fenshu_string=','.join(str(v) for v in fenshu)
    film_fenshu=re.findall(r'>(.+?)<',fenshu_string)
    film_fenshu=''.join(film_fenshu)
    #获取片名
    name_string=','.join(str(v) for v in name_name)
    film_name=re.findall(r'alt="(.+?)"',name_string)
    film_name=''.join(film_name)
    #获取年代
    year_string=','.join(str(v) for v in year_year)
    film_year=re.findall(r'>(.+?)<',year_string)
    film_year=''.join(film_year).strip('()')
    # 获取海报
    mainpic_info_=','.join(str(v) for v in mainpic_info_)
    mainpic_url=re.findall(r'public(.+?)"',mainpic_info_)
    mainpic_url=''.join(mainpic_url)
    mainpic_url='http://img3.doubanio.com/view/movie_poster_cover/lpst/public'+mainpic_url

    # 获取主要信息
    film_info_=','.join(str(v) for v in film_info_)
    soup2=BeautifulSoup(film_info_,"html.parser")
    film_info_1=soup2.find_all(class_='pl')
    film_info_1=','.join(str(v) for v in film_info_1)
    soup3=BeautifulSoup(film_info_1,"html.parser")
    film_info_2=soup2.find_all(class_='attrs')
    film_info_2=','.join(str(v) for v in film_info_2)
    soup4=BeautifulSoup(film_info_2,"html.parser")
    #简介项目
    xiangmu=''
    xiangmulist=[]
    for string in soup3.stripped_strings:
        a_linshi=repr(string)
        if a_linshi!="'/'":
              xiangmulist.append(a_linshi)
        a_linshi=a_linshi.strip("',")+'-'
        xiangmu+=a_linshi
    xiangmu=xiangmu.strip('-')
    xiangmu=xiangmu.split('--')
    #简介演员
    yanyuan=''
    yanyuanlist=[]
    for string in soup4.stripped_strings:
        a_linshi=repr(string)
        if a_linshi!="'/'":
              yanyuanlist.append(a_linshi)
        a_linshi=repr(string).strip("',")+'-'
        yanyuan+=a_linshi
    yanyuan=yanyuan.strip('-')
    yanyuan=yanyuan.replace('-/-','/')
    yanyuan=yanyuan.split('--')
    #简介其他
    qitalist=yanyuanlist+xiangmulist
    qita=''
    for string in soup2.stripped_strings:
        a_linshi=repr(string)
        if a_linshi not in qitalist:
              b_linshi=a_linshi.strip("',:")+'$'
              qita+=b_linshi
    qita=qita.strip('$/')
    qita=qita.replace('$/$','/')
    qita=qita.replace('$/','/')
    qita=qita.split('$')
    info=yanyuan+qita
    ch=re.compile(u'[\u4e00-\u9fa5]')
    jj=[]
    fengmian='[img='+mainpic_url+']' +'\n'+'\n'
    jj.append(fengmian)
    if '又名:' in xiangmu:
        if info[xiangmu.index('又名:')].find('/')==-1:
              yiming=info[xiangmu.index('又名:')]
        else:
              yiming_list=info[xiangmu.index('又名:')].split('/')
              for i in range(len(yiming_list)-1,-1,-1):
                    if len(re.findall(ch,yiming_list[i]))==0:
                          yiming_list.pop(i)
              yiming='/'.join(yiming_list)
        yiming='◎译　　名　'+yiming
        jj.append(yiming)
    pianming='◎片　　名　'+film_name
    jj.append(pianming)
    niandai='◎年　　代　'+film_year
    if '制片国家/地区:' in xiangmu:
        chandi='◎产　　地　'+info[xiangmu.index('制片国家/地区:')]
        jj.append(chandi)
    if '类型:' in xiangmu:
        leibie='◎类　　别　'+info[xiangmu.index('类型:')]
        jj.append(leibie)
    if '语言:' in xiangmu:
        yuyan='◎语　　言　'+info[xiangmu.index('语言:')]
        jj.append(yuyan)
    if '上映日期:' in xiangmu:
        riqi='◎上映日期　'+info[xiangmu.index('上映日期:')]
        jj.append(riqi)
    if '首播:' in xiangmu:
        riqi='◎首播日期　'+info[xiangmu.index('首播:')]
        jj.append(riqi)
    doubanfenshu='◎豆瓣评分　'+film_fenshu+'/'+'10'+' from '+film_renshu+' users'
    jj.append(doubanfenshu)
    doubanlianjie='◎豆瓣链接　'+douban_url
    jj.append(doubanlianjie)
    imdblianjie=''
    if 'IMDb链接:' in xiangmu:
        imdb='http://www.imdb.com/title/'+info[xiangmu.index('IMDb链接:')]
        imdblianjie='◎IMDb链接  '+imdb
        jj.append(imdblianjie)
    if '集数:' in xiangmu:
        jishu='◎集　　数　'+info[xiangmu.index('集数:')]
        jj.append(jishu)
    if '片长:' in xiangmu:
        pianchang='◎片　　长　'+info[xiangmu.index('片长:')]
        jj.append(pianchang)
    if '单集片长:' in xiangmu:
        pianchang='◎单集片长　'+info[xiangmu.index('单集片长:')]
        jj.append(pianchang)
    if '导演' in xiangmu:
        daoyan='◎导　　演　'+info[xiangmu.index('导演')]
        daoyan=daoyan.replace('/','\n　　 　　　')
        jj.append(daoyan)
    if '编剧' in xiangmu:
        bianju='◎编　　剧　'+info[xiangmu.index('编剧')]
        bianju=bianju.replace('/','\n　　　 　　')
        jj.append(bianju)
    if '主演' in xiangmu:
        zhuyan='◎主　　演　'+info[xiangmu.index('主演')]
        zhuyan=zhuyan.replace('/','\n　 　 　　　')
        jj.append(zhuyan)
    # 获取简介
    film_jj_=','.join(str(v) for v in film_jj_)
    film_jj=re.findall(r'summary">(.+?)</span',film_jj_,re.S)
    film_jj=''.join(film_jj).strip(' \n')
    film_jj=film_jj.replace('<br/>','')
    film_jj=film_jj.replace(' ','')
    jianjie='\n'.join(jj)+'\n'+'\n'+'◎简　　介'+'\n'+'\n'+film_jj
    #获取获奖情况
    
    #输出
    return name_ch,imdblianjie,jianjie

########################获取获奖情况########################
def douban_hj(douban_url):
    douban_url=douban_url+'/awards/'
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    douban_html=request.Request(url=douban_url,headers=headers)
    html=request.urlopen(douban_html).read().decode('utf-8')

    if 'class="awards"' in html:
        soup=BeautifulSoup(html,"html.parser")
        awards=soup.find_all(class_="awards")
        awards=''.join(str(v) for v in awards).split('<div class="awards">')
        awards.remove('')
        huojiang=''
        for i in awards:
            jiangxiang=[]
            soup=BeautifulSoup(i,"html.parser")
            name=re.findall('">(.+?)<',str(soup.h2))[0]
            jiangxiang.append(str(soup.ul))
            xm=[]
            for o in soup.ul.next_siblings:
                oo=str(o)
                if oo!='\n':
                    jiangxiang.append(oo)
            for o in jiangxiang:
                jm=re.findall('li>(.+?)</li>',o,re.S)
                if len(jm)==2:
                    jm_=jm[0]+' '+''.join(re.findall('>(.+?)<',jm[1]))
                else:
                    jm_=jm[0]
                xm.append(jm_)
            jiang=name+'\n    '+'\n    '.join(xm)+'\n'
            huojiang+=jiang
        huojiang='◎获奖情况'+'\n'+'\n'+huojiang
    else:
        huojiang=''
    return huojiang

########################获取bgm链接########################

def get_bgm_url(anime_name):

    anime_year='2017'
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
    bgm_id=re.findall(r'subject(.+?)class="l"',html)
    bgm_id=''.join(bgm_id).strip('/" ')
    bgm_id=bgm_id.split('" /')
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

    # 组装url
    if id_number=='' :
        bgm_url=''
    else:
        id_url='http://bgm.tv/subject/'
        bgm_url=id_url+id_number

    return bgm_url
########################获取bgm简介########################
def get_bgm_jj(bgm_url):

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

    return bgm_jj,anime_ch,tucao
########################_MAIN_########################
if __name__ == '__main__':
    url=input('url=')
    if 'douban' in url:
        name_ch,imdblianjie,jianjie=get_douban_jj(url)
        jianjie=jianjie+'\n'+'\n'+douban_hj(url)
    elif 'bgm' in url or 'bangumi' in url:
        bgm_jj,anime_ch,tucao=get_bgm_jj(url)
        jianjie=bgm_jj
    print(jianjie)
    try:
        pyperclip.copy(jianjie)
        print('已复制入剪切板')
    except:
        print('无法写入剪切板，请自行复制')
    over=input()
