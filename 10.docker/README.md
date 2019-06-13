# simple use for docker

## 1. docker安装

1.1 mac下安装<br>
[mac安装网址](https://hub.docker.com/editions/community/docker-ce-desktop-mac)<br>
[docker docs for mac](https://docs.docker.com/docker-for-mac/)<br>

1.2 linux下安装<br>
TODO

## 2. docker基本命令

2.1 docker查看版本及images
```shell
docker --version
docker images
```

2.2 docker run
```shell
docker run hello-world
```

2.3 docker跑完以后需要删除container再删除image
```shell
# 查看image对应的container id
docker ps -a
# 删除container
docker rm container_id
# 删除image
docker rmi image_id
# 也可以直接暴力删除image
docker rmi -f image_id
# 如果存在同名同id不同tag的镜像
可以使用repository：tag的组合来删除特殊的镜像
```

2.4 docker保存和读取image
```shell
# 保存
docker save -o helloword_test.tar fce45eedd449(image_id)
# 读取
docker load -i helloword_test.tar
```

2.5 docker保存和读取container
```shell
# 保存
docker export -o helloword_test.tar fce45eedd444(container_id)
# 读取
docker import ...
```

2.6 修改repository和tag名称
```shell
# 加载images后可以名称都为<none>
docker tag [image id] [name]:[版本]
```

2.7 docker跑一个简单的flask demo
```shell
# -d后台运行 -p端口映射
docker run -d -p 5000:5000 -v $PWD/myapp:/usr/src/myapp  -w /usr/src/myapp binzhou/python35:v2 python app.py
```

2.8 docker 





