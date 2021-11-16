# ansible笔记

```shell
在/etc/ansible/ansible.cfg下配置[model]
# ping
ansible model -m ping
# ansible-playbook写剧本
ansible-playbook xxx.yaml
# 传文件
ansible model -m copy -a "src=./test.txt dest=/home/zhoubin"
# 创建文件(ansible-playbook形式)
- hosts: model
  remote_user: zhoubin
  tasks:
    - name: "create test2.txt in the /etc directory"
      file:
        path: "/home/zhoubin/test2.txt"
        state: "touch"
# 创建文件夹(ansible-playbook形式)
- hosts: model
  remote_user: zhoubin
  tasks:
    - name: "create tmp file in the /etc directory"
      file:
        path: "/home/zhoubin/tmp"
        state: "directory"
# 删除文件(ansible-playbook形式)
- hosts: model
  remote_user: zhoubin
  tasks:
    - name: "delete test.txt in the /etc directory"
      file:
        path: "/home/zhoubin/test.txt"
        state: "absent"
# 删除多个文件(ansible-playbook形式)
- hosts: model
  remote_user: zhoubin
  tasks:
    - name: "delete multi files in the /etc directory"
      file:
        path: "{{ item }}"
        state: "absent"
      with_items:
        - /home/zhoubin/test1.txt
        - /home/zhoubin/test2.txt
# 将远程服务器文件拷贝到本机
ansible model -m fetch -a "src=/home/zhoubin/test.txt dest=./ force=yes backup=yes"

# 写一个剧本(传docker镜像并且加载) become:yes可以避免sudo输密码!
- hosts: model
  remote_user: zhoubin
  tasks:
    - name: copy docker image
      copy: src=./py37.tar.gz dest=/home/zhoubin
    - name: load image
      shell: docker load -i /home/zhoubin/py37.tar.gz
      become: yes


```


### 附录

[超简单ansible2.4.2.0与playbook入门教程](https://blog.csdn.net/qq_45206551/article/details/105004233)<br>
[ansible-命令使用说明](https://www.cnblogs.com/scajy/p/11353825.html)<br>
