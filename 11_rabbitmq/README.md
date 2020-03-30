## 消息队列

 - [1. 简单使用步骤](#简单使用步骤)
 - [2. 启动rabbitmq docker命令](#启动docker命令)
 - [3. 简单的生产者和消费者demo代码](#简单的生产者和消费者demo代码)
 - [4. rabbitmq实现一台服务器同时给所有的消费者发送消息](#rabbitmq实现一台服务器同时给所有的消费者发送消息)


[rabbitmq tutorial](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)<br>

### 简单使用步骤

[安装RabbitMQ Server](https://www.rabbitmq.com/download.html)<br>
用docker安装即可

### 启动docker命令

```shell
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# port 5672
```
用docker启动RabbitMQ

### 简单的生产者和消费者demo代码

消费者 server.py<br>
```python
#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')


def callback(ch, method, properties, body):
    vec = json.loads(body)
    print(" [x] Received ", vec)


channel.basic_consume(
    queue='hello', on_message_callback=callback, auto_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
```
receive.py启动以后会一直监听host上的queue<br>

生产者 client.py<br>
```python
#!/usr/bin/env python
import pika
import json

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='', routing_key='hello', body=json.dumps([1.2,0.99,5.5]))
print(" [x] Sent 'Hello World!'")
connection.close()
```
send.py每发一次，receive.py那边会打印出发送的body信息


### rabbitmq实现一台服务器同时给所有的消费者发送消息

开了docker版的rabbitmq服务以后，在多台机器上先运行消费者server.py<br>
```python
#!/usr/bin/env python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
#创建exchange的名称为logs，指定类型为fanout
channel.exchange_declare(exchange='logs', exchange_type='fanout')
#删除随机创建的消息队列
queue_name = 'task_queue1' #每台机器上的名字最好不一样
result = channel.queue_declare(queue=queue_name)
channel.queue_bind(exchange='logs', queue=queue_name)
print(' [*] Waiting for logs. To exit press CTRL+C')
def callback(ch, method, properties, body):
    print(" [x] %r" % body)
channel.basic_consume(queue_name, callback)
channel.start_consuming()
```

然后再用生产者client.py发送给消费者，这个时候这些消费者会同时接收到该消息<br>
```python
import pika
import sys
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs',exchange_type='fanout')
message = ' '.join(sys.argv[1:]) or "info: Hello World!"
#指定exchange的名称
channel.basic_publish(exchange='logs', routing_key='', body=message)
print(" [x] Sent %r" % message)
connection.close()
```

### xxx