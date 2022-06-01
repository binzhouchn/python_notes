## python实用技巧

[**1. lambda函数**](#lambda函数)

[**2. map函数**](#map函数)

[**3. filter函数**](#filter函数)

[**4. reduce函数**](#reduce函数)

[**5. apply和applymap函数、transform/agg**](#apply函数)

[**6. dict转object**](#dict转object)

[**7. KFold函数**](#kfold函数)

[**8. sys.defaultencoding**](#sys)

[**9. pip install error _NamespacePath**](#pip_error)

[**10. zip(\*xx)用法**](#zip)

[**11. dataframe中某一列字符串长度为10的进行切片**](#切片)

[**12. re模块(一些常用的正则轮子)**](#re模块)

[**13. eval**](#eval)

[**14. global用法**](#global)

[**15. 多进程与多线程实现**](#多进程与多线程实现)

[**16. CV的多进程实现**](#cv的多进程实现)

[**17. 保存数据(json)**](#保存数据)

[**18. 保存模型**](#保存模型)

[**19. enumerate用法**](#enumerate)

[**20. label数值化方法**](#label数值化方法)

[**21. 列表推导式中使用if else**](#列表推导式中使用if_else)

[**22. 将nparray或list中的最多的元素选出**](#将numpy_array中的最多的元素选出)

[**23. 函数中传入函数demo**](#函数中传入函数demo)

[**24. getattr**](#getattr)

[**25. df宽变长及一列变多列**](#df宽变长及一列变多列)

[**26. groupby使用**](#groupby使用)

[**27. python画图显示中文**](#python画图及显示中文)

[**28. 给字典按value排序**](#给字典按value排序)

[**29. sorted高级用法**](#sorted高级用法)

[**30. time用法**](#time用法)

[**31. 两层列表展开平铺**](#两层列表展开平铺)

[**32. 读取百度百科词向量**](#读取百度百科词向量)

[**33. logging**](#logging)

[**34. argparse用法**](#argparse用法)

[**35. 包管理**](#包管理)

[**36. 装饰器**](#装饰器)

[**37. 本地用python起http服务**](#本地用python起http服务)

[**38. cache**](#cache)

[**39. 创建文件**](#创建文件)

[**40. 字典转成对象（骚操作）**](#字典转成对象)

[**41. lgb[gpu版本]和xgb[gpu版本]安装**](#boost安装)

[**42. tqdm**](#tqdm)

[**43. joblib Parallel并行**](#joblib_parallel)

[**44. 调试神器 - 丢弃print**](#调试神器)

[**45. 分组计算均值并填充**](#分组计算均值并填充)

[**46. python日期处理**](#python日期处理)

---
<details close>
<summary>点击展开</summary>

```python
%reload_ext autoreload
%autoreload 2
%matplotlib notebook

import sys
sys.path.append('..')
```

### lambda函数
```python
# lambda: 快速定义单行的最小函数，inline的匿名函数
(lambda x : x ** 2)(3)
# 或者
f = lambda x : x ** 2
f(3)
```

### map函数
```python
arr_str = ["hello", "this"]
arr_num = [3,1,6,10,12]

def f(x):
    return x ** 2
map(lambda x : x ** 2, arr_num)
map(f, arr_num)
map(len, arr_str)
map(lambda x : (x, 1), arr_str)
```
```python
# 可以对每个列表对应的元素进行操作，比如加总
f1 = lambda x,y,z:x+y+z
list(map(f1,[1,2,10],[2,3,6],[4,3,5]))
# [7,8,21]
```

### filter函数
```python
arr_str = ['hello','hi','nice']
arr_num = [1,6,10,12]
filter(lambda x : len(x) >= 5, arr_str)
filter(lambda x : x > 5, arr_num) 
[(i.word, 'E') if i.flag =='n' else (i.word, 'P') for i in filter(lambda x: x.flag in ('n', 'v'), a) ]
```

### reduce函数
```python
# 在python3里，reduce函数已经被从全局命名空间里移除了，它现在被放置在functools模块里
from functools import reduce
arr_num = [1,6,7,10]
reduce(lambda x, y : x + y, arr_num)
```

### apply函数

 - apply函数是对行进行操作

你可以把apply()当作是一个map()函数，只不过这个函数是专为Pandas的dataframe和series对象打造的。对初学者来说，你可以把series对象想象成类似NumPy里的数组对象。它是一个一维带索引的数据表结构。<br>
<br>
apply() 函数作用是，将一个函数应用到某个数据表中你指定的一行或一列中的每一个元素上。是不是很方便？特别是当你需要对某一列的所有元素都进行格式化或修改的时候，你就不用再一遍遍地循环啦！<br>
```python
df = pd.DataFrame([[4,9],]*3,columns=['A','B'])
df.apply(np.sqrt)
df.apply(np.sum,axis=0)
df.apply(np.sum,axis=1)
df.apply(lambda x : [1,2], axis=1)
df.apply(lambda x : x.split()[0])
```
 > applymap和apply差不多，不过是全局函数，elementwise，作用于dataframe中的每个元素

 - transform/agg是对一列进行操作

由前面分析可以知道，Fare项在测试数据中缺少一个值，所以需要对该值进行填充。 
我们按照一二三等舱各自的均价来填充： 
下面transform将函数np.mean应用到各个group中。
```python
combined_train_test['Fare'] = combined_train_test[['Fare']].fillna(combined_train_test.groupby('Pclass').transform(np.mean))
```

### dict转object
```python
import json
# json格式的str
s = '{"name":{"0":"John","1":"Lily"},"phone_no":{"0":"189101","1":"234220"},"age":{"0":"11","1":"23"}}' 
# load成dict
dic = json.loads(s)
dic
# {"name":{"0":"John","1":"Lily"},"phone_no":{"0":"189101","1":"234220"},"age":{"0":"11","1":"23"}}
# 不能使用dic.name, dic.age 只能dic['name'], dic['age']
class p:
    def __init__(self, d=None):
        self.__dict__ = d
p1 = p(dic)
# 这个时候就可以用p1.name, p1.age了

# 更详细一点
import six
import pprint
# 现在有个字典
conf = {'base':{'good','medium','bad'},'age':'24'}
# conf.age是不行的
定义一个class：
class p:
    def __init__(self, d=None):
        self.__dict__ = d
    def keys(self):
        return self.__dict__.keys()
    def items(self):
        return six.iteritems(self.__dict__)
    def __repr__(self):
        return pprint.pformat(self.__dict__) # 将dict转成字符串
p1 = p(conf)
这个时候就可以p1.base和p1.age
p1这个实例拥有的属性有：
p.__doc__
p.__init__
p.__module__
p.__repr__
p.age * age和base这两个是字典加载进来以后多出来的属性
p.base *
p.items
p.keys
```

### kfold函数
新手用cross_val_score比较简单，后期可用KFold更灵活,
```python
skf = StratifiedKFold(n_splits=5,shuffle=True)
for train_idx, val_idx in skf.split(X,y):
    pass
train_idx
val_idx
```
```python
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold
forest = RandomForestClassifier(n_estimators = 120,max_depth=5, random_state=42)
cross_val_score(forest,X=train_data_features,y=df.Score,scoring='neg_mean_squared_error',cv=3)
# 这里的scoring可以自己写，比如我想用RMSE则
from sklearn.metrics import scorer
def ff(y,y_pred):
    rmse = np.sqrt(sum((y-y_pred)**2)/len(y))
    return rmse
rmse_scoring = scorer.make_scorer(ff)
cross_val_score(forest,X=train_data_features,y=df.Score,scoring=rmse_scoring,cv=5)
```
```python
# Some useful parameters which will come in handy later on
ntrain = titanic_train_data_X.shape[0]
ntest = titanic_test_data_X.shape[0]
SEED = 42 # for reproducibility
NFOLDS = 5 # set folds for out-of-fold prediction
kf = KFold(n_splits = NFOLDS, random_state=SEED, shuffle=True)

def get_out_fold(clf, x_train, y_train, x_test): # 这里需要将dataframe转成array，用x_train.values即可
    oof_train = np.zeros((ntrain,))
    oof_test = np.zeros((ntest,))
    oof_test_skf = np.empty((NFOLDS, ntest))

    for i, (train_index, test_index) in enumerate(kf.split(x_train)):
        x_tr = x_train.loc[train_index]
        y_tr = y_train.loc[train_index]
        x_te = x_train.loc[test_index]

        clf.fit(x_tr, y_tr)

        oof_train[test_index] = clf.predict(x_te)
        oof_test_skf[i, :] = clf.predict(x_test)

    oof_test[:] = oof_test_skf.mean(axis=0)
    return oof_train.reshape(-1, 1), oof_test.reshape(-1, 1)
```

### sys
```python
import sys 
reload(sys) 
sys.setdefaultencoding('utf-8') 
#注意：使用此方式，有极大的可能导致print函数无法打印数据！

#改进方式如下：
import sys #这里只是一个对sys的引用，只能reload才能进行重新加载
stdi,stdo,stde=sys.stdin,sys.stdout,sys.stderr 
reload(sys) #通过import引用进来时,setdefaultencoding函数在被系统调用后被删除了，所以必须reload一次
sys.stdin,sys.stdout,sys.stderr=stdi,stdo,stde 
sys.setdefaultencoding('utf-8')
```

### pip_error

使用pip时出现错误：
AttributeError: '_NamespacePath' object has no attribute 'sort'

解决方法：<br>
1. 关于Anaconda3报错 AttributeError: '_NamespacePath' object has no attribute 'sort'  ，先参考下面这篇博客：<br>
http://www.cnblogs.com/newP/p/7149155.html<br>
按照文中的做法是可以解决conda报错的，总结一下就是：一，把文件夹 D:\ProgramData\Anaconda3\Lib\site-packages\conda\_vendor\auxlib 中的 path.py 中，“except ImportError: ”修改为“except Exception:“；二、找到D:\ProgramData\Anaconda3\lib\site-packages\setuptools-27.2.0-py3.6.egg，删除（不放心的话，剪切到别的地方）

2.然而pip报错的问题还没解决。首先要安装setuptools模块，下载地址是：<br>
https://pypi.python.org/pypi/setuptools#files<br>
下载setuptools-36.5.0.zip解压，命令窗口进入到文件夹然后 python setup.py install

3.安装好setuptools模块之后应该能用easy_install了，我们要借助它来重新安装pip。命令窗口输入命令：easy_install pip

### zip
zip基本用法<br>
```python
a = [1,2,3]
b = [4,5,6]
for i,j in zip(a,b):
    print(i,j)
# 1 4
# 2 5
# 3 6
```

```python
s = '彩符和大汶口文化陶尊符号是第三阶段的语段文字'
print(synonyms.seg(s))
# (['彩符', '和', '大汶口', '文化', '陶尊', '符号', '是', '第三阶段', '的', '语段', '文字'], ['n', 'c', 'ns', 'n', 'nr', 'n', 'v', 't', 'uj', 'n', 'n'])
[x for x in zip(*synonyms.seg(s))]
# [('彩符', 'n'),
  ('和', 'c'),
  ('大汶口', 'ns'),
  ('文化', 'n'),
  ('陶尊', 'nr'),
  ('符号', 'n'),
  ('是', 'v'),
  ('第三阶段', 't'),
  ('的', 'uj'),
  ('语段', 'n'),
  ('文字', 'n')]
```
### 切片
```python
data.msg_from = data.msg_from.astype(str)
data[data.msg_from.apply(len)==10]
```

### re模块

[常用正则表达式速查手册，Python文本处理必备](https://mp.weixin.qq.com/s/ySsgcrSnkguO2c8D-SQNxw)<br>
[regexlearn](https://github.com/aykutkardas/regexlearn.com)<br>

```python
# 1. 将一个问题中的网址、邮箱、手机号、身份证、日期、价格提出来

# 日期 注：这里的{1,4}指的是匹配1到4位，问号指的是0个或1个
DATE_REG1 = "(?:[一二三四五六七八九零十0-9]{1,4}年[一二三四五六七八九零十0-9]{1,2}月[一二三四五六七八九零十0-9]{1,2}[日|号|天|分]?)|\
(?:[一二三四五六七八九零十0-9]+年[一二三四五六七八九零十0-9]+月)|\
(?:[一二三四五六七八九零十0-9]{1,2}月[一二三四五六七八九零十0-9]{1,2}[号|日|天]?)|\
(?:[一二三四五六七八九零十0-9]+年)|\
(?:[一二三四五六七八九零十0-9]+月)|\
(?:[一二三四五六七八九零十0-9]{1,3}[号|日|天])|\
(?:[一二三四五六七八九零十0-9]+小时[一二三四五六七八九零十0-9]+分钟)|\
(?:[一二三四五六七八九零十0-9]+小时)|\
(?:[一二三四五六七八九零十0-9]+分钟)\
"

# 网址
URL_REG = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*,]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
# 手机
PHONE_REG = "[+](?:86)[-\s+]*?1[3-8][0-9]{9}"
# 邮箱
MAIL_REG = "[0-9a-zA-Z_]{0,39}@(?:[A-Za-z0-9]+\.)+[A-Za-z]+"
# 身份证
IDCARD_REG = "\d{18}|\d{17}[Xx]"

# 价格
MONEY_REG1 = "(?:\d+[\.\d+]*万*亿*美*港*元/桶)|\
(?:\d+[\.\d+]*万*亿*美*港*元/吨)|\
(?:\d+[\.\d+]*万*亿*美*港*元/升)|\
(?:\d+[\.\d+]*万*亿*美*港*元/吨)|\
(?:\d+[\.\d+]*万*亿*美*港*元/赛季)|\
(?:\d+[\.\d+]*万*亿*美*港*平方米)|\
(?:\d+[\.\d+]*万*亿*美*港*平方千米)|\
(?:(?:[\d]{1,3},)*(?:[\d]{3})[万亿]*[美港]*元)|\
(?:\d+[\.\d+]*万*亿*美*港*[股|笔|户|辆|倍|桶|吨|升|个|手|点|元|亿|万])"

MONEY_REG2 = "([一二三四五六七八九零十百千万亿|\d|.]+[万|元|块|毛][一二三四五六七八九零十百千万亿|\d|.]*)+"

## add date reg
DATE_REG2 = "(?:[\d]*[-:\.]*\d+[-:\.点]\d+分)|(?:[\d+-]*\d+月份)|(?:\d+[-:\.]\d+[-:\.]\d+)"
# HYPER_REG 2017-09-20
HYPER_REG = "[0-9a-zA-Z]+[-:][0-9a-zA-Z]+[%]*"

# 2. 具体的正则匹配问题

## 2.1 以数字开头后面只能接文字，而且数字后面接的文字不能是【小时、种】
s = '22基本日常生活活动：指食物摄取、大小便始末、穿脱衣服、起居、步行、入浴。'
re.findall(r'^\d+(?![\d*小时*]|[\d*种*])[\u4e00-\u9fa5]+', s)

# 匹配只留下中文、英文和数字
re.sub(r'[^\u4E00-\u9FA5\s0-9a-zA-Z]+', '', s)
```

### eval
```python
eval("['一','二','三']")
输出 ['一','二','三']
eval("{'a':1,'b':2}")
输出 {'a':1,'b':2}
```

### global
```python
a = None

def f1():
    a = 10
    
def f2():
    global a
    a = 10
f1()
print(a)
f2()
print(a)
```
运行完f1()后，a还是None；运行完f2()后，a变成了10。一般规范global变量用大写

### 多进程与多线程实现

```python
# 多进程实现举例
from multiprocessing import Pool
import os
import time

def long_time_task(a, b):
    print('Run task %s (%s)...' % (a, os.getpid()))
    start = time.time()
    time.sleep(1)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (a, (end - start)))
    return str(a) + '__pool__' + str(b)


if __name__ == '__main__':

    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    res = []
    for i in range(10):
        res.append(p.apply_async(long_time_task, args=(i, i+1)))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
    # 拿到子进程返回的结果
    for i in res:
        print('xxx', i.get())
```
```python
# 多线程实现举例
def func1(p1, p2, p3):
    pass
def func2(p1, p2):
    pass
from concurrent.futures import ThreadPoolExecutor, wait
executor = ThreadPoolExecutor(max_workers=4)
tasks = []
tasks.append(executor.submit(func1, param1, param2, param3))
tasks.append(executor.submit(func2, param1, param2))
wait(tasks, return_when='ALL_COMPLETED')
res1, res2 = (x.result() for x in tasks)
```

### cv的多进程实现

```python
from multiprocessing import Manager, Process
n = 5
kf = KFold(n_splits=n, shuffle=False)
mg = Manager()
mg_list = mg.list()
p_proc = []

def lr_pred(i,tr,va,mg_list):
    print('%s stack:%d/%d'%(str(datetime.now()),i+1,n))
    clf = LogisticRegression(C=3)
    clf.fit(X[tr],y[tr])
    y_pred_va = clf.predict_proba(X[va])
    print('va acc:',myAcc(y[va], y_pred_va))
    mg_list.append((va, y_pred_va))
#     return mg_list # 可以不加

print('main line')
for i,(tr,va) in tqdm_notebook(enumerate(kf.split(X))):
    p = Process(target=lr_pred, args=(i,tr,va,mg_list,))
    p.start()
    p_proc.append(p)
[p.join() for p in p_proc]
# 最后把mg_list中的元组数据拿出来即可
```

### 保存数据

```python
# 这里medical是mongodb的一个集合
import json
with open('../data/medical.json','w',encoding='utf-8') as fp:
    for i in medical.find():
        i['_id'] = i.get('_id').__str__() # 把bson的ObjectId转成str
        json.dump(i,fp, ensure_ascii=False)
        fp.write('\n')
fp.close()

# 使用pickle(保存)
data = (x_train, y_train, x_test)
f_data = open('./data_doc2vec_25.pkl', 'wb')
pickle.dump(data, f_data)
f_data.close()
# 使用pickle(读取)
f = open('./data_doc2vec_25.pkl', 'rb')
x_train, _, x_test = pickle.load(f)
f.close()

```

### 保存模型

1. 使用 pickle 保存
```python
import pickle #pickle模块

#保存Model(注:save文件夹要预先建立，否则会报错)
with open('save/clf.pickle', 'wb') as f:
    pickle.dump(clf, f)

#读取Model
with open('save/clf.pickle', 'rb') as f:
    clf2 = pickle.load(f)
    #测试读取后的Model
    print(clf2.predict(X[0:1]))
```
2. 使用joblib保存
```python
from sklearn.externals import joblib #jbolib模块

#保存Model(注:save文件夹要预先建立，否则会报错)
joblib.dump(clf, 'save/clf.pkl')

#读取Model
clf3 = joblib.load('save/clf.pkl')

#测试读取后的Model
print(clf3.predict(X[0:1]))
```

3. 可以使用dataframe自带的to_pickle函数，可以把大的文件存成多个
```python
import os
from glob import glob

def mkdir_p(path):
    try:
        os.stat(path)
    except:
        os.mkdir(path)
    
def to_pickles(df, path, split_size=3, inplace=True):
    """
    path = '../output/mydf'
    
    wirte '../output/mydf/0.p'
          '../output/mydf/1.p'
          '../output/mydf/2.p'
    
    """
    if inplace==True:
        df.reset_index(drop=True, inplace=True)
    else:
        df = df.reset_index(drop=True)
    gc.collect()
    mkdir_p(path)
    
    kf = KFold(n_splits=split_size)
    for i, (train_index, val_index) in enumerate(tqdm(kf.split(df))):
        df.iloc[val_index].to_pickle(f'{path}/{i:03d}.p')
    return

def read_pickles(path, col=None):
    if col is None:
        df = pd.concat([pd.read_pickle(f) for f in tqdm(sorted(glob(path+'/*')))])
    else:
        df = pd.concat([pd.read_pickle(f)[col] for f in tqdm(sorted(glob(path+'/*')))])
    return df
```

### enumerate

```python
tuples = [(2,3),(7,8),(12,25)]
for step, tp in enumerate(tuples):
    print(step,tp)
# 0 (2, 3)
# 1 (7, 8)
# 2 (12, 25)
```

### label数值化方法

方法一<br>
```python
# 比如10个类别转成1到10
from sklearn.preprocessing import LabelEncoder
data['label'] = LabelEncoder().fit_transform(data.categ_id)
```
方法二<br>
```python
# 比如10个类别转成onehot形式
import pandas as pd
pd.get_dummies(data.categ_id)
```

方法三<br
```python
# 比如4个类别转成onehot形式
from sklearn import preprocessing
le = preprocessing.MultiLabelBinarizer()    #获取一个MultiLabelBinarizer
data = [['a','b'],['a'],['b','c'],['d']]
le = le.fit(data)      
res = le.transform(data)
#array([[1, 1, 0, 0],
#       [1, 0, 0, 0],
#       [0, 1, 1, 0],
#       [0, 0, 0, 1]])
```


### 列表推导式中使用if_else

两种方式：<br>
1. [x for x in data if condition] <br>
2. [exp1 if condition else exp2 for x in data]

### 将numpy_array中的最多的元素选出

将numpy array中的最多的元素选出，如果一样则取最小的那个
```python
arr = np.array([2,2,2,4,5])
np.bincount(arr).argmax()
# output: 2
arr = np.array([1,2,1,4,2,8])
np.bincount(arr).argmax()
# output: 1
```

将list中最多的元素选出，如果一样则取最小的那个
```python
# 方法一
arr = [2,2,2,4,5]
max(set(arr),key=arr.count)
# 方法二
from collections import Counter
Counter(arr).most_common(1)[0][0]
```

### 函数中传入函数demo

```python
# time_function把时间包装了一下给其他的函数
def time_function(f, *args):
    """
    Call a function f with args and return the time (in seconds) that it took to execute.
    """
    import time
    tic = time.time()
    f(*args)
    toc = time.time()
    return toc - tic

two_loop_time = time_function(classifier.compute_distances_two_loops, X_test)
print('Two loop version took %f seconds' % two_loop_time)

one_loop_time = time_function(classifier.compute_distances_one_loop, X_test)
print('One loop version took %f seconds' % one_loop_time)

no_loop_time = time_function(classifier.compute_distances_no_loops, X_test)
print('No loop version took %f seconds' % no_loop_time)
```

### getattr

```python
class A(object):
    def __init__(self):
        pass
    def xx(self,x):
        print('get xx func',x)
a = A()
getattr(a,'xx')(23213) ### 等同于a.xx(23213)
#out[]: get xx func 23213
```

### df宽变长及一列变多列

(1) df宽变长<br>
```python
def explode(df, col, pat=None, drop_col=True):
    """
    :param df:
    :param col: col name
    :param pat: String or regular expression to split on. If None, splits on whitespace
    :param drop_col: drop col is Yes or No
    :return: hive explode
    """
    data = df.copy()
    data_temp = data[col].str.split(pat=pat, expand=True).stack().reset_index(level=1, drop=True).rename(col+'_explode')
    if drop_col:
        data.drop(col, 1, inplace=True)
    return data.join(data_temp)
    
df = pd.DataFrame([[1, 'a b c'], 
                   [2, 'a b'],
                   [3, np.nan]], columns=['id', 'col'])

explode(df, 'col', pat=' ')
```
```python
#	id	col_explode
#0	1	a
#0	1	b
#0	1	c
#1	2	a
#1	2	b
#2 	3	NaN
```
(2) 一列变多列
```python
df.col.str.split(' ', expand=True)
```
```python
#	0	1	2
#0	a	b	c
#1	a	b	None
#2	NaN	NaN	NaN
```

### groupby使用

根据df的personid进行groupby，统计一下用户消费consume这一列特征的相关聚合情况；
比如count, max, kurt

```python
gr = df.groupby('personid')['consume']
df_aggr = gr.agg([('_count','count'),('_max',np.max),('_kurt',pd.Series.kurt)]).reset_index()

# 多个特征聚合统计值拼接
df = df.merge(df_aggr, how='left', on='personid').fillna(0)
```

### python画图显示中文

```python
## 显示中文解决方法
# 解决方法一
import matplotlib as mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['font.serif'] = ['SimHei']

# 如果方法一解决不了
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 解决中文显示问题-设置字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 如果方法二解决不了
import matplotlib
zhfont = matplotlib.font_manager.FontProperties(fname='../simsun.ttc')
plt.title("职业分布情况",fontproperties=zhfont)
plt.xlabel("用户职业",fontproperties=zhfont)
plt.ylabel("逾期用户比例",fontproperties=zhfont)
#或者
import seaborn as sns
p = sns.color_palette()
sns.set_style("darkgrid",{"font.sans-serif":['simhei', 'Arial']})
fig = plt.figure(figsize=(20, 20))
ax1 = fig.add_subplot(3, 2, 1) # 总共3行2列6张，这是第一张图
ax1=sns.barplot(职业分布.index, 职业分布.逾期/职业分布.总数, alpha=0.8, color=p[0], label='train')
ax1.legend()
ax1.set_title(u'职业分布情况',fontproperties=zhfont) 
ax1.set_xlabel(u'用户职业',fontproperties=zhfont)
ax1.set_ylabel(u'逾期用户比例',fontproperties=zhfont)

# 杰哥的方法，这个比较好
from pathlib import Path
from matplotlib.font_manager import _rebuild
def chinese_setting(url=None):
    """
    :param url: SimHei字体下载链接
    :return:
    """
    print('开始设置中文...')
    matplotlibrc_path = Path(matplotlib.matplotlib_fname())
    ttf_path = matplotlibrc_path.parent.__str__() + '/fonts/ttf'
    ttf_url = 'https://raw.githubusercontent.com/Jie-Yuan/Jie-Yuan.github.io/master/SimHei.ttf' if url is None else url
    if list(Path(ttf_path).glob('SimHei.ttf')):
        pass
    else:
        print('下载字体...')
        os.popen("cd %s && wget %s" % (ttf_path, ttf_url))

    print('设置字体...')
    setting1 = 'font.family: sans-serif'
    setting2 = 'font.sans-serif: SimHei, Bitstream Vera Sans, Lucida Grande, Verdana, Geneva, Lucid, Arial, Helvetica, Avant Garde, sans-serif'
    setting3 = 'axes.unicode_minus: False'
    os.system('echo > %s' % matplotlibrc_path)
    os.system('echo %s >> %s' % (setting1, matplotlibrc_path))
    os.system('echo %s >> %s' % (setting2, matplotlibrc_path))
    os.system('echo %s >> %s' % (setting3, matplotlibrc_path))
    _rebuild()
    print('请重启kernel测试...')
chinese_setting()
```


```bash
# Graphviz 中文乱码
centos5.x下 
yum install fonts-chinese 
centos6.x或7.x下 
yum install cjkuni-ukai-fonts

fc-cache -f -v 刷新字体缓存
```

### 给字典按value排序

```python
model = xgb.train()
feature_score = model.get_fscore()
#{'avg_user_date_datereceived_gap': 1207,
# 'buy_total': 2391,
# 'buy_use_coupon': 557,
# 'buy_use_coupon_rate': 1240,
# 'count_merchant': 1475,
# 'coupon_rate': 5615,
# ...
# }
```

方法一：
```python
sorted(feature_score.items(), key=lambda x:x[1],reverse=True)
```

方法二：
```python
df = pd.DataFrame([(key, value) for key,value in feature_score.items()],columns=['key','value'])
df.sort_values(by='value',ascending=False,inplace=True)
```

### sorted高级用法

用法一：<br>
这里，列表里面的每一个元素都为二维元组，key参数传入了一个lambda函数表达式，其x就代表列表里的每一个元素，然后分别利用索引返回元素内的第一个和第二个元素，这就代表了sorted()函数利用哪一个元素进行排列。而reverse参数就如同上面讲的一样，起到逆排的作用。默认情况下，reverse参数为False。<br>
```python
l=[('a', 1), ('b', 2), ('c', 6), ('d', 4), ('e', 3)]
sorted(l, key=lambda x:x[0], reverse=True)
# Out[40]: [('e', 3), ('d', 4), ('c', 6), ('b', 2), ('a', 1)]
sorted(l, key=lambda x:x[1], reverse=True)
# Out[42]: [('c', 6), ('d', 4), ('e', 3), ('b', 2), ('a', 1)]
```

用法二：<br>
```python
# 调整数组顺序使奇数位于偶数前面，奇偶相对顺序不变
# 按照某个键值（即索引）排序，这里相当于对0和1进行排序
a = [3,2,1,5,8,4,9]
sorted(a, key=lambda c:c%2, reverse=True)
# key=a%2得到索引[1,0,1,1,0,0,1] 相当于给a打上索引标签[(1, 3), (0, 2), (1, 1), (1, 5), (0, 8), (0, 4), (1, 9)]
# 然后根据0和1的索引排序 得到[0,0,0,1,1,1,1]对应的数[2,8,4,3,1,5,9]，
# 最后reverse的时候两块索引整体交换位置[1,1,1,1,0,0,0] 对应的数为[3, 1, 5, 9, 2, 8, 4] 这一系列过程数相对位置不变
```

用法三：<br>
需要注意的是，在python3以后，sort方法和sorted函数中的cmp参数被取消，此时如果还需要使用自定义的比较函数，那么可以使用cmp_to_key函数(在functools中)<br>
```python
from functools import cmp_to_key
arr = [3,5,6,4,2,8,1]
def comp(x, y):
    if x < y:
        return 1
    elif x > y:
        return -1
    else:
        return 0
        
sorted(arr, key=cmp_to_key(comp))
# Out[10]: [8,6,5,4,3,2,1]
```

用法三（衍生）：<br>
输入一个正整数数组，把数组里所有数字拼接起来排成一个数，打印能拼接出的所有数字中最小的一个。例如输入数组{3，32，321}，则打印出这三个数字能排成的最小数字为321323。<br>
```python
# 把数组排成最小的数
from functools import cmp_to_key
arr = [3, 32, 321]
arr = map(str, arr) # or [str(x) for x in arr]
ll = sorted(arr, key=cmp_to_key(lambda x,y:int(x+y)-int(y+x)))
print(int(''.join(ll)))
# Out[3]: 321323
```

### time用法

```python
import time
s = 'Jun-96'
time.mktime(time.strptime(s,'%b-%y'))
# strptime函数是将字符串按照后面的格式转换成时间元组类型；mktime函数则是将时间元组转换成时间戳
```

### 两层列表展开平铺

性能最好的两个方法

1. 方法一
```python
C = [[1,2],[3,4,5],[7]]
[a for b in C for a in b]
```

2. 方法二
```python
from itertools import chain
list(chain(*input))
# list(chain.from_iterable(input))
```

3. 方法三
```python
import functools
import operator
#使用functools內建模块 
def functools_reduce(a): 
    return functools.reduce(operator.concat, a) 
```

### 读取百度百科词向量

```python
from bz2 import BZ2File as b2f
import tarfile
path = 'data/sgns.target.word-ngram.1-2.dynwin5.thr10.neg5.dim300.iter5.bz2'
fp = b2f(path)
lines = fp.readlines()

def get_baike_wv(lines):
    d_ = {}
    for line in lines:
        tmp = line.decode('utf-8').split(' ')
        d_[tmp[0]] = [float(x) for x in tmp[1:-1]]
    return d_
baike_wv_dict = get_baike_wv(lines)
```

### logging

```python
import logging
#logger
def get_logger():
    FORMAT = '[%(levelname)s]%(asctime)s:%(name)s:%(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger('main')
    logger.setLevel(logging.DEBUG)
    return logger
    
logger = get_logger()

logger.warning('Input data')
logger.info('cat treatment')
```

### argparse用法

argparse 是在 Python 中处理命令行参数的一种标准方式。

[arg_test.py](arg_test.py)
```
# 在shell中输入 
python arg_test.py --train_path aa --dev_path bb
# 打印结果如下
Namespace(dev_path='bb',log_level='info',train_path='aa')
aa
bb
done.
```

### 包管理

一个包里有三个模块，mod1.py, mod2.py, mod3.py，但使用from demopack import *导入模块时，如何保证只有mod1、mod3被导入了。<br>
答案:增加init.py文件，并在文件中增加：
```python
__all__ = ['mod1','mod3']
```

### 装饰器

[装饰器参考网址（还可以）](https://blog.csdn.net/qq_41853758/article/details/82853811)<br>
```python
#其中一种举例 装饰带有返回值的函数
def function(func): #定义了一个闭包
	def func_in(*args,**kwargs): #闭包内的函数，因为装饰器运行的实则是闭包内的函数，所以这里将需要有形参用来接收原函数的参数。
		print('这里是需要装饰的内容，就是需要添加的内容')
		num = func(*args,**kwargs) #调用实参函数，并传入一致的实参，并且用变量来接收原函数的返回值，
		return num #将接受到的返回值再次返回到新的test()函数中。
	return func_in
@function
def test(a,b): #定义一个函数
	return a+b #返回实参的和
print(test(3, 4))
# 这里是需要装饰的内容，就是需要添加的内容
# 7
```

### 本地用python起http服务

```shell
python -m http.server 7777
```

### cache

[好用的cache包](https://github.com/tkem/cachetools)<br>
```python
from cachetools import cached, LRUCache, TTLCache

# speed up calculating Fibonacci numbers with dynamic programming
@cached(cache={})
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

# cache least recently used Python Enhancement Proposals
@cached(cache=LRUCache(maxsize=32))
def get_pep(num):
    url = 'http://www.python.org/dev/peps/pep-%04d/' % num
    with urllib.request.urlopen(url) as s:
        return s.read()

# cache weather data for no longer than ten minutes
@cached(cache=TTLCache(maxsize=1024, ttl=600))
def get_weather(place):
    return owm.weather_at_place(place).get_weather()
```
加在函数之前，主要cache输入和返回的值，下次输入同样的值就会1ms内返回，可以设置cache策略和数据过期时间ttl

### 创建文件

如果文件不存在则创建
```python
from pathlib import Path
Path(OUT_DIR).mkdir(exist_ok=True)
```

### 字典转成对象

```python
class MyDict(dict):
    __setattr__ = dict.__setitem__
    __getattr__ = dict.__getitem__


def dict_to_object(_d):
    if not isinstance(_d, dict):
        return _d
    inst = MyDict()
    for k, v in _d.items():
        inst[k] = dict_to_object(v)  # 解决嵌套字典问题
    return inst
```

### boost安装

```shell
sudo apt-get install libboost-all-dev  
sudo apt install ocl-icd-opencl-dev
sudo apt install cmake(可以去https://cmake.org/files下载比如cmake-3.14.0.tar.gz然后执行./bootstrap然后make然后make install)
```

lgb gpu版安装<br>
```shell
pip install --upgrade pip
pip install lightgbm --install-option=--gpu
```
xgb gpu版安装<br>
```shell
git clone --recursive https://github.com/dmlc/xgboost
cd xgboost
mkdir build
cd build
cmake .. -DUSE_CUDA=ON
make(或者make -j4可能或报错)

cd  ..
cd python-package
python setup.py install
```

### tqdm

[当Pytorch遇上tqdm](https://blog.csdn.net/dreaming_coder/article/details/113486645)<br>
```python
for epoch in range(epoch):
        with tqdm(
                iterable=train_loader,
                bar_format='{desc} {n_fmt:>4s}/{total_fmt:<4s} {percentage:3.0f}%|{bar}| {postfix}',
        ) as t:
            start_time = datetime.now()
            loss_list = []
            for batch, data in enumerate(train_loader):
                t.set_description_str(f"\33[36m【Epoch {epoch + 1:04d}】")
                # 训练代码
                time.sleep(1)
                # 计算当前损失
                loss = random()
                loss_list.append(loss)
                cur_time = datetime.now()
                delta_time = cur_time - start_time
                t.set_postfix_str(f"train_loss={sum(loss_list) / len(loss_list):.6f}， 执行时长：{delta_time}\33[0m")
                t.update()
```

### joblib_parallel


```python
#Parallel for loop 此方法可用于多个文件数据并行读取
from joblib import Parallel, delayed
from math import sqrt
def ff(num):
    return [sqrt(n ** 3) for n in range(num)]
#不使用并行 7.5s
res = []
for i in range(10,7000):
    res.append(ff(i))
#使用并行 2.75s
res = Parallel(n_jobs = -1, verbose = 1)(delayed(ff)(i) for i in range(10,7000))
```

### 调试神器

```python
#pip install pysnooper
import os
os.environ['pysnooper'] = '1' # 开关

from pysnooper import snoop
#如果为0，则重新定义snoop然后这个修饰啥都不干
if os.environ['pysnooper'] == '0':
    import wrapt
    def snoop(*args, **kwargs):
        @wrapt.decorator
        def wrapper(wrapped, instance, args, kwargs):
            return wrapped(*args, **kwargs)
        return wrapper
```

### 分组计算均值并填充

```python
def pad_mean_by_group(df, gp_col='stock_id'):
    # 只留下需要处理的列
    cols = [col for col in df.columns if col not in["stock_id", "time_id", "target", "row_id"]]
    # 查询nan的列
    df_na = df[cols].isna()
    # 根据分组计算平均值
    df_mean = df.groupby(gp_col)[cols].mean()

    # 依次处理每一列
    for col in cols:
        na_series = df_na[col]
        names = list(df.loc[na_series,gp_col])     

        t = df_mean.loc[names,col]
        t.index = df.loc[na_series,col].index

        # 相同的index进行赋值     
        df.loc[na_series,col] = t
    return df
train_pca = pad_mean_by_group(train_pca)
```

### python日期处理

[80个例子，彻底掌握Python日期时间处理](https://mp.weixin.qq.com/s/2bJUZBfWS_8ULGrb9tRpmw)<br>




</details>