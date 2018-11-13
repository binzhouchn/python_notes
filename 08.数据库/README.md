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

