# simple use for docker

## 1. docker安装及配置Docker镜像站

1.1 mac下安装<br>
[mac安装网址](https://hub.docker.com/editions/community/docker-ce-desktop-mac)<br>
[docker docs for mac](https://docs.docker.com/docker-for-mac/)<br>

1.2 linux下安装<br>
TODO

1.3 配置docker镜像站<br>
[docker镜像站网址](https://www.daocloud.io/mirror#accelerator-doc)<br>

1.4 配置docker代理<br>

 - windows中右击图标，选settings->Proxies
 - [mac/linux](https://www.cnblogs.com/EasonJim/p/9988154.html)

```shell
# 如果使用HTTP代理服务器时，将为docker服务创建systemd插件目录
mkdir -p /etc/systemd/system/docker.service.d
# 创建一个名为的文件/etc/systemd/system/docker.service.d/http-proxy.conf，添加HTTP_PROXY环境变量
[Service]
Environment="HTTP_PROXY=http://proxy.example.com:80/"
# 或者，如果使用HTTPS代理服务器，那么再创建一个名为/etc/systemd/system/docker.service.d/https-proxy.conf 添加HTTPS_PROXY环境变量
[Service]
Environment="HTTPS_PROXY=https://proxy.example.com:443/"
# 为Docker配置不代理的地址时，可以通过NO_PROXY环境变量指定它们，比如HTTP代理服务器的配置
[Service]    
Environment="HTTP_PROXY=http://proxy.example.com:80/" "NO_PROXY=localhost,127.0.0.1,docker-registry.somecorporation.com"
[Service]    
Environment="HTTPS_PROXY=https://proxy.example.com:443/" "NO_PROXY=localhost,127.0.0.1,docker-registry.somecorporation.com"
# 重新读取服务的配置文件
systemctl daemon-reload
# 重启Docker
systemctl restart docker
# 验证是否已加载配置
systemctl show --property=Environment docker
```


## 2. docker基本命令

2.1 docker查看版本及images
```shell
docker --version
docker images
```

2.2 docker run
```shell
docker run hello-world
# run之前如果没有这个images，则会从docker_hub上先pull下来 docker pull hello-world
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

2.4 docker打开image bash编辑，比如打开python镜像bash下载一些包再保存
```shell
docker pull python:3.5
docker run -t -i python:3.5 /bin/bash
# 接下去进行一些pip install一些包等操作
docker commit -m="has update" -a="binzhou" <container_id> binzhouchn/python35:v2
```

2.5 docker保存和读取image（存成tar文件）
```shell
# 保存
docker save -o helloword_test.tar fce45eedd449(image_id)
# 读取
docker load -i helloword_test.tar
```

2.6 docker保存和读取container
```shell
# 保存
docker export -o helloword_test.tar fce45eedd444(container_id)
# 读取
docker import ...
```

2.7 修改repository和tag名称
```shell
# 加载images后可以名称都为<none>
docker tag [image id] [name]:[版本]
```

2.8 用dockerfile建一个image，并上传到dockerhub
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

2.9 要获取所有容器名称及其IP地址只需一个命令 
```shell
docker inspect -f '{{.Name}} - {{.NetworkSettings.IPAddress }}' $(docker ps -aq)
```

2.10 查找依赖容器
```shell
docker image inspect --format='{{.RepoTags}} {{.Id}} {{.Parent}}' $(docker image ls -q --filter since=<image_id>)
```

2.11 批量删除停止容器
```shell
docker rm $(sudo docker ps -a -q)
```

2.12 docker修改完镜像生成新的镜像以后貌似没看法删除旧的镜像
```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy 
pandas sklearn jieba gensim tqdm flask requests PyMySQL redis 
pymongo pyspark py2neo neo4j-driver==$PYTHON_DRIVER_VERSION
```

## 3. docker镜像使用

3.1 docker跑一个helloworld
```shell
docker run  -v $PWD/myapp:/usr/src/myapp  -w /usr/src/myapp python:3.5 python helloworld.py
# 本地需要建一个myapp文件夹，把helloworld.py文件放文件夹中，然后返回上一级cd ..
命令说明：
-v $PWD/myapp:/usr/src/myapp :将主机中当前目录下的myapp挂载到容器的/usr/src/myapp
-w /usr/src/myapp :指定容器的/usr/src/myapp目录为工作目录
python helloworld.py :使用容器的python命令来执行工作目录中的helloworld.py文件
```

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
sql = "INSERT INTO tt(a, b, date) VALUES ('%d', '%s', '%s')"
data = (306, '插入6', '20190615')
cursor.execute(sql % data)
db.commit()

# 起了mysql服务以后，在用docker python去插入数据
# 需要先查看docker mysql的容器ip地址，命令看2.8
# 然后localhost改成mysql容器的ip地址即可，其他一样

```

3.3 docker用redis镜像
```
# 启动redis命令
docker run --name docker-redis-test -p 6379:6379  -d redis:latest --requirepass "123456"
# redis客户端连接命令
docker exec -it <container_id> redis-cli
# 进去以后的操作
auth 123456
set name zhangsan
get name 
quit

# python连接docker起的redis服务
import redis
r = redis.Redis(host='localhost', port=6379, password='123456')
r.set('name', 'John')
print(r.get('name'))

# redis可视化工具RDM(已安装)
```

3.4 docker用mongo镜像
```
# 启动mongodb命令
docker run -p 27017:27017 -v $PWD/mongo_db:/data/mongo_db -d mongo:4.0.10
# 连接到mongo镜像cli
docker run -it mongo:4.0.10 mongo --host <容器ip>

# 建database建collection比如runoob然后插入数据
db.runoob.insert({"title": 'MongoDB 教程', 
    "description": 'MongoDB 是一个 Nosql 数据库',
    "by": 'w3cschool',
    "url": 'http://www.w3cschool.cn',
    "tags": ['mongodb', 'database', 'NoSQL'],
    "likes": 100})
db.runoob.find()

# python连接docker起的mongo服务
import pymongo
mongodb_host = 'localhost'
mongodb_port = 27017
# pymongo.MongoClient(mongodb_host, 27017, username='test', password='123456')
myclient = pymongo.MongoClient('mongodb://localhost:27017/')
myclient.list_database_names()
mydb = myclient["mongo_testdb"]
mydb.list_collection_names()
mycol = mydb["runoob"]
# 创建collection
mydb.create_collection('test2')
# 插入数据
mydict = { "name": "Google", "age": "25", "url": "https://www.google.com" }
mycol.insert_one(mydict)
# 查看数据
list(mycol.find())
```

3.5 docker用elasticsearch镜像
```
# Run Elasticsearch 
docker run -d --name elasticsearch_for_test -p 9200:9200 -e "discovery.type=single-node" elasticsearch:6.6.0
# 安装elasticsearch-head 已安装googlechrome插件


TODO
```


3.6 docker用neo4j镜像
```
# docker启动neo4j服务
docker run \
    --publish=7474:7474 --publish=7687:7687 \
    --volume=$PWD/neo4j/data:/data \
    -d neo4j:latest

# 然后登陆网页可视化界面

# 或使用Cypher shell
docker exec --interactive --tty <container_id> bin/cypher-shell
# 退出:exit
```

3.7 stardog


