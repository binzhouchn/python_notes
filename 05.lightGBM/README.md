# 目录

[**1. lgb baseline模型**](#lgb_baseline模型)

[**2. lgb 自定义metric**](#lgb_自定义metric)


---

## lgb_baseline模型

[lgb_baseline模型](baseline_model.py)

## 自定义metric

```python
from sklearn import metrics
def ks(y_hat, data):
    y_true = data.get_label()
    fpr,tpr,thres = metrics.roc_curve(y_true,y_hat,pos_label=1)
    return 'ks', abs(fpr - tpr).max(), True

lgb_data = lgb.Dataset(X, y)

lgb.cv(
    params,
    lgb_data,
    num_boost_round=2000,
    nfold=5,
    stratified=False, # 回归一定是False
    early_stopping_rounds=100,
    verbose_eval=50,
    feval = ks, #ks  #这里增加feval参数
    show_stdv=True)
```