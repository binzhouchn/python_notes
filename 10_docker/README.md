# simple use for docker

## 1. docker安装

1.1 mac下安装<br>
[mac安装网址](https://hub.docker.com/editions/community/docker-ce-desktop-mac)<br>
[docker docs for mac](https://docs.docker.com/docker-for-mac/)<br>

1.2 linux下安装<br>
TODO

## 2. docker基本命令

2.1 docker查看版本及images
```shell
docker --version
docker images
```

2.2 docker run
```shell
docker run hello-world
```

2.3 docker跑完以后需要删除container再删除image
```shell
# 查看image对应的container id
docker ps -a
# 删除container
docker rm container_id
# 删除image
docker rmi image_id
# 也可以直接暴力删除image
docker rmi -f image_id
# 如果存在同名同id不同tag的镜像
可以使用repository：tag的组合来删除特殊的镜像
```

2.4 docker保存和读取image
```shell
# 保存
docker save -o helloword_test.tar fce45eedd449(image_id)
# 读取
docker load -i helloword_test.tar
```

2.5 docker保存和读取container
```shell
# 保存
docker export -o helloword_test.tar fce45eedd444(container_id)
# 读取
docker import ...
```

2.6 修改repository和tag名称
```shell
# 加载images后可以名称都为<none>
docker tag [image id] [name]:[版本]
```

2.7 用dockerfile建一个image，并上传到dockerhub
```
# 建一个dockerfile
cat > Dockerfile <<EOF
FROM busybox
CMD echo "Hello world! This is my first Docker image."
EOF
# 上面命令的效果的vi Dockerfile，然后填入
FROM busybox
CMD echo "Hello world! This is my first Docker image."

# build image建镜像
docker build -t binzhouchn/my-first-repo .
# 刚建完的docker镜像上传到我的仓库
docker push binzhouchn/my-first-repo
```

## 3. docker镜像使用

3.1 docker跑一个简单的flask demo(用到python3.5镜像)
```shell
# -d后台运行 -p端口映射
docker run -d -p 5000:5000 -v $PWD/myapp:/usr/src/myapp  -w /usr/src/myapp binzhou/python35:v2 python app.py
```

3.2 docker用mysql镜像
```
# 先下载镜像
docker pull mysql:5.5
# 运行容器 可以先把-v去掉
docker run -p 3306:3306 --name mymysql -v $PWD/conf:/etc/mysql/conf.d -v $PWD/logs:/logs -v $PWD/data:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=123456 -d mysql:5.5

-p 3306:3306：将容器的 3306 端口映射到主机的 3306 端口。
-v -v $PWD/conf:/etc/mysql/conf.d：将主机当前目录下的 conf/my.cnf 挂载到容器的 /etc/mysql/my.cnf。
-v $PWD/logs:/logs：将主机当前目录下的 logs 目录挂载到容器的 /logs。
-v $PWD/data:/var/lib/mysql ：将主机当前目录下的data目录挂载到容器的 /var/lib/mysql 。
-e MYSQL_ROOT_PASSWORD=123456：初始化 root 用户的密码。

# 用三方工具Navicat或者python连接，先建好db比如test_db
import pymysql
# 打开数据库连接
db = pymysql.connect("localhost","root","123456","test_db")
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
```

3.3 docker





