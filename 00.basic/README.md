## python实用技巧

[**1. lambda函数**](#lambda函数)

[**2. map函数**](#map函数)

[**3. filter函数**](#filter函数)

[**4. reduce函数**](#reduce函数)

[**5. apply和applymap函数**](#apply函数)

[**6. 装饰器**](#装饰器)

[**7. dict转object**](#dict转object)

[**8. 统计空缺率**](#统计空缺率)

[**9. transform函数**](#transform函数)

[**10. KFold函数**](#kfold函数)

[**11. sys.defaultencoding**](#sys)

[**12. pip install error _NamespacePath**](#pip_error)

[**13. zip(\*xx)用法**](#zip)

[**14. dataframe中某一列字符串长度为10的进行切片**](#切片)

[**15. re模块**](#re模块)

[**16. eval**](#eval)

[**17. global用法**](#global)

[**18. 多进程之pool用法**](#pool)

[**19. 保存模型**](#保存模型)

[**20. enumerate用法**](#enumerate)

---
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
(lambda x : x ** 2)(3)  9
# 或者
f = lambda x : x ** 2
f(3)  9
```
### map函数
```python
arr_str = ["hello", "this"]
arr_num = [3,1,6,10,12]

def f(x):
    return x ** 2
map(lambda x : x ** 2, arr_num) [9,1,36,100,144]
map(f, arr_num) [9,1,36,100,144]
map(len, arr_str) [5,4]
map(lambda x : (x, 1), arr_str)  [('hello', 1), ('this', 1)]
```
```python
# 可以对每个列表对应的元素进行操作，比如加总
f1 = lambda x,y,z:x+y+z
list(map(f1,[1,2,10],[2,3,6],[4,3,5]))
# [7,8,21]
```

### filter函数
```python
filter(lambda x : len(x) >= 5, arr_str) ['hello']
filter(lambda x : x > 5, arr_num) [6,10,12]
[(i.word, 'E') if i.flag =='n' else (i.word, 'P') for i in filter(lambda x: x.flag in ('n', 'v'), a) ]
```

### reduce函数
```python
reduce(lambda x, y : x + y, arr_num) 32
```

### apply函数
你可以把apply()当作是一个map()函数，只不过这个函数是专为Pandas的dataframe和series对象打造的。对初学者来说，你可以把series对象想象成类似NumPy里的数组对象。它是一个一维带索引的数据表结构。<br>
<br>
apply() 函数作用是，将一个函数应用到某个数据表中你指定的一行或一列中的每一个元素上。是不是很方便？特别是当你需要对某一列的所有元素都进行格式化或修改的时候，你就不用再一遍遍地循环啦！<br>
```python
df = pd.DataFrame([[4,9],]*3,columns=['A','B'])
df.apply(np.sqrt)
df.apply(np.sum,axis=0)
df.apply(np.sum,axis=1)
df.apply(lambda x : [1,2], axis=1)
```
 > applymap和apply差不多，不过是全局函数，elementwise，作用于dataframe中的每个元素

### 装饰器

装饰器相当于一个高阶函数，传入函数，返回函数，返回的时候这个函数多了一些功能[(原文链接)](https://mp.weixin.qq.com/s/hsa-kYvL31c1pEtMpkr6bA)
```python
# 无参数的装饰器
def use_logging(func):

    def wrapper():
        logging.warn("%s is running" % func.__name__)
        return func()
    return wrapper

@use_logging
def foo():
    print("i am foo")

foo()

#----------------------------------------------------------
# 带参数的装饰器
def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warn("%s is running" % func.__name__)
            elif level == "info":
                logging.info("%s is running" % func.__name__)
            return func(*args, **kwargs)
        return wrapper

    return decorator

@use_logging(level="warn") # 可以传参数进装饰器
def foo(name, age=None, height=None):
    print("I am %s, age %s, height %s" % (name, age, height))

foo('John',9) [WARNING:root:foo is running]I am John, age 9, height None

#---------------------------------------------------
# 类装饰器
class Foo(object):
    def __init__(self, func):
        self._func = func

    def __call__(self):
        print ('class decorator runing')
        self._func()
        print ('class decorator ending')

@Foo
def bar():
    print ('test bar')

bar() 
输出
class decorator runing
test bar
class decorator ending
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

### 统计空缺率
两种方法统计空缺率：
```python
(1 - np.count_nonzero(np.array(data['col2']))*1.0 / data['col2'].count()) * 100

(1 - data['col2'].apply(lambda x : x != '').sum() * 1.0 / data['col2'].count()) * 100
```

### transform函数
由前面分析可以知道，Fare项在测试数据中缺少一个值，所以需要对该值进行填充。 
我们按照一二三等舱各自的均价来填充： 
下面transform将函数np.mean应用到各个group中。
```python
combined_train_test['Fare'] = combined_train_test[['Fare']].fillna(combined_train_test.groupby('Pclass').transform(np.mean))
```

### kfold函数
新手用cross_val_score比较简单，后期可用KFold更灵活,
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
cross_val_score(forest,X=train_data_features,y=df.Score,scoring=rmse_scoring,cv=3)
```
```python
# Some useful parameters which will come in handy later on
ntrain = titanic_train_data_X.shape[0]
ntest = titanic_test_data_X.shape[0]
SEED = 0 # for reproducibility
NFOLDS = 7 # set folds for out-of-fold prediction
kf = KFold(n_splits = NFOLDS, random_state=SEED, shuffle=False)

def get_out_fold(clf, x_train, y_train, x_test): # 这里需要将dataframe转成array，用x_train.values即可
    oof_train = np.zeros((ntrain,))
    oof_test = np.zeros((ntest,))
    oof_test_skf = np.empty((NFOLDS, ntest))

    for i, (train_index, test_index) in enumerate(kf.split(x_train)):
        x_tr = x_train[train_index]
        y_tr = y_train[train_index]
        x_te = x_train[test_index]

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
```python
# 将一个问题中的网址、邮箱、手机号、身份证、日期、价格提出来

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

### pool
```python
from multiprocessing import Pool
import time

def task(msg):
    print ('hello, %s' % msg)
    time.sleep(1)

if __name__ == '__main__':
    pool = Pool(processes=4)

    for x in range(10):
        pool.apply_async(task, args=(x,))

    pool.close()
    pool.join() # 加入主进程中，不然processes done会提前打印

    print('processes done.')
```
结果是，四个四个差不多同时打印，因为设置了四个进程，四个进程之间的打印顺序是乱的
```python
hello, 1
hello, 3
hello, 0
hello, 2
hello, 5
hello, 4
hello, 6
hello, 7
hello, 8
hello, 9
processes done.
CPU times: user 32.5 ms, sys: 49.9 ms, total: 82.4 ms
Wall time: 3.13 s
```
不加进程，单进程结果如下
```python
for x in range(10):
    task(x)
hello, 0
hello, 1
hello, 2
hello, 3
hello, 4
hello, 5
hello, 6
hello, 7
hello, 8
hello, 9
CPU times: user 45.5 ms, sys: 16.7 ms, total: 62.1 ms
Wall time: 10 s
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

### enumerate
```python
tuples = [(2,3),(7,8),(12,25)]
for step, tp in enumerate(tuples):
    print(step,tp)
# 0 (2, 3)
# 1 (7, 8)
# 2 (12, 25)
```
