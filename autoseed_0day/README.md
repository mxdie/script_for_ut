# autoseed
![](https://img.shields.io/badge/python-3.7-red.svg)![](https://img.shields.io/badge/support-ny-blue.svg)![](https://img.shields.io/badge/powered-ny-green.svg)

可以把支持下载完成运行程序的bt客户端rss回来的东西直接转发到南洋。

<!--


## 导航
- [autoseed](#autoseed)
  - [导航](#%E5%AF%BC%E8%88%AA)
  - [使用方法](#%E4%BD%BF%E7%94%A8%E6%96%B9%E6%B3%95)
    - [UT设置](#ut%E8%AE%BE%E7%BD%AE)
    - [config配置](#config%E9%85%8D%E7%BD%AE)
      - [nanyang](#nanyang)
      - [path](#path)
      - [namerule](#namerule)
      - [匹配规则](#%E5%8C%B9%E9%85%8D%E8%A7%84%E5%88%99)
    - [2 使用](#2-%E4%BD%BF%E7%94%A8)
      - [requirements](#requirements)
      - [uTorrent](#utorrent)
      - [FAQ](#faq)
-->

----

## 使用方法

> clone 本项目至本地任一文件夹 `"~\script_for_ut\"`

### UT设置

* 用来RSS的UT，勾选并指定文件和种子保存位置

![](https://img.ajycc20.xyz/imgs/2019/05/eb58f82ff31b616f.png)

* 用来做种的UT（可以和RSS是同一个），勾选并使文件保存位置和RSS的UT相同，勾选并指定自动载入种子位置

![](https://img.ajycc20.xyz/imgs/2019/05/125a12aed1c8994f.png)

### config配置

* 将`data.sample.json`另存为`data.json`
* 将`config.sample.json`另存为`config.json`并打开

#### nanyang

* 把字符串式cookie填上去，获取方式见下图，可以整个复制替换原默认值。

![](https://img.ajycc20.xyz/imgs/2019/05/45b5948171512389.png)

#### path

* `ut_save`: `"E:\save\"`  即上文RSS的UT保存种子的路径
* `ut_load`: `E:\save\` 即上文做种的UT载入种子的路径

#### namerule

* key值为资源组，**只会转发填写在这里的资源组发布的资源**，以wiki为例

|namerule||
|:---:|:---:|
|key|value|
|wiki|[401,"name.year.resolution.source.codec-group.mkv","{name}.{year}.{source}.{resolution}.{codec}-{group}"]|

**值参数:**

|字段|字段说明|类型|必填|说明|
|:---:|:---:|:---:|:---:|:---:|
|`401`|资源类别|int|Y|网站种子分类的`cat`参数|
|`name.year.resolution.source.codec-group.mkv`|资源名格式|string|Y|使用关键字替代原资源命名中的需要提取的数据，`401`类资源至少包含`name`和`year`两个关键字，`403`类至少有`name`|
|`{name}.{year}.{source}.{resolution}.{codec}-{group}`|发布资源名|string|N|发布资源的标题名，由关键字和普通字符组成，关键字使用`{}`，且只能使用资源名格式字段中使用过的关键字，缺省则直接使用原资源名发布|

* 会不定期更新，不会写可以来gayhub更新config

#### 匹配规则

* 定义关键字，及该关键字的正则匹配式

|compile|正则表达式||
|:---:|:---:|:---:|
|key|value|type|
|name|`(.+?)`|string|
|year|`(\\d+)`|string|
|ep|`(\\d+)`|string|
|...|...|string|

* 会不定期更新，不会写可以gayhub更新config

### 2 使用

#### requirements
- [x] bs4
- [x] requests

> pip3 install bs4
> 
> pip3 install requests

#### uTorrent

* 为RSS的UT填入下载完成后运行 `~\script_for_ut\autoseed_0day\start.bat "%D" "%N" "%F"`

![](https://img.ajycc20.xyz/imgs/2019/05/07ebc7bd5509f8fb.png)

**enjoy!该ut完成的所有种子，只要符合规则都会自动发布，并下载种子至ut_load路径，由另一个ut载入做种**

<!--

1. 添加[动漫花园](share.dmhy.org)的[rss链接](https://share.dmhy.org/topics/rss/sort_id/2/rss.xml) 可能需要添加个人中心的`uTorrent Key`
2. 添加适配`config.json`里匹配的字幕组rss规则
3. ...

|ut打开路径|填写值|说明|
|:---:|:---:|:---:|
|右键RSS订阅规则,保存路径|`J:\DMHY`|rss保存路径，请与下载路径一致|
|选项-设置-目录-新建下载放置|`J:\DMHY`|下载默认位置，请与rss保存路径一致|
|选项-设置-目录-保存Torrent至|`F:\utorrent2.2.1\utorrent`|请与`config.json`里`ut_save`路径一致|
|选项-设置-目录-自动载入Torrent于|`F:\dmhyload`|请与`config.json`里`ut_load`路径一致，并勾上删除载入的Torrent|
|选项-设置-高级-运行程序-下载完成时运行|`F:\autoseed_0day\start.bat "%D" "%N" "%F"`|项目`start.bat`文件路径|

#### FAQ
1. `搜不到bgm链接，输入这个番更通俗易懂的名字叭：`
   
   自行前往`bgm.tv`搜索该番的中文名
2. `中译名是xxx吗`

   每个番第一次下载都会出现的，如果脚本匹配无误直接回车即可
3. `upload种子上传失败`
   
   两种情况，一是网站已有该种子；二是自动做种时检测到的从NYPT`down`下的种子会弹出，关闭即可
4. `其他问题`
   
   可能是网不好引起的一系列2333333
-->

