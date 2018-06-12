## 一级目录

[**1. pandas dataframe手动创建**](#pandas_dataframe手动创建)

[**2. pandas dataframe中apply用法**](#pandas_dataframe中apply用法)

[**3. groupby用法**](#groupby用法)

[**4. explode用法**](#explode用法)

[**5. sort用法**](#sort用法)

[**6. left join用法**](#left_join用法)

[**7. reset_index用法**](#reset_index用法)

[**8. pandas to_csv**](#to_csv)

---
### pandas_dataframe手动创建

手动创建dataframe
```python
arr = np.array([['John','Lily','Ben'],[11,23,56]])
data = pd.DataFrame(arr.transpose(),columns=['name','age'])
```


### pandas_dataframe中apply用法

现在想看一下地址中含有-和,的数据有哪些可以进行如下操作： 
```python
data[data.address.apply(lambda x: ('-' in list(x)) and (',' in list(x)))]
```

### groupby用法

[**用法举例一**]
```python
gr = data.groupby(by='EID')
gr.agg({'BTBL':'max','BTYEAR':'count'}).reset_index() # 常见的max, min, count, mean, first, nunique
```
||EID|BTBL|BTYEAR
|--|--|--|--
|0|4|0.620|2011
|1|38|0.700|2013
|2|51|0.147|2002

这里对data根据EID进行groupby，然后根据字段BTBL, BTYEAR两个字段进行聚合，然后reset_index

[**用法举例二**]

||EID|ALTERNO|ALTDATE|ALTBE|ALTAF
|--|--|--|--|--|--
|1|399|05|2014-01|10|50
|2|399|12|2015-05|NaN|NaN
|3|399|12|2013-12|NaN|NaN
|4|399|27|2014-01|10|50
|5|399|99|2014-01|NaN|NaN

groupby EID然后想要统计一些唯一的月份有几个   
```python
# 方法一
def f(ll):
    fun = lambda x : x.split('-')[1]
    return len(set(map(fun,list(ll))))
# lambda套lambda写法
f = lambda ll : len(set(map(lambda x : x.split('-')[1],list(ll))))

p = pd.merge(data0, data2.groupby('EID').agg({'ALTERNO':'nunique','ALTDATE':f}).reset_index().rename(columns={'ALTERNO':'alt_count','ALTDATE':'altdate_nunique'}), how='left',on='EID')

#方法二
data2['year'] = data2.ALTDATE.apply(lambda x : x.split('-')[0])
data2['month'] = data2.ALTDATE.apply(lambda x : x.split('-')[1])
data2.groupby('EID').agg({'month':'nunique'}).reset_index().rename(columns={'month':'month_nunique'})
```

### explode用法

比如有个dataframe的结构如下

||city|community|longitude|latitude|address
|--|--|--|--|--|--
|1|上海|东方庭院|121.044|31.1332|复兴路88弄,珠安路77弄,浦祥路377弄

执行如下语句：
```python
data.drop('address',axis=1).join(data['address'].str.split(',',expand=True).stack().reset_index(level=1,drop=True).rename('address'))

# spark中的explode用法
spark_df = spark_df.select(spark_df['city'],spark_df['community_org'],spark_df['community'],\
spark_df['longitude'],spark_df['latitude'],(explode(split('address',','))).alias('address'),spark_df['villagekey'])
```
||city|community|longitude|latitude|address
|--|--|--|--|--|--
|1|上海|东方庭院|121.044|31.1332|复兴路88弄|
|2|上海|东方庭院|121.044|31.1332|珠安路77弄|
|3|上海|东方庭院|121.044|31.1332|浦祥路377弄|

### sort用法

注：df.sort()已经deprecated，以后可用df.sort_values()
```python
data3.sort_values(['EID','B_REYEAR'],ascending=True) #默认是升序排，先根据EID然后再根据B_REYEAR进行排序
```

### left_join用法
```python
data.merge(data1, how='left', on='id_code')
```

### reset_index用法
```python
data.reset_index(drop=True)
```

### to_csv
to_csv中的参数quoting: int or csv.QUOTE_* instance, default 0
控制csv中的引号常量。
可选 QUOTE_MINIMAL(0), QUOTE_ALL(1), QUOTE_NONNUMERIC(2) OR QUOTE_NONE(3)

