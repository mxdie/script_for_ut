import re
from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
import json
########################获取IMDB地址########################
def get_douban_url_db(film_name,film_year):
    # url转义
    film_name_search=parse.quote(film_name)
    film_name_search=film_name_search.replace('.','_')
    # 获取搜索关键字
    url_p2=film_name_search
    url_p1='https://v2.sg.media-imdb.com/suggestion/'+film_name[0].lower()+'/'
    film_name_url=url_p1+url_p2+'.json'
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    film_name_html=request.Request(url=film_name_url,headers=headers)
    with request.urlopen(film_name_html) as f:
          imdbinfo= json.loads(f.read().decode('utf-8'))
    imdbid = ''
    for info in imdbinfo['d']:
        if info['y'] == int(film_year):
            imdbid = info['id']
    if not imdbid:return
    film_name_html=request.Request(url='https://api.douban.com/v2/movie/imdb/'+imdbid,headers=headers)
    with request.urlopen(film_name_html) as f:
          doubaninfo= json.loads(f.read().decode('utf-8')) 
    return doubaninfo['alt'].replace('/movie/','/subject/')   

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
    html=request.urlopen(douban_html,timeout = 30).read().decode('utf-8')

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
    mainpic_url='https://img1.doubanio.com/view/photo/l_ratio_poster/public/'+mainpic_url

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
    return (name_ch,imdb,jianjie)

########################获取获奖情况########################
def douban_hj(douban_url):
    douban_url=douban_url+'/awards/'
    headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
    douban_html=request.Request(url=douban_url,headers=headers)
    html=request.urlopen(douban_html,timeout = 30).read().decode('utf-8')

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
    over=input()
