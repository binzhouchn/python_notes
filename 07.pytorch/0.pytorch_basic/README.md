## pytorch实用技巧

[**1. view函数**](#view函数)

[**2. unsqueeze函数**](#unsqueeze函数)


---

### view函数

```python
import torch as t
a = t.arange(0,6)
print(a)
# tensor([ 0.,  1.,  2.,  3.,  4.,  5.])
a.view(2,-1) # 行数为2行，-1表示列自动计算
# tensor([[ 0.,  1.,  2.],
#         [ 3.,  4.,  5.]])
```

### unsqueeze函数

```python
import torch as t
a = t.arange(0,6).view(2,3)
print(a)
# tensor([[ 0.,  1.,  2.],
#         [ 3.,  4.,  5.]])
print(a.size())
# torch.Size([2, 3])
```
```python
a.unsqueeze(0).size()
# torch.Size([1, 2, 3])
a.unsqueeze(1).size()
# torch.Size([2, 1, 3])
a.unsqueeze(2).size()
# torch.Size([2, 3, 1])
```

