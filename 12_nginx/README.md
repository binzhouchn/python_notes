## nginx

[**1. nginx入门使用**](#nginx入门使用)

[**2. nginx正则使用1（2024.4.2更新）**](#nginx正则使用1)



---

### nginx入门使用

<details close>
<summary>点击展开</summary>

**1. 第一步用安装docker nginx**

```shell
docker pull nginx:latest
```

**2. 开启nginx和两个flask服务(用来模拟多个服务器的)**

```shell
# 开启nginx
docker run --name=nginx -d -p 4030:80 nginx #网页访问端口4030
# 开启两个flask server
docker run -d -p 5001:5001 -v $PWD/flask_nginx_test:/usr/src/flask_nginx_test  -w /usr/src/flask_nginx_test binzhouchn/python36:1.4 python test1.py
docker run -d -p 5002:5002 -v $PWD/flask_nginx_test:/usr/src/flask_nginx_test  -w /usr/src/flask_nginx_test binzhouchn/python36:1.4 python test2.py
```

nginx配置前，开启以后单独访问<br>
localhost:4030会进入nginx欢迎界面<br>
localhost:5001页面显示BINZHOU TEST 1<br>
localhost:5002页面显示BINZHOU TEST 2<br>

**3. 配置nginx配置文件**

文件在/etc/nginx/nginx.conf，由于这个文件include /etc/nginx/conf.d/*.conf;所以直接到/etc/nginx/conf.d/下面更改default.conf即可<br>
[更改后的default.conf](default.conf)

注：
这里172.17.0.3这些是docker虚拟ip地址，docker之间通信可以通过这个地址 <br>
负载均衡通过轮询方式 <br>
172.17.0.5:5003这个端口并没有开启，会自动忽略 <br>

**4. 配置完后重启ngix**

```shell
# 先进到ngix docker里面/etc/nginx/config.d中运行nginx -t看下是否success
docker stop <container id>
docker start <container id>
```

配置完nginx以及重启后，再访问<br>
localhost:4030页面会显示BINZHOU TEST 1；再刷新(重载)会显示BINZHOU TEST 2；再刷新BINZHOU TEST 1

**说明nginx已经自动转到两个服务器去了**<br>

**5. 配置文件扩展**

5.1 一台nginx服务器，通过指定不同端口(比如4030和4031)来达到访问不同应用的目的<br>
```shell
# docker开启nginx命令如下，映射两个端口
docker run --name=nginx -d -p 4030:4030 -p 4031:4031 nginx
```
[配置文件1](default1.conf)

5.2 一台nginx服务器，通过不同的路由(比如/project/guoge)来达到访问不同应用的目的<br
```shell
# docker开启nginx命令如下，只映射一个端口
docker run --name=nginx -d -p 4030:4030 nginx
```
```python
# flask部分文件如下
# 创建路由2
@app.route('/project/guoge')
def custom():
    return str(3 + 2)
```
[配置文件2](default2.conf)

</details>

### nginx正则使用1

```shell
cd /etc/nginx/conf.d
#修改后重启
systemctl restart nginx
nginx -s reload
```
[配置文件3](default3.conf)

说明：本次使用正则的目的是当我访问<br>
http://10.28.xx.xx:8000/aimanager_gpu/recsys/时，<br>
正则匹配后转到http://localhost:10086，后面不加/aimanager_gpu/recsys路由<br>
（如果不走正则那么转到http://localhost:10086后会自动拼接/aimanager_gpu/recsys）<br>




 - 参考资料

[nginx作为http服务器-静态页面的访问](https://www.cnblogs.com/xuyang94/p/12667844.html)<br>
[docker nginx反向代理](https://www.cnblogs.com/dotnet261010/p/12596185.html)<br>
[nginx负载均衡参考1](https://www.jianshu.com/p/4c250c1cd6cd)<br>
[nginx负载均衡参考2](https://www.cnblogs.com/diantong/p/11208508.html)<br>