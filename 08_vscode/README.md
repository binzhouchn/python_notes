# vscode使用（版本1.86.2）

## 1.在VScode中添加远程Linux服务器中Docker容器中的Python解释器

**以dgx.6机器为例**<br>
```shell
# 第一步 创建容器
nvidia-docker run -d --name myllm -p 8891:22 -v $PWD/llm:/workspace/llm -w /workspace/llm -it 10.xx.xx.xxx/zhoubin/llm:py311-cuda12.1.0-cudnn8-devel-ubuntu22.04 /bin/bash
注释：
[-p 8891:22]：把docker的端口号22映射到服务器的端口号8891。
[-d]：容器后台运行，避免退出容器后容器自动关闭。
[-v]：挂载和同步目录，服务器和docker内有一个文件夹保持同步。
[-it]：确保docker后台交互运行。
[10.xx.xx.xxx/zhoubin/llm:py311-cuda12.1.0-cudnn8-devel-ubuntu22.04]：镜像名。
[/bin/bash]：docker内要运行的指令。
```
```shell
#第二步 在容器内安装ssh服务
docker exec -it [容器ID] /bin/bash
# 更新apt-get
命令：apt-get update
# 安装vim
命令：apt-get install vim
# 安装openssh-server
命令：apt-get install openssh-server
# 设置root密码(docker里面的用户名和密码，我这边账号密码都是root/root)
命令：passwd
```
```shell
# 第三步 配置/etc/ssh/sshd_config文件
# 在文件/etc/ssh/sshd_config中添加下面的代码：
PubkeyAuthentication yes
PermitRootLogin yes

# 第四步 重启ssh服务(好像每次停止容器后重启都需要运行下)
/etc/init.d/ssh restart
或 service ssh restart

# 第五步 退出docker后，验证端口映射
docker ps -a
docker port [容器ID] 22
若结果输出“0.0.0.0：8891”，则说明端口映射正确。
```
```shell
# 第6步 本地电脑连接docker（见Termius dgx6_docker_llm）
ssh root@11.xx.xx.xxx -p 8891 ，密码是root
```
```shell
# 使用VSCode连接远程主机上的docker container
# 打开VScode编辑器，按下快捷键“Ctrl+Shift+X”，查找安装“Remote Development”。安装完成后需要点击“reload”，然后按下快捷键“Ctrl+Shift+P”，输入“remote-ssh”，选择“open SSH Configuration file”，在文件xx/username/.ssh/config中添加如下内容：
Host llm_docker #Host随便起名字
  HostName 11.xxx.xx.x
  User root
  Port 8891

#保存后，按下快捷键"Ctrl+Shift+P"，输入"remote-ssh"，选择"Connect to Host..."，然后点击"llm_docker"，接着选择“Linux”，最后按提示输入第三步中设置的root连接密码，在左下角显示"SSH:llm_docker"，说明已经成功连接docker。
```

```shell
#内网环境远程如果出现连接不上，大概率是vscode-server无法下载导致，可以手动搞定
https://update.code.visualstudio.com/commit:903b1e9d8990623e3d7da1df3d33db3e42d80eda/server-linux-x64/stable

具体参考附录中的[VSCode连不上远程服务器]
```






----

[vscode历史版本下载地址](https://code.visualstudio.com/updates/v1_86)<br>
[vscode扩展应用市场vsix文件手动下载安装](https://marketplace.visualstudio.com/search?target=VSCode&category=All%20categories&sortBy=Installs)<br>
[vscode扩展应用市场vsix文件手动下载历史版本插件包](https://blog.csdn.net/qq_15054345/article/details/133884626)<br>
[在VScode中添加Linux中的Docker容器中的Python解释器](https://blog.csdn.net/weixin_43268590/article/details/129244984)<br>
[VSCode连不上远程服务器](https://blog.csdn.net/qq_42610612/article/details/132782965)<br>
[无网机的vscode中怎么使用jupyter notebook](https://www.bilibili.com/read/cv34411972/?jump_opus=1)<br>
