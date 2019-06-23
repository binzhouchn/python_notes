# 目录

## 1. Mysql/Hive(docker version)

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
```
```python
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
```
```
# 起了mysql服务以后，在用docker python去插入数据
# 需要先查看docker mysql的容器ip地址，命令看2.8
# 然后localhost改成mysql容器的ip地址即可，其他一样
```

## 2. Redis(docker version)

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
```

```python
# python连接docker起的redis服务
import redis
# 连接redis
redis_conf = redis.Redis(host='xx.xx.xx.xx', port=6379, password='123456')
# 查看redis中的keys
redis_conf.keys()
# 插入name，value
redis_conf.set(name='name',value='John')
# 插入name，key，value
redis_conf.hset(name='name',key='k1',value='John')
# 批量插入name，key，value
redis_conf.hmset('hash1',{'k1':'v1','k2':'v2'})
# 批量get name
redis_conf.hgetall('hash1')
```
```
# redis可视化工具RDM(已安装)
```

## 3. pymongo(docker version)

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
```
```python
import pymongo
# 连接
client = pymongo.MongoClient(host='xx.xx.xx.xx', port=27017, username='test', password='123456')
# 读取数据库（如果没有的话自动创建）
db = client.tencent_wv
# 读取集合（如果没有的话自动创建）
my_set = db.test_set
# 删除集合 test_set
db.drop_collection('test_set')
# 插入数据和查询数据
my_set.insert_one ({"name":"zhangsan","age":18,'shuze':[3,4,2,6,7,10]})
my_set.find_one({"name":"zhangsan"})
```
```python
# 以插入腾讯词向量为例
from tqdm import tqdm
# 定义一个迭代器
def __reader():
    with open("/opt/common_files/Tencent_AILab_ChineseEmbedding.txt",encoding='utf-8',errors='ignore') as f:
        for idx, line in tqdm(enumerate(f), 'Loading ...'):
            ws = line.strip().split(' ')
            if idx:
                vec = [float(i) for i in ws[1:]]
                if len(vec) != 200:
                    continue
                yield {'word': ws[0], 'vector': vec}rd = __reader()
rd = __reader()
while rd:
    my_set.insert_one(next(rd))
```

## 4. ElasticSearch(docker version)

## 5. neo4j图数据库(docker version)

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


