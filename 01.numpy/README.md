
## 一级目录

[**1. numpy类型**](#numpy类型)

[**2. np.where用法**](#np_where用法)

[**3. 数组方法**](#数组方法)

[**4. xx用法**](#xx用法)

---

### numpy类型

具体如下：

|基本类型|可用的**Numpy**类型|备注
|--|--|--
|布尔型|`bool`|占1个字节
|整型|`int8, int16, int32, int64, int128, int`| `int` 跟**C**语言中的 `long` 一样大
|无符号整型|`uint8, uint16, uint32, uint64, uint128, uint`| `uint` 跟**C**语言中的 `unsigned long` 一样大
|浮点数| `float16, float32, float64, float, longfloat`|默认为双精度 `float64` ，`longfloat` 精度大小与系统有关
|复数| `complex64, complex128, complex, longcomplex`| 默认为 `complex128` ，即实部虚部都为双精度
|字符串| `string, unicode` | 可以使用 `dtype=S4` 表示一个4字节字符串的数组
|对象| `object` |数组中可以使用任意值|
|Records| `void` ||
|时间| `datetime64, timedelta64` ||


### np_where用法
```python
arr = array([ 0.31593257, 0.33837679, 0.38240686, 0.38970056, 0.54940456]) 
pd.Series(np.where(arr > 0.5, 1, 0), name='result').to_csv(path_save, index=False, header=True) 
```
这句话的意思是arr中值大于0.5赋为1，小于等于0.5赋为0，然后把这个series的名字命名为result，最后保存成csv文件去掉index，保留列名

### 数组方法
```python
a = array([[1,2,3],
            [4,5,6]])
            
# 求和， 沿第一维求和，沿第二维求和 下面函数都类似
sum(a) 21
a.sum() 21
sum(a,axis=0) array([5, 7, 9])
sum(a, axis=1) array([ 6, 15])
# 求积
a.prod() 720
prod(a) 720
# 求最大最小及最大最小值的位置
a.min() 1
a.max() 6
a.argmin() 0
a.argmax() 5
# 求均值、标准差
a.mean()
a.std()
# clip方法，将数值限制在某个范围
a.clip(3,5) array([[3,3,3],[4,5,5]])
# ptp方法，计算最大值和最小值之差
a.ptp() 5

# 生成二维随机矩阵并且保留3位小数
from numpy.random import rand
a = rand(3,4)
%precision 3 #这个修饰可以运用在整个IDE上
```

### xx用法
