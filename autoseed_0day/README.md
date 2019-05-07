# autoseed
![](https://img.shields.io/badge/python-3.7-red.svg)

可以把ut2.14↑rss回来的东西直接转发到南洋。<br>

## 使用方法

### 1 配置

把config.json里东西填好，ut_save是ut下载后保存种子文件（.torrent）的目录，ut_load是用来做种的ut自动加载种子的目录，请使用反斜杠，填完后运行test.py，建议ut下载文件保存位置固定。

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