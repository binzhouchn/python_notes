
[![Analytics](https://ga-beacon.appspot.com/GA-80121379-2/notes-python)](https://github.com/binzhouchn/feature_engineering)

# python笔记
> 版本：0.5<br>
> 作者：binzhou<br>
> 邮件：binzhouchn@gmail.com<br>

`Github`加载`ipynb`的速度较慢，建议在 [Nbviewer](http://nbviewer.ipython.org/github/lijin-THU/notes-python/blob/master/index.ipynb) 中查看该项目。

[python各版本下载仓库](https://www.python.org/ftp/python/)<br>

---

## 简介

默认安装了 `Python 3.10`，以及相关的第三方包 `gensim`, `tqdm`, `flask`

anaconda 虚拟环境创建python版本降级命令：conda create -n tableqa python=3.9

> life is short.use python.

推荐使用[Anaconda](http://www.continuum.io/downloads)，这个IDE集成了大部分常用的包。

<details open>
<summary>pip使用国内镜像</summary>

[让python pip使用国内镜像](https://www.cnblogs.com/wqpkita/p/7248525.html)
```shell
pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com xx包
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple xx包
pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com xx包 --use-feature=2020-resolver #解决安装包时冲突问题
```
```
临时使用示例：
pip install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com flask
# 如果是公司电脑且有代理，本地进入docker python3.6后需要加个代理再安装相关的包
pip --proxy=proxyAddress:port install -i http://pypi.douban.com/simple --trusted-host pypi.douban.com flask
```

</details>

<details open>
<summary>pip镜像配置</summary>

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
</details>

## 使用conda升级到python3.12

方法一<br>
https://qa.1r1g.com/sf/ask/4099772281/)<br>
```shell
conda update -n base -c defaults conda
conda install -c anaconda python=3.12
#然后再重新安装下依赖包
```
方法二(或使用虚拟环境)<br>
```
$ conda create -p /your_path/env_name python=3.12
# 激活环境
$ source activate /your_path/env_name
# 关闭环境
$ source deactivate /your_path/env_name
# 删除环境
$ conda env remove -p  /your_path/env_name
```

## 其他python仓库推荐

[All algorithms implemented in Python - for education](https://github.com/TheAlgorithms/Python/)<br>
