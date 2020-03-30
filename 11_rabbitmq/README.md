# 消息队列

 - [1. 简单使用步骤](#简单使用步骤)
 - [xxx](#xx)


[rabbitmq tutorial](https://www.rabbitmq.com/tutorials/tutorial-one-python.html)<br>

简单使用步骤<br>
1. [安装RabbitMQ Server](https://www.rabbitmq.com/download.html)<br>
用docker安装即可

2. 启动docker<br>
```shell
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
# port 5672
```

3. 生产者和消费者代码(hello_world basic demo)<br>

receive.py<br>
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

send.py<br>
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



