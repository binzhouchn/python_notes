[**1. pycharm远程配置**](#pycharm远程配置)

[**2. 远程ipython http版**](#远程ipython_http版)

[**3. 远程ipython https安全版**](#远程ipython_https安全版)

[**4. jupyter notebook启动错误总结**](#jupyter_notebook启动错误总结)

[**5. 添加Anaconda虚拟环境**](#添加anaconda虚拟环境)

# pycharm远程配置

pycharm远程配置： <br>
file->Settings->Project Interpreter->加入远程ssh的连接和python的执行文件地址 <br>
然后再加一个path mappings（本地和远程的文件存储地址）

文件同步配置： <br>
Tools->Deployment->Configuration->添加一个新SFTP <br>
Root path选远程文件夹 <br>
Web server root URL: http:/// <br>
Mappings选local path工程目录，其他的都为/ <br>

done!

# 远程ipython_http版

1. 打开ipython
```python
from notebook.auth import passwd
In [2] : passwd() # 输入密码
Enter password:
Verify password:
Out[2]: 'sha1:f9...'
```

2. 新建jupyter_config.py，输入如下配置。
```bash
c.NotebookApp.password = u'sha1:f9...'
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
```

3. 启动jupyter notebook 并指定配置文件，输入如下命令。
```bash
jupyter notebook --config=jupyter_config.py
```

4. 若客户端浏览器无法打开jupyter，有可能是防火墙的缘故，输入如下命令开放对应的
的端口（若使用IPv6，把命令iptables改成ip6tables）
```bash
iptables -I INPUT -p tcp --dport 8888 -j ACCEPT
iptables save
```

# 远程ipython_https安全版

通过mac终端登录： <br>
sudo ssh -p 22 ubuntu@182.254.247.182 <br>
z1234.. <br>
安装教程和视频（在本机） <br>
http://blog.csdn.net/hshuihui/article/details/53320144 <br>

安装ipython notebook on 百度云 <br>
```bash
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/
```
PATH in your .bashrc or .bash_profile 
```bash
export PATH="/root/anaconda2/bin:$PATH"
```
在服务器上启动IPython，生成自定义密码的sha1
```python
In [1]: from IPython.lib import passwd
In [2]: passwd()
Enter password:
Verify password:
Out[2]: 'sha1:01f0def65085:059ed81ab3f5658e7d4d266f1ed5394e9885e663'
```
创建IPython notebook服务器
```bash
ipython profile create nbserver
```
生成mycert.pem
```bash
mkdir certs 
cd certs 
然后openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem
```
我们重点要关注的是 cd .ipython/profile_nbserver <br>
ipython_notebook_config.py这个文件，待会儿我们要修改该文件来配置服务器。不过，有时候这个文件不能生成，
这时候我们自己在这里新建即可，使用vim或者gedit。我自己配置的时候就没有生成ipython_notebook_config.py这个文件，我使用vim新建了一个： 
然后把以下代码复制进去（替换certfile路径和sha1），保存

```bash
# Configuration file for ipython-notebook
c = get_config()
#Kernel config
c.IPKernelApp.pylab = 'inline'
#Notebook config
c.NotebookApp.certfile = u'/root/certs/mycert.pem'
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser =  False
c.NotebookApp.password = u'sha1:375df20c451e:16f5535e55154eb3490dbcb83d8cb930ef3c3799'
c.NotebookApp.port = 8888
```
启动命令： <br>
```bash
ipython notebook --config=/root/.ipython/profile_nbserver/ipython_notebook_config.py
```
```bash
nohup ipython notebook --config=/root/.ipython/profile_nbserver/ipython_notebook_config.py 
如果想关闭nohup先lsof nohup.out 然后kill -9 [PID] 
登录ipython notebook:
```

或者建一个jupyter_config.py文件然后输入(http访问)<br>
```python
c.NotebookApp.password = u'sha1:ebf4c635f6b6:7d6824aa8f863ffbe7c264b28854ec2acf1a0961'
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.port = 8888
```
然后用命令行启动
```shell
nohup jupyter notebook --config=jupyter_config.py
```

---

Jupyter Notebook 添加目录插件<br>

```bash
pip install jupyter_contrib_nbextensions
```
```bash
jupyter contrib nbextension install --user --skip-running-check
```
注意配置的时候要确保没有打开Jupyter Notebook

# The installation of the Java Jupyter Kernel

要求jdk11及以上，maven3.6.3及以上<br>
```shell
java --list-modules | grep "jdk.jshell"

> jdk.jshell@12.0.1
```
```shell
git clone https://github.com/frankfliu/IJava.git
cd IJava/
./gradlew installKernel
```
然后启动jupyter notebook即可，选java kernel的notebook

### Run docker image

```shell
cd jupyter
docker run -itd -p 127.0.0.1:8888:8888 -v $PWD:/home/jupyter deepjavalibrary/jupyter
```

# jupyter_notebook启动错误总结

[Jupyter Notebook "signal only works in main thread"](https://blog.csdn.net/loovelj/article/details/82184223)<br>
查询了很多网站，最后发现是两个包版本安装不对，重新安装这两个包就就可以了<br>
```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple "pyzmq==17.0.0" "ipykernel==4.8.2"
```

# 添加anaconda虚拟环境

把anaconda3整个文件夹拷贝到anaconda3/envs下，然后取名为比如tf-gpu<br>
然后可以把这个文件夹下的包的版本可以自行替换比如把tf2.0替换成tf1.14（注：不要删除，会有问题）<br>
然后在jupyter notebook添加Anaconda虚拟环境的python kernel
```shell
conda create -n tf-gpu python=3.8 # 创建tf-gpu虚拟环境
source activate tf-gpu # 激活tf-gpu环境
conda deactivate # 退出虚拟环境
conda install ipykernel # 安装ipykernel模块(如果是虚拟机没联网，可以去https://anaconda.org/conda-forge/ipykernel/files下载)
python -m ipykernel install --user --name tf-gpu --display-name "tf-gpu" # 进行配置
jupyter notebook # 启动jupyter notebook，然后在"新建"中就会有py3这个kernel了 
```
虚拟环境启动notebook<br>
```shell
1. conda install jupter notebook（如果不行，主环境的site-package整个拷贝到envs/下的虚拟环境）
2. 虚拟环境安装jupyter_nbextensions_configurator（https://zodiac911.github.io/blog/jupyter-nbextensions-configurator.html）
3. 虚拟环境conda install nb_conda/conda install nb_conda_kernels
```

