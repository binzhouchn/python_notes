## flask on docker demo

1. 如果用request.json则传入的数据需要json格式<br>
2. 如果用request.values则传入的数据是[(key, value),()]这种形式<br>

### 这里以json为例

```python
import requests
json={'id': 1223, 'text': '我是中国人'}
r = requests.post('http://0.0.0.0:5000/req_message', json=json)
r.json()

# {'responseTime': '20190515120101', 'sid': 1223, 'text_sep': '我 是 中国 人'}
```