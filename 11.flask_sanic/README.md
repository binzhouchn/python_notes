# flask

## GET方法
```python
# GET方法
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False # 防止中文乱码
tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done': False
    },
    {
        'id': 2,
        'title': u'Learn Python',
        'description': u'Need to find a good Python tutorial on the web',
        'done': False
    }
]
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})
if __name__ == '__main__':
    app.run(host=127.0.0.1,
    port=5000)
```

## POST方法
```python
# -*- coding: utf-8 -*-
from flask import Flask  
from flask import request
from flask import make_response,Response
from flask import jsonify
# 抛出flask异常类
class CustomFlaskErr(Exception):
    # 自己定义了一个 responseCode，作为粗粒度的错误代码
    def __init__(self, responseCode=None):
        Exception.__init__(self)
        self.responseCode = responseCode
        self.J_MSG = {9704: '参数不合法！',9999:'系统内部异常！'}
    # 构造要返回的错误代码和错误信息的 dict
    def get_dict(self):
        rv = dict()
        # 增加 dict key: response code
        rv['responseCode'] = self.responseCode
        # 增加 dict key: responseMsg, 具体内容由常量定义文件中通过 responseCode 转化而来
        rv['responseMsg'] = self.J_MSG[self.responseCode]
        return rv
def get_chatterbot_result(xx):
    pass # 这里应该return标准问题及ID，标准答案及ID，相似问及ID等之类的东西

app = Flask(__name__)    
app.config['JSON_AS_ASCII'] = False

@app.route('/')    
def get_simple_test():
    return 'BINZHOU TEST'    

@app.route('/req_message', methods=['POST'])
def req_message():
    if request.method == 'POST':
        sid = request.form.get('sid')
        q = request.form.get('q')
        uid = request.form.get('uid','default_uid') # 可为空
        businessId = request.form.get('businessId')
        messageId = request.form.get('messageId','default_messageId') # 可为空
        source = request.form.get('source','default_source') # 可为空
        requestTime = request.form.get('requestTime')
        requestId = request.form.get('requestId')
        if not (sid and q and businessId and requestTime and requestId):
            raise CustomFlaskErr(responseCode=9704)
    # 进过我们自己定义的模块和chatterbot返回答案以及我们想要的一些东西等
    # bot_answer包含标准问题及ID，标准答案及ID，相似问及ID等之类的东西，需要解析一下然后给result
    bot_answer = get_chatterbot_result(q)
    # 根据机器人得到的结果将整个返回报文进行组装
    result = {
        'sid':sid,
        'q':q,
        'uid':uid,
        'businessId':businessId,
        'messageId':messageId,
        'type':0,
        'source':source,
        'sqId':12345,
        'stQuestion':'绍兴在哪里？',
        'sm':[
            {'smid':12346,'smQuestion':'绍兴?哪里?'},
             {'smid':12347,'smQuestion':'绍兴是哪里的啊啊'}],
        'answer':{
            "aid":"12345",
            "answare_text":"绍兴在浙江",
            "atype":1
            },
        'responseCode':'0000',
        'responseMsg':'返回成功',
        'responseTime':'20180601'
    }
    return jsonify(result)

@app.errorhandler(CustomFlaskErr)
def handle_flask_error(error):
    # response的json内容为自定义错误代码和错误信息
    response = jsonify(error.get_dict())
    response.responseCode = error.responseCode
    return response

if __name__ == '__main__':
    app.run(host='127.0.0.1',
port='5000')
```

# sanic 
```python
# sanic get和post方法
# 使用了异步特性，而且还使用uvloop作为事件循环，其底层使用的是libuv，从而使 Sanic的速度优势更加明显。
from sanic.response import json
from sanic import Sanic
from sanic.response import json
from sanic.response import text

app = Sanic()

@app.route("/")
async def index(request):
    return text('Hello World!')

@app.route("/post_form_data",methods=["POST"])
async def post_form_data(request):
    name = request.form.get("name")
    return text(name)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000)
```
