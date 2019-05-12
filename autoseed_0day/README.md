# autoseed
![](https://img.shields.io/badge/python-3.7-red.svg) ![](https://img.shields.io/badge/ny-support-blue.svg)

可以把ut2.14↑rss回来的东西直接转发到南洋。<br>

## 使用方法

### 1 配置config

#### nanyang

把cookie填上去。

#### path

建议使用两个ut进项操作，第一个ut用来rss，将其下载后保存种子文件（.torrent）的目录填入ut_save，第二个ut用来做种，将ut自动加载种子的目录填入ut_load，请使用反斜杠，建议两个ut下载文件保存位置设为一致。

#### namerule

key是压制组名/字幕组名，value为一个列表，value[0]为种类，比如401为电影，403为动漫；value[1]为改压制组的命名规则，使用关键词代替，value[2]为发种命名规则，可省缺；如果同一个压制组有多种命名规则，请用双重列表。每一次rss前都确保有其命名规则。

### 2 使用

安装依赖
```powershell
pip3 install bs4
pip3 install requests
```

ut-设置-高级-运行程序-完成时运行程序；把这个东西填上去（~替换为start.bat的准确路径）：
```ut
\~\start.bat "%D" "%N" "%F"
```