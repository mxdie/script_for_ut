# autoseed
![](https://img.shields.io/badge/python-3.7-red.svg)

可以把ut2.14↑下载的动漫直接转发到南洋。<br>

## 使用方法

### 1 配置

把config.json里东西填好，ut_save是ut下载后保存种子的目录，ut_load是ut自动加载种子的目录，请使用反斜杠。

### 2 使用

安装依赖
```powershell
pip3 install bs4
pip3 install requests
```

ut-设置-高级-运行程序-完成时运行程序
```ut
~\1.bat "%N" "%D" 
```