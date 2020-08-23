## nginx

[docker nginx反向代理](https://www.cnblogs.com/dotnet261010/p/12596185.html)<br>
[nginx负载均衡参考1](https://www.jianshu.com/p/4c250c1cd6cd)<br>
[nginx负载均衡参考2](https://www.cnblogs.com/diantong/p/11208508.html)<br>

### nginx使用

1. 第一步用安装docker nginx

```shell
docker pull nginx:latest
```

2. 开启nginx和两个flask服务(用来模拟多个服务器的)

```shell
# 开启nginx
docker run --name=nginx -d -p 4030:80 nginx #网页访问端口4030
# 开启两个flask server
docker run -d -p 5001:5001 -v $PWD/flask_nginx_test:/usr/src/flask_nginx_test  -w /usr/src/flask_nginx_test binzhouchn/python36:1.4 python test1.py
docker run -d -p 5002:5002 -v $PWD/flask_nginx_test:/usr/src/flask_nginx_test  -w /usr/src/flask_nginx_test binzhouchn/python36:1.4 python test2.py
```

开启以后单独访问<br>
localhost:4030会进入nginx欢迎界面<br>
localhost:5001页面显示BINZHOU TEST 1<br>
localhost:5002页面显示BINZHOU TEST 2<br>

3. 配置nginx配置文件

文件在/etc/nginx/nginx.conf，由于这个文件include /etc/nginx/conf.d/*.conf;所以直接到/etc/nginx/conf.d/下面更改default.conf即可<br>
[更改后的default.conf](default.conf)

