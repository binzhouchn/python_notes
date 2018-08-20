# 目录

[**1. xgboost优化**](#xgboost优化)

[**2. xgboost在windows上安装**](#xgboost在windows上安装)

[**3. xgboost参数**](#xgboost参数)

[**4. xgboost sklearn框架和原生态框架**](#xgboost_sklearn框架和原生态框架)

[**5. xgb调参示例代码**](#xgb调参示例代码)

---

## xgboost优化

**xgb是gbdt的优化：主要两方面**
1.目标函数，传统GBDT在优化时只用到一阶导数信息（负梯度），xgboost则对代价函数进行了二阶泰勒展开，同时用到一阶和二阶导数<br>
2.我们知道，决策树的学习最耗时的一个步骤就是对特征的值进行排序（因为要确定最佳分割点），xgboost在训练之前，预先对数据进行排序，然后保存为block结构，后面的迭代中重复地使用这个结构，大大减小计算量。<br>

这个block结构也使得并行成为了可能，在进行节点分裂时，需要计算每个特征的增益，最终选增益最大的那个特征去做分裂，那么各个特征的增益计算就可以开多线程进行。 （后期用直方图算法，用于高效地生成候选的分割点）

**lgb对xgb的优化**
1.基于Histogram的决策树算法<br>
2.带深度限制的Leaf-wise的叶子生长策略<br>
3.直方图做差加速<br>
4.直接支持类别特征(Categorical Feature)<br>
5.Cache命中率优化<br>
6.基于直方图的稀疏特征优化<br>
7.多线程优化<br>

## xgboost在windows上安装

xboost在windows安装需要自己编译，编译的过程比较麻烦(需要安装visual studio等)，而且需要复杂的软件环境。为了免去编译，我这里把编译好的文件供大家下载安装。有了编译好的文件，xgboost的安装变得超级简单（注：编译好的dll文件仅适用于windows64位操作系统）

(1) 下载我提供的xgboost代码和编译好的dll文件libxgboost.zip解压:
[xgboost-master.zip](xgboost-master.zip), [libxgboost.zip](libxgboost.zip)

(2) 将xgboost-master.zip 文件解压缩到python的…\python2.7\Lib\site-packages目录下

(3) 复制libxgboost.dll文件到 ....\site-package\xgboost-master\python-package\xgboost\目录

(4) 打开cmd，命令行进入 ....\site-package\xgboost-master\python-package\ 目录

(5) 执行命令：python setup.py install

(6) Done!

## xgboost参数
```python
import xgboost as xgb

params={
    'booster':'gbtree',
    'objective': 'binary:logistic',
    'scale_pos_weight': 1/7.5,
    #7183正样本
    #55596条总样本
    #差不多1:7.7这样子
    'gamma':0.2,  # 用于控制是否后剪枝的参数,越大越保守，一般0.1、0.2这样子。
    'max_depth':8, # 构建树的深度，越大越容易过拟合
    'lambda':3,  # 控制模型复杂度的权重值的L2正则化项参数，参数越大，模型越不容易过拟合。
    'subsample':0.7, # 随机采样训练样本
    #'colsample_bytree':0.7, # 生成树时进行的列采样
    'min_child_weight':3, 
    # 这个参数默认是 1，是每个叶子里面 h 的和至少是多少，对正负样本不均衡时的 0-1 分类而言
    #，假设 h 在 0.01 附近，min_child_weight 为 1 意味着叶子节点中最少需要包含 100 个样本。
    #这个参数非常影响结果，控制叶子节点中二阶导的和的最小值，该参数值越小，越容易 overfitting。 
    'silent':0 ,#设置成1则没有运行信息输出，最好是设置为0.
    'eta': 0.03, # 如同学习率
    'seed':1000,
    'nthread':12,# cpu 线程数
    'eval_metric':'auc',
    'missing':-1
}
plst = list(params.items())
num_rounds = 2000 # 迭代次数
xgb_train = xgb.DMatrix(X, label=y)
xgb_val = xgb.DMatrix(val_X,label=val_y)
watchlist = [(xgb_train, 'train'),(xgb_val, 'val')]
model = xgb.train(plst, xgb_train, num_boost_round=75000,evals=watchlist,early_stopping_rounds=500)
```
```python
params = {
        'colsample_bytree': 0.5041920450812235,
        'gamma': 0.690363148214239,
        'learning_rate': 0.01,
        'max_depth': 8,
        'min_child_weight': 9,
        'nthread': 1,
        'objective': 'binary:logistic',
        'reg_alpha': 4.620727573976632,
        'reg_lambda': 1.9231173132006631,
        'scale_pos_weight': 5,
        'seed': 2017,
        'subsample': 0.5463188675095159
        }
```

## xgboost_sklearn框架和原生态框架

- sklearn框架
```python
model = xgb.BoostClassifier(加参数即params=)
xgb_m1 = model.fit()
xgb_m1.predict / xgb_m1.predict_proba
```
- 原生态框架
```python
xgb.train() 这个是xgb的原生态框架
需要将数据 data_t = xgb.DMatrix(X, label=y)
xgb_m2 = xgb.train(params, data_t)
xgb_m2.predict(xgb.DMatrix(test))  这个得到的就是概率【一列 n*1】，而sklean中predict得到的是0和1,predict_proba得到的是概率【两列 n*2，看后面一列>0.5预测为1】
还有个参数evals可以加验证集，early_stopping_rounds=1000 最高迭代1000次，如果验证集误差上升就停止
```

## xgb调参示例代码

[xgboost调参示例代码](xgboost调参示例代码.py)
