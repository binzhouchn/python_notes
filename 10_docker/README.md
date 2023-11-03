# simple use for docker

## 1. docker安装及配置Docker镜像站

1.1 mac下安装<br>
[mac安装网址](https://hub.docker.com/editions/community/docker-ce-desktop-mac)<br>
[docker docs for mac](https://docs.docker.com/docker-for-mac/)<br>

1.2 linux下安装<br>
[Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)

1.3 配置docker镜像站<br>
[docker镜像站网址](https://www.daocloud.io/mirror#accelerator-doc)<br>

1.4 配置docker代理<br>

 - windows中右击图标，选settings->Proxies
 - [mac](https://www.cnblogs.com/EasonJim/p/9988154.html)
 - [linux](https://blog.csdn.net/qq_30034989/article/details/132021346)

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
systemctl restart docker #或者sudo service docker restart
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

2.3 如果不小心关了container或者重启了电脑
```
# 先查看container历史
docker ps -a
# 重启container即可，前提是docker run的时候要加-volume把数据挂载到本地
docker start <container_id>
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
# 如果原来的镜像已经启动了container，则
docker exec -it <container_id> /bin/bash
# 进去修改完后
docker start <container_id>
#------------------------------------------
docker pull python:3.6
docker run -it python:3.6 /bin/bash #启动镜像并进入到shell页面
docker run -dit python:3.6 /bin/bash #如果只是想启动并后台运行
# 接下去进行一些pip install一些包等操作
docker commit -m="has update" -a="binzhouchn" <container_id> binzhouchn/python36:1.3
```

2.5 docker保存和读取image（存成tar.gz文件）
```shell
# 保存
docker save -o helloword_test.tar fce45eedd449(image_id)
#或者docker save -o mydocker.tar.gz mydocker:1.0.0
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

2.11 批量停止并删除容器
```shell
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

2.12 docker修改完镜像生成新的镜像以后貌似没看法删除旧的镜像
```shell
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple numpy 
pandas sklearn jieba gensim tqdm flask requests PyMySQL redis pyahocorasick  
pymongo pyspark py2neo neo4j-driver==$PYTHON_DRIVER_VERSION
```

2.13 拷贝宿主机本地文件到docker中，和从docker中拷贝到宿主机
```shell
#1
docker cp test.txt <container id>:/home
#2
docker cp <container id>:/home/xx.txt /opt
```

2.14 根据镜像名定位到已经开启python:3.6镜像容器的id
```shell
docker ps -a| grep python:3.6 | awk '{print $1}' #方法一
docker ps -aq --filter ancestor=python:3.6 #方法二
# 根据镜像名停止和删除容器
docker stop `docker ps -a| grep python:3.6 | awk '{print $1}'`
docker rm `docker ps -a| grep python:3.6 | awk '{print $1}'`
```

2.15 docker中python print不生效解决办法
```shell
#方法一 显式调用flush
print("Hello www", flush=True)
#方法二 使用 "-u" 参数执行 python 命令
sudo nvidia-docker run -v $PWD/masr_bz:/workspace/masr_bz  -w /workspace/masr_bz binzhouchn/pytorch:1.7-cuda10.1-cudnn7-masr python -u train.py
```


## 3. docker镜像使用

【3.0 工作中】<br>
**方法一(环境和代码独立，代码放外面)**
```shell

 - 配置好环境镜像比如binzhouchn/python36:1.4
 - docker run -d -p 5005:5005 -v $PWD/xx_service:/usr/src/xx_service -w /usr/src/xx_service binzhouchn/python36:1.4 gunicorn -b :5005 server:app
```

**方法二（代码放在镜像里面为一个整体）**<br>
```shell
#构建Dockerfile
FROM binzhouchn/python36:1.4
MAINTAINER zhoubin zhoubin@qq.com
COPY target/xx_service /usr/src/xx_service
WORKDIR /usr/src/xx_service
ENTRYPOINT ["gunicorn", "-b", ":5005", "server:app"]
#run dockerfile
docker build -t binzhouchn/new_img:0.1 .
#run image(后台运行，5005映射出来)
docker run -d -p 5005:5005 new_img:0.1
```


3.1 docker跑一个helloworld
```shell
docker run -v $PWD/myapp:/usr/src/myapp  -w /usr/src/myapp python:3.5 python helloworld.py
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
# pymongo.MongoClient(mongodb_host, mongodb_port, username='test', password='123456')
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
# 安装elasticsearch-head
```
```python
# 用python连接，并进行增删改查
from elasticsearch import Elasticsearch
from elasticsearch import helpers
# es = Elasticsearch(hosts="localhost:9200", http_auth=('username','passwd'))
esclient = Elasticsearch(['localhost:9200'])
# 高效插入ES
action1 = {
        "_index": "idx111",
        "_type": "test",
#         "_id": ,
        "_source": {
            'ServerIp': '0.1.1.1',
            'SpiderType': 'toxic',
            'Level': 4
        }
}
action2 = {
        "_index": "idx111",
        "_type": "pre",
#         "_id": 1,
        "_source": {
            'ServerIp': '0.1.1.2',
            'SpiderType': 'non-toxic',
            'Level': 1
        }
}
actions = [action1, action2]
helpers.bulk(esclient, actions)

#---------------------------------------------------
# 创建schema然后单条插入数据
# 类似创建schema
answer_index = 'baidu_answer'
answer_type = 'doc22'
esclient.indices.create(answer_index)
answer_mapping = {
        "doc22": {
            "properties": {
                "id": {
                    "type": "integer",
                    # "index": True
                },
                "schoolID":{
                    "type":"text"
                },
                "schoolName":{
                    "type": "text",
                    "analyzer": "ik_max_word" # 这个需要安装，先run docker6.6.0然后docker exec -it <container_id> /bin/bash下载解压ik后exit然后restart这个container即可，之后可以新生成一个image
#                     "analyzer":"whitespace"
                },
                "calNum":{
                    "type":"float"
                }
            }
        }
    }
esclient.indices.put_mapping(index=answer_index, doc_type=answer_type, body=answer_mapping)
# 创建完schema以后导入数据
doc = {'id': 7, 'schoolID': '007', 'schoolName': '春晖外国语学校', 'calNum':6.20190624}
esclient.index(index=answer_index ,doc_type=answer_type ,body=doc, id=doc['id'])
esclient.index(index=answer_index ,doc_type=answer_type ,body=doc, id=10)
#----------------------------------------------------

# 删除单条数据
# esclient.delete(index='indexName', doc_type='typeName', id='idValue')
esclient.delete(index='pre', doc_type='imagetable2', id=1)
# 删除索引
esclient.indices.delete(answer_index)

# 更新
# esclient.update(index='indexName', doc_type='typeName', id='idValue', body={_type:{待更新字段}})
new_doc = {'id': 7, 'schoolId': '007', 'schoolName': '更新名字1'}
esclient.update(index=answer_index, id=7, doc_type=answer_type, body={'doc': new_doc}) # 注意body中一定要加_type doc，更新的body中不一定要加入所有字段，只要把要更新的几个字段加入即可

# 查询
### 根据id查找数据
res = esclient.get(index=answer_index, doc_type=answer_type, id=7)
### match：在schoolName中包含关键词的都会被搜索出来（这里的分词工具是ik）
# res = esclient.search(index=answer_index,body={'query':{'match':{'schoolName':'春晖外'}}})
res = esclient.search(index=answer_index,body={'query':{'match':{'schoolName':'春晖学校'}}})
### ids：根据id值
esclient.search(index='baidu_answer',body={'query':{'ids':{'values':'10'}}})
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

```
docker pull stardog/stardog:latest
docker run -v ~/stardog-6.2.2/:/var/opt/stardog -e STARDOG_SERVER_JAVA_ARGS="-Xmx8g -Xms8g -XX:MaxDirectMemorySize=2g" stardog/stardog:latest

```

3.8 容器云k8s

Kubernetes是什么？Kubernetes是一个全新的基于容器技术的分布式架构解决方案，是Google开源的一个容器集群管理系统，Kubernetes简称K8S。Kubernetes 提供了完善的管理工具，这些工具涵盖了开发、部署测试、运维监控在内的各个环节。<br>

Kubernetes特性<br>
    - 自我修复：在节点故障时，重新启动失败的容器，替换和重新部署，保证预期的副本数量；杀死健康检查失败的容器，并且在未准备好之前不会处理用户的请求，确保线上服务不中断。
    - 弹性伸缩：使用命令、UI或者基于CPU使用情况自动快速扩容和缩容应用程序实例，保证应用业务高峰并发时的高可用性；业务低峰时回收资源，以最小成本运行服务。
    - 自动部署和回滚：K8S采用滚动更新策略更新应用，一次更新一个Pod，而不是同时删除所有Pod，如果更新过程中出现问题，将回滚更改，确保升级不影响业务。
    - 服务发现和负载均衡：K8S为多个容器提供一个统一访问入口（内部IP地址和一个DNS名称），并且负载均衡关联的所有容器，使得用户无需考虑容器IP问题。
    - 机密和配置管理：管理机密数据和应用程序配置，而不需要把敏感数据暴露在镜像里，提高敏感数据安全性。并可以将一些常用的配置存储在K8S中，方便应用程序使用。
    - 存储编排：挂载外部存储系统，无论是来自本地存储，公有云，还是网络存储，都作为集群资源的一部分使用，极大提高存储使用灵活性。
    - 批处理：提供一次性任务，定时任务；满足批量数据处理和分析的场景。
    
[Kubernetes 深入学习（一） —— 入门和集群安装部署](https://www.cnblogs.com/chiangchou/p/k8s-1.html#_label0_0)<br>
[Kubernetes(一) 跟着官方文档从零搭建K8S](https://juejin.cn/post/6844903943051411469)<br>
[kubeadm部署k8s集群最全最详细](https://blog.csdn.net/Doudou_Mylove/article/details/103901732)<br>



[RDF入门](https://blog.csdn.net/txlCandy/article/details/50959358)<br>
[OWL语言](https://blog.csdn.net/zycxnanwang/article/details/86557350)<br>

