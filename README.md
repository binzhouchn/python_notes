
[![Analytics](https://ga-beacon.appspot.com/GA-80121379-2/notes-python)](https://github.com/binzhouchn/feature_engineering)

# python笔记
> 版本：0.0.4<br>
> 作者：binzhou<br>
> 邮件：binzhouchn@gmail.com<br>

`Github`加载`ipynb`的速度较慢，建议在 [Nbviewer](http://nbviewer.ipython.org/github/lijin-THU/notes-python/blob/master/index.ipynb) 中查看该项目。

---

## 简介

默认安装了 `Python 3.6`，以及相关的第三方包  `numpy`， `pandas`，`sklearn`

> life is short.use python.

推荐使用[Anaconda](http://www.continuum.io/downloads)，这个IDE集成了大部分常用的包。

### 以下两个镜像由于授权问题anaconda安装包下载已经不可用
推荐下载[Anaconda-tsinghua](https://mirrors.tuna.tsinghua.edu.cn/)，清华镜像下载速度快。
或者[USTC](https://mirrors.ustc.edu.cn/)科大

### python pip使用国内镜像

[让python pip使用国内镜像](https://www.cnblogs.com/wqpkita/p/7248525.html)

```
临时使用：
pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com flask
# 如果是公司电脑且有代理，本地进入docker python3.5后需要加个代理再安装相关的包
pip --proxy=proxyAddress:port install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com flask
```

### pip镜像配置

pip install镜像配置（Linux）
```
# 先在home或者和anaconda文件夹平级的的.pip文件夹下新建pip.conf配置文件然后把以后代码复制进去
[global]
trusted-host = pypi.tuna.tsinghua.edu.cn
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```
pip install镜像配置（Windows）
```
# 进入目录（C:\Users\Administrator）下新建一个pip文件夹，文件夹里建一个pip.ini 文本文件，内容如下：
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
[install]
trusted-host =  pypi.tuna.tsinghua.edu.cn
或者
[global]
index-url = http://mirrors.aliyun.com/pypi/simple/
[install]
trusted-host = mirrors.aliyun.com
```
