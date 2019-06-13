# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import make_response, Response
from flask import jsonify
import datetime
import jieba
jieba.initialize()


# 创建一个falsk对象
app = Flask(__name__)


@app.route('/')
def get_simple_test():
    return 'BINZHOU TEST'

@app.route('/req_message', methods=['POST'])
def req_message():
    print(request.json)
    if request.method == 'POST':
        id_ = request.json.get('id')
        text_ = request.json.get('text')
        text_sep_str = ' '.join(jieba.lcut(text_))
        res = {
            'sid': id_,
            'text_sep': text_sep_str,
            'responseTime': datetime.datetime.now().strftime('%Y%m%d%H%M%S')}
        return jsonify(res)

app.config['JSON_AS_ASCII'] = False
app.run(host='0.0.0.0', port=5000, debug=False)
