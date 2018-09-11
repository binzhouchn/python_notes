[**1. pycharm远程配置**](#pycharm远程配置)

[**2. 远程ipython http版**](#远程ipython_http版)

[**3. 远程ipython https安全版**](#远程ipython_https安全版)

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
```
wget https://mirrors.tuna.tsinghua.edu.cn/anaconda/archive/
```
PATH in your /root/.bashrc: 
```
export PATH="/root/anaconda2/bin:$PATH"
```
 - 1. 'sha1:01f0def65085:059ed81ab3f5658e7d4d266f1ed5394e9885e663'

 - 2. ipython profile create nbserver

 - 3. mkdir certs 
      cd certs 
      然后 openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mycert.pem -out mycert.pem

 - 4. 我们重点要关注的是 cd .ipython/profile_nbserver <br>
      ipython_notebook_config.py这个文件，待会儿我们要修改该文件来配置服务器。不过，有时候这个文件不能生成，这时候我们自己在这里新建即可，使用vim或者gedit。我自己配置的时候就没有生成ipython_notebook_config.py这个文件，我使用vim新建了一个： 
      然后把一下代码复制进去（替换certfile路径和sha1），保存

（不需要这步 #找不到notebook config文件 
```bash
#jupyter notebook —generate-config）
```
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

---

jupyter是ipython的升级版，它的安装也非常方便，一般Anaconda安装包中会自带。安装好以后直接输入jupyter notebook便可以在浏览器中使用。但是它默认只能在本地访问，如果想把它安装在服务器上，然后在本地远程访问，则需要进行如下配置：