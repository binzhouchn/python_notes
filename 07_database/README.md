# 目录

## 1. Mysql/Hive



## 2. Redis

```python
import redis
# 连接redis
redis_conf = redis.Redis(host='xx.xx.xx.xx', port=6379)
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


## 3. pymongo

```python
import pymongo
# 连接
client = pymongo.MongoClient(host='xx.xx.xx.xx', port=27017)
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
