# neo4j入门

[**1. neo4j_python操作**](#neo4j_python操作)

[**2. neo4j网页版直接操作**](#neo4j网页版直接操作)

[**3. neo4j-spark-connector操作**](#neo4j-spark-connector操作)

[**4. neo4j问题整理**](#neo4j问题整理)


### neo4j_python操作

```python
import numpy as np
import pandas as pd
import py2neo
from py2neo import Graph,Node,Relationship
import neo4j
from neo4j.v1 import GraphDatabase, basic_auth

# py2neo操作
test_graph = Graph(
    #"http://localhost:7474",
    "bolt://localhost:7687"
    username="neo4j",
    password="z123456789"
)

# 创建节点
node1 = Node('Customer', name='John',age=18,phone=2232)
node2 = Node('Customer', name='Lily',age=22,phone=9921)
node3 = Node('Customer', name='Cathy',age=52,phone=7100)
test_graph.create(node1)
test_graph.create(node2)
test_graph.create(node3)

# 创建节点2
arr = np.array([['John','Lily','Ben','Mark'],['189101','234220','019018','330682'],[11,23,56,28]])
df = pd.DataFrame(arr.transpose(),columns=['name','phone_no','age'])
for i, j, k in df.values:
    node1 = Node('Person',name=i,phone_no=j,age=k)
    graph.create(node1)
    
# neo4j.v1操作
driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "z123456789"))
session = driver.session()
# 创建节点3
arr = np.array([['John','Lily','Ben','Mark'],['189101','234220','019018','330682'],[11,23,56,28]])
df = pd.DataFrame(arr.transpose(),columns=['name','phone_no','age'])
#  	 name	phone_no	age
# 0	 John	189101	    11
# 1	 Lily	234220	    23
# 2	 Ben    019018	    56
# 3	 Mark	330682	    28
# dataframe to dict操作
dic = {'events':df.to_dict('records')}
session.run("unwind {events} as event merge (n:Person{name:event.name,phone_no2:event.phone_no,age: event.age})",dic)

# 删除所有节点和边
test_graph.delete_all()
```

### neo4j网页版直接操作

先把jdk改成1.8然后再进入neo4j的文件夹bin中输入neo4j.bat console撑起网页版服务

在http://localhost:7474/browser/用户名neo4j密码z1234...中输入命令进行一些简单的节点，关系等操作

**Neo4j CQL常见的操作有：**

|S.No|CQL命令/条款|用法
|--|--|--
|1|CREATE[创建节点](#创建节点)|创建节点，关系和属性
|2|CREATE[创建关系1](#创建关系1)|创建关系和属性
|3|CREATE[创建关系2](#创建关系2)|创建关系和属性
|4|CREATE[创建关系3](#创建关系3)|创建关系和属性
|5|MATCH[匹配](#匹配)|检索有关系点，关系和属性数据
|6|RETURN[返回](#返回)|返回查询结果
|7|WHERE[哪里](#哪里)|提供条件过滤检索数据
|8|DELETE[删除](#删除)|删除节点和关系
|9|REMOVE[移除](#移除)|删除节点和关系的属性
|10|ORDER BY以..[排序](#排序)|排序检索数据
|11|SET[设置](#设置)|添加或更新标签
|12|[UNWIND](#unwind)|unwind操作
|13|[INDEX](#index)|index添加,删除和查询
|14|[修改graph.db](#修改)|修改备份Neo4j图数据库

**Neo4j CQL常见的函数有：**
|S.No|定制列表功能|用法
|--|--|--
|1|String[字符串](#string)|它们用于使用String字面量(UPPER,LOWER,SUBSTRING,REPLACE)
|2|Aggregation[聚合](#聚合)|对CQL查询结果执行一些聚合操作(COUNT,MAX,MIN,SUM,AVG)
|3|Relationship关系|他们用于获取关系的细节如startnode, endnode等


---
**CQL常见的操作**<br>

 - 创建节点
1)创建节点：
create (e:Customer{id:'1001',name:'Bob',dob:'01/10/1982'})
create (cc:CreditCard{id:'5001',number:'1234567890',cvv:'888',expiredate:'20/17'})

2)导入csv文件进行节点的创建
load csv with headers from "file:///shop.csv" as df
merge(:Shop{name:df.name,cn_name:df.cn_name,age:df.age,sex:df.age})

 - Import data from a CSV file with a custom field delimiter
 比如 load csv with headers from "file:///shop.csv" as df FIELDTERMINATOR '\t'
 - Importing large amounts of data
 比如 USING PERIODIC COMMIT 500
      load csv with headers from "file:///shop.csv" as df

----------

```
 - 创建关系1
创建两个节点之间的关系:
match(e:Customer),(cc:CreditCard)
create (e)-[r:DO_SHOPPING_WITH]->(cc)

创建两个节点之间的关系(加边属性):
match(e:Customer),(cc:CreditCard)
create (e)-[r:DO_SHOPPING_WITH{shopdate:'12/12/2014',price:6666}]->(cc)

 - 创建关系2
根据两个节点之间的相同属性进行连接1：
match(c:Customer),(p:Phone)
where c.phone = p.phone_no
create (c)-[:Call]->(p)

根据两个节点之间的相同属性进行连接2：
match(a:Test),(b:Test22)
where  b.ide in a.name
create (a)-[:sssssssssss]->(b)
这里的a.name是个list

 - 创建关系3
各自创建节点比如shop和phone两个节点，然后导入一个关系的csv文件进行连接
```

**shop.csv**
|name|cn_name|age|sex
|--|--|--|--
|Jack|杰克|22|男
|Lily|丽丽|34|女
|John|约翰|56|男
|Mark|马克|99|男

**phone.csv**
|phone|id_p|
|--|--
|1223|0
|3432|1
|9011|2

**关系.csv**
|name|phone
|--|--
|Jack|1223
|Lily|3432
|John|9011
|Mark|3432

```
cypher关系语句：
load csv with headers from "file:///test.csv" as df
match(a:Shop{name:df.name}),(b:Phone{phone:df.phone})
create (a)-[:Call{phone_id:df.id_p}]->(b)
```
*注：neo4j中不能创建双向或者无向的关系，只能单向*

```
### 匹配

三层关系：
match (n:企业)-[k*1..3]-(m) return n.company_nm

### 返回
match(e:Customer),(cc:CreditCard)
return e.name,cc.cvv

### 哪里
match(n:Customer), (cc:CreditCard)
where n.name = 'Lily' and cc.id = '5001'
create (n)-[r:DO_SHOPPING_WITH{shopdate:'1/1/9999', price:100}]->(cc)

正则使用：
match(n:Person)
where n.name =~ '(?i)^[a-d].*'
return n

### 删除
删除所有的节点和关系
match(n) match(n)-[r]-() delete n,r

删除相关的节点及和这些节点相连的边（一阶）
match(cc:Customer)
*detach* delete cc
或者
match(cc:Customer) match(cc)-[r]-() delete cc,r

删除产品及上下游相连关系和节点，（递归），除3款产品外
match r=(n:Product)-[*]->() where not n.raw_name in ["xx1","xx2","xx3"]  detach delete r

删除孤立节点
match (n) where not (n)–-() delete n

### 移除
可以移除节点的属性
match(n:Customer) where n.name = 'Lily'
remove n.dob

### 设置
可以设置节点的属性(增加或者改写)
match(n:Customer) where n.name = 'Bob'
SET n.id = 1003

对已经存在的点，进行属性添加操作
**--Person:**
create(:Person{cd:'1223',xx:'er'})
create(:Person{cd:'92223',xx:'iir'})
create(:Person{cd:'6783',xx:'rrrr'})
create(:Person{cd:'555903',xx:'ppppppppppr'})
```

**--test.csv:** (注:导入csv的时候会把所有的转成string格式)

|col_one|col_two|col_three
|--|--|--
|555903|"桂勇"|"良"
|92223|"黎明"|"优"
|1223|"皇家"|"优"
|6783|"汽车"|"良"
给Person添加两个属性
load csv with headers from "file:///test.csv" as df 
match(n:Person) where n.cd = df.col_one
set n.nm = df.col_two
set n.credit = df.col_three

```
### 排序
match(n:Customer)
return n.name, n.id, n.dob
order by n.name desc

### UNWIND
创建节点
unwind ['John','Mark','Peter'] as name
create (n:Customer{name:name})

unwind [{id:1,name:'Bob',phone:1232},{id:2,name:'Lily',phone:5421},{id:3,name:'John',phone:9011}] as cust
create (n:Customer{name:cust.name,id:cust.id,phone:cust.phone})

删除节点
unwind [1,2,3] as id
match (n:Customer) where n.id = id
delete n

---

### String
match(e:Customer)
return e.id,upper(e.name) as name, e.dob

### 聚合
count三种写法：
1.  Match (n:people) where  n.age=18   return  count(n)
2.  Match (n:people{age:’18’})  return  count(n)  
3.  Match (n:people)  return  count(n.age=18)

### INDEX
添加 CREATE INDEX ON :Person(name)
删除 DROP INDEX ON :Person(name)
查询 call db.indexes()

### 修改
在neo4j的文件夹conf下面，打开文件neo4j.conf,找到一下位置处

dbms.active_database=graph.db，修改数据库名字，例如graph.db -> graph2.db即可。

```
