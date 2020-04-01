## 目录

[**1. super函数使用基础**](#super函数使用基础)

[**2. super函数使用 以LR为例**](#super函数使用_以lr为例)

[**3. 装饰器@**](#装饰器)

[**4. 装饰器@property**](#装饰器property)

[**5. python单例模式**](#单例模式)

[**6. python deprecated warning**](#deprecationwarning)

[**7. 定制类**](#定制类)

[**8. 网络编程**](#网络编程)

[**各种模式待补充 看设计之禅(第2版)**](#设计模式)

---

### super函数使用基础

实际上，大家对于在Python中如何正确使用super()函数普遍知之甚少。你有时候会看到像下面这样直接调用父类的一个方法：
```python
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
```
尽管对于大部分代码而言这么做没什么问题，但是在更复杂的涉及到多继承的代码中就有可能导致很奇怪的问题发生。比如，考虑如下的情况：
```python
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        Base.__init__(self)
        print('A.__init__')
class B(Base):
    def __init__(self):
        Base.__init__(self)
        print('B.__init__')
class C(A,B):
    def __init__(self):
        A.__init__(self)
        B.__init__(self)
        print('C.__init__')
```
如果你运行这段代码就会发现Base.init()被调用两次，如下所示：
```python
>>> c = C()
Base.__init__
A.__init__
Base.__init__
B.__init__
C.__init__
>>>
```
可能两次调用Base.init()没什么坏处，但有时候却不是。另一方面，假设你在代码中换成使用super()，结果就很完美了：
```python
class Base:
    def __init__(self):
        print('Base.__init__')
class A(Base):
    def __init__(self):
        super().__init__()
        print('A.__init__')
class B(Base):
    def __init__(self):
        super().__init__()
        print('B.__init__')
class C(A,B):
    def __init__(self):
        super().__init__()  # Only one call to super() here
        print('C.__init__')
```
运行这个新版本后，你会发现每个init()方法只会被调用一次了：
```python
>>> c = C()
Base.__init__
B.__init__
A.__init__
C.__init__
>>>
```
记一下这个：
```python
class Base(object):
    def __init__(self,a=1,b=11):
        self.a = a
        self.b = b
# 绑定（推荐）
class B(Base):
    def __init__(self, a, b, c):
        super().__init__(a, b)  # super(B, self).__init__(a, b)
        self.c = c
# 未绑定
class C(Base):
    def __init__(self, a, b, c):
        Base.__init__(self, a=a, b=1000)
```
```python
B(1,2,3).a, B(1,2,3).b, B(1,2,3).c
BB(1,2,3).a, BB(1,2,3).b, BB(1,2,3).c

(1, 2, 3)
(1, 1000, 3)
```
```
　　1. super并不是一个函数，是一个类名，形如super(B, self)事实上调用了super类的初始化函数，
       产生了一个super对象；
　　2. super类的初始化函数并没有做什么特殊的操作，只是简单记录了类类型和具体实例；
　　3. super(B, self).func的调用并不是用于调用当前类的父类的func函数；
　　4. Python的多继承类是通过mro的方式来保证各个父类的函数被逐一调用，而且保证每个父类函数
       只调用一次（如果每个类都使用super）；
　　5. 混用super类和非绑定的函数是一个危险行为，这可能导致应该调用的父类函数没有调用或者一
       个父类函数被调用多次。
```
### super函数使用_以LR为例
```python
from sklearn.linear_model import LogisticRegression

class LR(LogisticRegression):

    def __init__(self, threshold=0.01, dual=False, tol=1e-4, C=1.0,
                 fit_intercept=True, intercept_scaling=1, class_weight=None,
                 random_state=None, solver='liblinear', max_iter=100,
                 multi_class='ovr', verbose=0, warm_start=False, n_jobs=1):
        #权值相近的阈值
        self.threshold = threshold
        super(LR, self).__init__(penalty='l1', dual=dual, tol=tol, C=C,
                 fit_intercept=fit_intercept,
                 intercept_scaling=intercept_scaling,
                 class_weight=class_weight,
                 random_state=random_state,
                 solver=solver, max_iter=max_iter,
                 multi_class=multi_class, 
                 verbose=verbose,
                 warm_start=warm_start, 
                 n_jobs=n_jobs)
        #使用同样的参数创建L2逻辑回归
        self.l2 = LogisticRegression(penalty='l2', dual=dual, tol=tol, C=C, fit_intercept=fit_intercept, intercept_scaling=intercept_scaling, 
                 class_weight = class_weight, random_state=random_state, 
                 solver=solver, 
                 max_iter=max_iter,
                 multi_class=multi_class, 
                 verbose=verbose,
                 warm_start=warm_start, 
                 n_jobs=n_jobs)
                 
    def fit(self, X, y, sample_weight=None):
        #训练L1逻辑回归
        super(LR, self).fit(X, y, sample_weight=sample_weight) # 这个不需要实例化就直接用父类的方法，父类在之前已经被初始化了penalty = 'l1'那个。
        self.coef_old_ = self.coef_.copy() # 继承了父类的，所以可以直接用self.coef_
        #训练L2逻辑回归
        self.l2.fit(X, y, sample_weight=sample_weight)
        print self.coef_
        print self.l2.coef_
```

### 装饰器

_装饰器详解可参照[basic文档](https://github.com/binzhouchn/python_notes/blob/master/00.basic/README.md#装饰器)_

a. @classmethod: 不需要self参数，但第一个参数需要是表示自身类的cls参数
```
@classmethod意味着：当调用此方法时，我们将该类作为第一个参数传递，而不是该类的实例（正如我们通常使用的方法）。
这意味着您可以使用该方法中的类及其属性，而不是特定的实例
```
b. @staticmethod: 不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样
```
@staticmethod意味着：当调用此方法时，我们不会将类的实例传递给它（正如我们通常使用的方法）。
这意味着你可以在一个类中放置一个函数，但是你无法访问该类的实例（当你的方法不使用实例时这很实用）
```
```python
class A(object):  
    bar = 1  
    def foo(self):  
        print 'foo'  
 
    @staticmethod  
    def static_foo():  
        print 'static_foo'  
        print A.bar  
 
    @classmethod  
    def class_foo(cls):  
        print 'class_foo'  
        print cls.bar  
        cls().foo()
        
A.static_foo()  
A.class_foo()
```
```python
static_foo
1
class_foo
1
foo
```

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

### 装饰器property

把一个getter方法变成属性，只需要加上@property就可以了，此时，@property本身又创建了另一个装饰器@score.setter，
负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作<br>
```python
class Student(object):

    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth

a = Student()
a.birth = 22 # 这个的birth.setter装饰器相当于把之前birth方法变成了属性
print(a.birth)
print(a.age)
```

### 单例模式
```python
# 使用__new__方法
#写法一
class Singleton(object):
    def __new__(cls, *args, **kw):
        if not hasattr(cls, '_instance'):
            orig = super(Singleton, cls)
            cls._instance = orig.__new__(cls, *args, **kw)
        return cls._instance
#写法二
class Singleton(object):
    __instance=None
    def __init__(self):
        pass
    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance=super(Singleton, cls).__new__(cls,*args,**kwargs)
        return cls.__instance
```
```python
# 这个class是自己定义的class可以继承singleton实现单例模式
# MyClass只加载一次
class MyClass(Singleton):
    def __init__(self):
        print('ok')
    def kk(self):
        print('effwfwsefwefwef')
```
> 写一个装饰器@singleton也行
```python
def singleton(cls, *args, **kw):
    instance={}
    def _singleton():
        if cls not in instance:
            instance[cls]=cls(*args, **kw)
        return instance[cls]
    return _singleton

@singleton
class A:
    def __init__(self):
        pass
    def test(self,num):
        return num*2
```


### DeprecationWarning

```python
import warnings
import functools

def deprecated(func):
    """This is a decorator which can be used to mark functions
    as deprecated. It will result in a warning being emitted
    when the function is used."""
    @functools.wraps(func)
    def new_func(*args, **kwargs):
        warnings.simplefilter('always', DeprecationWarning)  # turn off filter
        warnings.warn("Call to deprecated function {}.".format(func.__name__),
                      category=DeprecationWarning,
                      stacklevel=2)
        warnings.simplefilter('default', DeprecationWarning)  # reset filter
        return func(*args, **kwargs)
    return new_func

@deprecated
def some_old_function(x, y):
    return x + y
```

### 定制类

[廖雪峰 定制类](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/0014319098638265527beb24f7840aa97de564ccc7f20f6000)

### 网络编程

[网络编程网址](https://blog.csdn.net/qq_41853758/article/details/82853811)<br>

### 