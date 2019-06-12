# simple use for docker

## 1. docker安装

1.1 mac下安装<br>
[mac安装网址](https://hub.docker.com/editions/community/docker-ce-desktop-mac)<br>
[docker docs for mac](https://docs.docker.com/docker-for-mac/)<br>

1.2 linux下安装<br>


## 2. docker基本命令

2.1 docker查看版本
```shell
docker --version
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
# 


```
