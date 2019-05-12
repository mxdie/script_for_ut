# autoseed
![](https://img.shields.io/badge/python-3.7-red.svg)

可以把ut2.14↑rss回来的东西直接转发到南洋。

## 使用方法

> clone 本项目至本地任一文件夹

### 1 配置config

#### nanyang

把cookie填上去。

#### path

* `ut_save`: `"F:/utorrent2.2.1/utorrent/"`  本地utorrent路径
* `ut_load`: `F:/dmhyload/` 本地任一空文件夹

#### namerule

> 以喵萌字幕组为例

|namerule||
|:---:|:---:|
|key|value|
|Nekomoe kissaten|[403,"[group][name][ep][resolution][sub].format","{name}.{ep}.TVRip.{sub}.{resolution}.{format}-{group}"]|

**值参数:**

|字段|字段说明|类型|必填|说明|
|:---:|:---:|:---:|:---:|:---:|
|403|资源类别|int|Y|网站种子分类的`cat`参数|
|`[group][name][ep][resolution][sub].format`|种子名|string|Y|种子名,如`[Nekomoe kissaten][Grisaia Phantom Trigger][02][720p][CHS].mp4`|
|`{name}.{ep}.TVRip.{sub}.{resolution}.{format}-{group}`|发布资源名|string|Y|网站种子主标题名,如`Grisaia.Phantom.Trigger.02.TVRip.CHS.720p.mp4-Nekomoe kissaten`|

> 匹配规则

|compile|正则表达式||
|:---:|:---:|:---:|
|key|value|type|
|name|`(.+?)`|string|
|year|`(\\d+)`|string|
|ep|`(\\d+)`|string|
|resolution|`(720p|1080p|2160p)`|string|
|source|`(bluray|web-dl|bdrip)`|string|
|...|...|string|

>自行修改添加

### 2 使用

#### requirements
- [x] bs4
- [x] requests

#### uTorrent

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
