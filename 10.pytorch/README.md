[pytorch官网](https://pytorch.org/)

安装Pytorch会安装两个模块, 一个是torch, 一个是torchvision, <br>
torch 是主模块, 用来搭建神经网络的；<br>
torchvision 是辅模块, 有数据库, 还有一些已经训练好的神经网络可以直接用, 如VGG, AlexNet, ResNet<br>

## 目录

[**1. pytorch入门知乎**](#入门知乎网址)

[**2. pytorch入门之Tensor**](#tensor)

[**3. pytorch入门之Autograd**](#autograd)

[**4. pytorch入门之构造一个小型CNN**](#lenet)


---

### 入门知乎网址

https://www.zhihu.com/question/55720139

### Tensor


### Autograd


### LeNet

[完整代码lenet.py及注释](lenet.py)

运行完该代码我们得到下图:

![pic1](pic1.png)

该网络有5层神经元，第一层是1到6的卷积层，第二层是6到16的卷积层，第三层到第5层均为全连接层。第一层的参数计算是6x1x5x5=150，
当然别忘了还有bias=6，所以第一层的参数总量是150+6=156。以此类推，总参数和为61706个。

> 注意：torch.nn只接受mini-batch的输入，也就是说我们输入的时候是必须是好几张图片同时输入<br>
> 例如：nn. Conv2d 允许输入4维的Tensor：n个样本 x n个色彩频道 x 高度 x 宽度<br>
