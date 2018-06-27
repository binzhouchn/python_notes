## 一级目录

[**0. 特征工程相关查阅feature_engineering仓库**](https://github.com/binzhouchn/feature_engineering)

[**1. 将数据集进行train, test分割**](#将数据集进行train_test分割)

[**2. 对数据集进行随机抽样**](#对数据集进行随机抽样)

 - [抽样方法一](#抽样方法一)
 - [抽样方法二](#抽样方法二)

[**3. 对结果进行评判，混淆矩阵**](#对结果进行评判用混淆矩阵)

[**4. 模型效果评价accuracy, logloss, precision, recall等**](#模型效果评价)

---

### 将数据集进行train_test分割
```python
# 训练测试样本集 stratify可以指定分割是否需要分层，分层的话正负样本在分割后还是保持一致, 输入的label
from sklearn.cross_validation import train_test_split
def train_test_sep(X, test_size = 0.25, stratify = None, random_state = 1001):
        train, test = train_test_split(X, test_size = test_size, stratify = stratify, random_state = random_state)
        return train, test
```
### 对数据集进行随机抽样

#### 抽样方法一
```python
df.sample(n=None, frac=None, replace=False, weights=None, random_state=None, axis=None)

- n是要抽取的行数。（例如n=20000时，抽取其中的2w行）
- frac是抽取的比列。（有一些时候，我们并对具体抽取的行数不关系，我们想抽取其中的百分比，这个时候就可以选择使用frac，例如frac=0.8，就是抽取其中80%）
- replace抽样后的数据是否代替原DataFrame()
- weights这个是每个样本的权重，具体可以看官方文档说明。
- random_state这个在之前的文章已经介绍过了。
- axis是选择抽取数据的行还是列。axis=0的时是抽取行，axis=1时是抽取列（也就是说axis=1时，在列中随机抽取n列，在axis=0时，在行中随机抽取n行）
```
#### 抽样方法二
```python
import random
random_num_test = random.sample(np.arange(0,len(df)),200)
random_num_train = list(set(xrange(len(df)))^set(random_num_test))
test = df.iloc[random_num_test]
train = df.iloc[random_num_train]
```

### 对结果进行评判用混淆矩阵
```python
from sklearn.metrics import confusion_matrix
confusion_matrix(y_true, y_pred)
```

### 模型效果评价
```python
# accuracy 准确率是针对y_true和y_pred都是类别的比如0和1
from sklearn.metrics import accuracy_score
accuracy_score(y_true, y_pred)
```
```python
# log_loss 又叫交叉熵,y_true是类别比如0和1，y_pred是属于类别1的概率值
from sklearn.metrics import log_loss
logloss = log_loss(y_true, y_pred, eps=1e-15)
```
```python
# recall precision
from sklearn.metrics import confusion_matrix
confusion_matrix(y_true, y_pred)
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.metrics import f1_score
```

