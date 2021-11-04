# python调用golang

## 示例一 python端输入int返回int

```Go
package main

import (
	"C"
)

func f1(x int) int {
	return x*x + 2
}

//export Fib
func Fib(n int) int {
	if n == 1 || n == 2 {
		return 1
	} else {
		return Fib(n-1) + Fib(n-2) + f1(1)
	}
}

func main() {}
```

//go build -buildmode=c-shared -o _fib.so fib.go<br>
//参考链接https://blog.csdn.net/cainiao_python/article/details/107724309<br>
//将_fib.so文件拷贝到python文件夹下<br>

```python
import ctypes
import time
from ctypes import *
so = ctypes.cdll.LoadLibrary('./_fib.so')
start = time.time()
result = so.Fib(40)
end = time.time()
print(f'斐波那契数列第40项：{result}，耗时：{end - start}')
```

## 示例二 python端输入string返回string（推荐看示例三）

```Go
package main

import (
	"C"
	"database/sql"
	"log"
	"strings"

	_ "github.com/go-sql-driver/mysql"
)

//export Gdbc
func Gdbc(uri *C.char) string {
	log.Println(uri)
	db, err := sql.Open("mysql", C.GoString(uri))
	if err != nil {
		log.Fatalln(err)
	}
	rows, err := db.Query("SELECT feature_word FROM insurance_qa.feature_words")
	if err != nil {
		log.Fatalln(err)
	}
	res := []string{}
	for rows.Next() {
		var s string
		err = rows.Scan(&s)
		if err != nil {
			log.Fatalln(err)
		}
		// log.Printf("found row containing %q", s)
		res = append(res, s)
	}
	rows.Close()
	return strings.Join(res, ",")
}

func main() {
	// res := Gdbc("username:password@tcp(localhost:3306)/database?charset=utf8")
	// fmt.Println(res)
}
```
//go build -buildmode=c-shared -o _gdbc.so test.go<br>
//将_gdbc.so文件拷贝到python文件夹下<br>

```python
import ctypes
import time
from ctypes import *
class StructPointer(Structure):  
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

so = ctypes.cdll.LoadLibrary('./_gdbc.so')
so.Gdbc.restype = StructPointer
start = time.time()
uri = "username:password@tcp(localhost:3306)/database?charset=utf8"
res = so.Gdbc(uri.encode("utf-8"))
print(res.n)
print(res.p[:res.n].decode())#print(res.p.decode())这样貌似也没问题
end = time.time()
print(f'耗时：{end - start}')
```

## 示例三 python端输入string，go查询数据库然后返回json str

```Go
package main

import (
	"C"
	"database/sql"
	"encoding/json"
	"log"

	_ "github.com/go-sql-driver/mysql"
)

type Fw struct {
	feature_word string
	word_type    string
	id           int64
}

//export Gdbc
func Gdbc(uri *C.char) string {
	db, err := sql.Open("mysql", C.GoString(uri))
	//设置数据库最大连接数
	db.SetConnMaxLifetime(100)
	//设置上数据库最大闲置连接数
	db.SetMaxIdleConns(10)
	if err != nil {
		log.Fatalln(err)
	}
	rows, err := db.Query("SELECT feature_word,word_type,id FROM insurance_qa.feature_words")
	if err != nil {
		log.Fatalln(err)
	}
	res := [][]interface{}{}
	var fw Fw
	for rows.Next() {
		err = rows.Scan(&fw.feature_word, &fw.word_type, &fw.id)
		if err != nil {
			log.Fatalln(err)
		}
		// log.Printf("found row containing %q", s)
		tmp := []interface{}{}
		tmp = append(tmp, fw.feature_word)
		tmp = append(tmp, fw.word_type)
		tmp = append(tmp, fw.id)
		res = append(res, tmp)
		// res = append(res, []interface{}{fw.feature_word, fw.word_type, fw.id})//上面的一行写法
	}
	rows.Close()
	b, err := json.Marshal(res)
	if err != nil {
		panic(err)
	}
	result := string(b)
	return result
}

func main() {}

```

//go build -buildmode=c-shared -o _gdbc.so test.go<br>
//将_gdbc.so文件拷贝到python文件夹下<br>

```python
import ctypes
import time
import json
from ctypes import *
class StructPointer(Structure):
    _fields_ = [("p", c_char_p), ("n", c_longlong)]

so = ctypes.cdll.LoadLibrary('./_gdbc.so')
so.Gdbc.restype = StructPointer
start = time.time()
uri = "username:password@tcp(localhost:3306)/database?charset=utf8"
res = so.Gdbc(uri.encode("utf-8"))
print(res.n)
print(res.p.decode())
print(json.loads(res.p.decode()))
end = time.time()
```

## 