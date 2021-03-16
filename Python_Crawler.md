# Python	Crawler

## 第一章 网络请求

### 1-爬虫前奏

#### 1.1 什么是爬虫：

通俗理解，模拟人类访问网站，获取并储存息

#### 1.2 为什么用Python写爬虫程序：

1. PHP：并行开发能力弱，天生不是做这个的。

2. Java：语言本身很重大，代码量大。

3. C/C++：运行效率虽然高，但是学习、开发成本高。

4. Python：语法优美、代码简洁、开发效率高，有相关的框架

#### 1.3 准备工具：

1. Python 3.+开发环境。
2. Pycharm 2019 professions 版本。
3. 虚拟环境。“virtualenv/virtualenwrapper”.

### **==2- `http`协议和`Chrome`抓包工具==**

#### 2.1 url详解：

URL是统一资源定位符（“scheme:// host / port / path /?query-string=xx x#anchor”）

1. scheme：访问协议（HTTP / HTTPS/ FTP）；
2. host：主机名，域名；
3. port：端口号，默认为80端口；
4. path：查找路径；
5. query-string：查询字符串。

#### 2.2 常用的请求方法：

在http协议中，共定义8种请求方法，这里介绍两种（get(), post()）

1. `get` 请求：从服务器获取数据，不对服务器产生影响。
2. `post` 请求：对服务器产生影响（上传，修改数据）。

#### 2.3 请求头常见参数：

在`http`协议中，向服务器发送请求，数据分为三部分，分别为：`url、body、head`

1. User-Agent：浏览器的名称。在爬虫经常用到。用来伪装爬虫。
2. Referer：表明从哪个URl过来的。用来做反爬虫技术。
3. Cookie：`http`协议是无状态的。一般做登录后访问的网站需要Cookie信息。

#### 2.4 常见的响应状态码：

1. 200：请求正常。
2. 301：永久重定向。
3. 302：临时重定向。
4. 400：请求`url`在服务器上找不到。
5. 403：服务器拒绝访问，权限不够。
6. 500：服务器出现`bug`

#### 2.5 Chrome抓包工具：

`Chrome`浏览器非常亲近开发者的浏览器，可以方便的查看网络请求的数据。

### **==3-`urllib`库==**

> **urllib库是Python中一个最基本的网络请求库。可以模拟浏览器的行为，向指定的服务器发送一个请求，并可以保存服务器返回的数据。**

####  `3.1 urlopen`函数：

在`Python3`的`urllib`库中，所有和网络请求相关的方法，都被集到`urllib.request`模块下面了，以先来看下`urlopen`函数基本的使用

```python
from urllib import request
resp = request.urlopen("https://www.baidu.com")
print(resp.read())
```

实际上，使用浏览器访问百度，右键查看源代码。你会发现，跟我们刚才打印出来的数据是一模一样的。也就是说，上面的三行代码就已经帮我们把百度的首页的全部代码爬下来了。一个基本的url请求对应的python代码真的非常简单。

1. `url`：请求的网址；
2. `data`：请求的data，如果设置了这个值，那么将变成POST；
3. 返回值：返回值一个`http.client.HTTPResponse`对象，是一个类文件句柄对象。有`read(size)、readline()、readlines、getcode()`等方法。

#### `3.2 urlretrieve`函数：

这个函数可以方便的将网页上的一个文件保存到本地。以下代码可以非常方便的将百度的首页下载到本地

```python
from urllib import request
request.urlretrieve('http://www.baidu.com/','baidu.html')
```

#### `3.3 urlencode`函数：

用浏览器发送请求的时候，如果url中包含了中文或者其他特殊字符，那么浏览器会自动的给我们进行编码。而如果使用代码发送请求，那么就必须手动的进行编码，这时候就应该使用`urlencode`函数来实现。`urlencode`可以把字典数据转换为`URL`编码的数据。示例代码如下：

```python
from urllib import parse
data = {'name':'爬虫基础','greet':'hello world','age':100}
qs = parse.urlencode(data)
print(qs)
```

#### `3.4 parse_qs`函数：

可以将经过编码后的url参数进行解码。示例代码如下：

```python
from urllib import parse
qs = "name=%E7%88%AC%E8%99%AB%E5%9F%BA%E7%A1%80&greet=hello+world&age=100"
print(parse.parse_qs(qs))
```

#### `3.5 urlparse`和`urlsplit`函数：

有时候拿到一个url，想要对这个url中的各个组成部分进行分割，那么这时候就可以使用`urlparse`或者是`urlsplit`来进行分割。示例代码如下：

```python
from urllib import request,parse
url = 'http://www.baidu.com/s?username=zhiliao'
result = parse.urlsplit(url)
# result = parse.urlparse(url)
print('scheme:',result.scheme)
print('netloc:',result.netloc)
print('path:',result.path)
print('query:',result.query)
```

*urlparse和urlsplit基本上是一模一样的。唯一不一样的地方是，urlparse里面多了一个params属性，而urlsplit没有这个params属性。比如有一个url为：url = 'http://www.baidu.com/s;hello?wd=python&username=abc#1'*
*那么urlparse可以获取到hello，而urlsplit不可以获取到。url中的params也用得比较少。*

#### `3.6 request.Request`类：

如果想要在请求的时候增加一些请求头，那么就必须使用`request.Request`类来实现。比如要增加一个`User-Agent`，示例代码如下：

```python
from urllib import request
headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
req = request.Request("http://www.baidu.com/",headers=headers)
resp = request.urlopen(req)
print(resp.read())
```

#### `3.7 ProxyHandler`处理器（代理设置）：

很多网站会检测某一段时间某个IP的访问次数(通过流量统计，系统日志等)，如果访问次数多的不像正常人，它会禁止这个IP的访问。
所以我们可以设置一些代理服务器，每隔一段时间换一个代理，就算IP被禁止，依然可以换个IP继续爬取。
urllib中通过ProxyHandler来设置使用代理服务器，下面代码说明如何使用自定义opener来使用代理：

```python
from urllib import request
# 这个是没有使用代理的
# resp = request.urlopen('http://httpbin.org/get')
# print(resp.read().decode("utf-8"))
# 这个是使用了代理的
handler = request.ProxyHandler({"http":"218.66.161.88:31769"})
opener = request.build_opener(handler)
req = request.Request("http://httpbin.org/ip")
resp = opener.open(req)
print(resp.read())
```

常用的代理有：

- 西刺免费代理IP：http://www.xicidaili.com/
- 快代理：http://www.kuaidaili.com/
- 代理云：http://www.dailiyun.com/

#### `3.8` 什么是`cookie`：

在网站中，http请求是无状态的。也就是说即使第一次和服务器连接后并且登录成功后，第二次请求服务器依然不能知道当前请求是哪个用户。`cookie`的出现就是为了解决这个问题，第一次登录后服务器返回一些数据（`cookie`）给浏览器，然后浏览器保存在本地，当该用户发送第二次请求的时候，就会自动的把上次请求存储的`cookie`数据自动的携带给服务器，服务器通过浏览器携带的数据就能判断当前用户是哪个了。`cookie`存储的数据量有限，不同的浏览器有不同的存储大小，但一般不超过4KB。因此使用`cookie`只能存储一些小量的数据。

参数意义：

- NAME：cookie的名字。
- VALUE：cookie的值。
- Expires：cookie的过期时间。
- Path：cookie作用的路径。
- Domain：cookie作用的域名。
- SECURE：是否只在https协议下起作用。

#### `3.9`**使用`cookielib`库和`HTTPCookieProcessor`模拟登录：**

Cookie 是指网站服务器为了辨别用户身份和进行Session跟踪，而储存在用户浏览器上的文本文件，Cookie可以保持登录信息到用户下次与服务器的会话。
这里以人人网为例。人人网中，要访问某个人的主页，必须先登录才能访问，登录说白了就是要有cookie信息。那么如果我们想要用代码的方式访问，就必须要有正确的cookie信息才能访问。解决方案有两种，第一种是使用浏览器访问，然后将cookie信息复制下来，放到headers中。示例代码如下：

```python
from urllib import request

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    'Cookie': 'anonymid=jacdwz2x-8bjldx; depovince=GW; _r01_=1; _ga=GA1.2.1455063316.1511436360; _gid=GA1.2.862627163.1511436360; wp=1; JSESSIONID=abczwY8ecd4xz8RJcyP-v; jebecookies=d4497791-9d41-4269-9e2b-3858d4989785|||||; ick_login=884e75d4-f361-4cff-94bb-81fe6c42b220; _de=EA5778F44555C091303554EBBEB4676C696BF75400CE19CC; p=61a3c7d0d4b2d1e991095353f83fa2141; first_login_flag=1; ln_uact=970138074@qq.com; ln_hurl=http://hdn.xnimg.cn/photos/hdn121/20170428/1700/main_nhiB_aebd0000854a1986.jpg; t=3dd84a3117737e819dd2c32f1cdb91d01; societyguester=3dd84a3117737e819dd2c32f1cdb91d01; id=443362311; xnsid=169efdc0; loginfrom=syshome; ch_id=10016; jebe_key=9c062f5a-4335-4a91-bf7a-970f8b86a64e%7Ca022c303305d1b2ab6b5089643e4b5de%7C1511449232839%7C1; wp_fold=0'
}

url = 'http://www.renren.com/880151247/profile'

req = request.Request(url,headers=headers)
resp = request.urlopen(req)
with open('renren.html','w') as fp:
    fp.write(resp.read().decode('utf-8'))
```

但是每次在访问需要cookie的页面都要从浏览器中复制`cookie`比较麻烦。在`Python`处理`Cookie`，一般是通过`http.cookiejar`模块和`urllib模块的HTTPCookieProcessor`处理器类一起使用。`http.cookiejar`模块主要作用是提供用于存储`cookie`的对象。而`HTTPCookieProcessor`处理器主要作用是处理这些`cookie`对象，并构建`handler`对象。

#### **`3.10`保存cookie到本地：**

保存`cookie`到本地，可以使用`cookiejar`的`save`方法，并且需要指定一个文件名:

```python
from urllib import request
from http.cookiejar import MozillaCookieJar
cookiejar = MozillaCookieJar("cookie.txt")
handler = request.HTTPCookieProcessor(cookiejar)
opener = request.build_opener(handler)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
req = request.Request('http://httpbin.org/cookies',headers=headers)
resp = opener.open(req)
print(resp.read())
cookiejar.save(ignore_discard=True,ignore_expires=True)
```

#### **`3.11`从本地加载cookie：**

从本地加载`cookie`，需要使用`cookiejar`的`load`方法，并且也需要指定方法：

```python
from urllib import request
from http.cookiejar import MozillaCookieJar

cookiejar = MozillaCookieJar("cookie.txt")
cookiejar.load(ignore_expires=True,ignore_discard=True)
handler = request.HTTPCookieProcessor(cookiejar)
opener = request.build_opener(handler)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}
req = request.Request('http://httpbin.org/cookies',headers=headers)

resp = opener.open(req)
print(resp.read())
```

### **==4-`requests`库==**

> 虽然Python的标准库中 urllib模块已经包含了平常我们使用的大多数功能，但是它的 API 使用起来让人感觉不太好，而 Requests宣传是 “HTTP for Humans”，说明使用更简洁方便。
>

#### `4.1`**安装和文档地址：**

利用`pip`可以非常方便的安装：

```python
pip install requests
```

中文文档：http://docs.python-requests.org/zh_CN/latest/index.html
github地址：https://github.com/requests/requests

#### `4.2`**发送GET请求：**

1. 最简单的发送`get`请求就是通过`requests.get`来调用:

   ```python
   response = requests.get("http://www.baidu.com/")
   ```

2. 添加headers和查询参数：
    如果想添加 headers，可以传入headers参数来增加请求头中的headers信息。如果要将参数放在url中传递，可以利用 params 参数。相关示例代码如下：

  ```python
  import requests
  
   kw = {'wd':'中国'}
  
   headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
  
   # params 接收一个字典或者字符串的查询参数，字典类型自动转换为url编码，不需要urlencode()
   response = requests.get("http://www.baidu.com/s", params = kw, headers = headers)
  
   # 查看响应内容，response.text 返回的是Unicode格式的数据
   print(response.text)
  
   # 查看响应内容，response.content返回的字节流数据
   print(response.content)
  
   # 查看完整url地址
   print(response.url)
  
   # 查看响应头部字符编码
   print(response.encoding)
  
   # 查看响应码
   print(response.status_code)
  ```

  #### `4.3`**发送POST请求：**

  1. 最基本的POST请求可以使用`post`方法：

     ```python
     response = requests.post("http://www.baidu.com/",data=data)
     ```

2. 传入data数据：
   这时候就不要再使用`urlencode`进行编码了，直接传入一个字典进去就可以了。比如请求拉勾网的数据的代码:

   ```python
   import requests
   
    url = "https://www.lagou.com/jobs/positionAjax.json?city=%E6%B7%B1%E5%9C%B3&needAddtionalResult=false&isSchoolJob=0"
   
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
    }
   
    data = {
        'first': 'true',
        'pn': 1,
        'kd': 'python'
    }
   
    resp = requests.post(url,headers=headers,data=data)
    # 如果是json数据，直接可以调用json方法
    print(resp.json())
   ```

#### `4.4`**使用代理：**

使用`requests`添加代理也非常简单，只要在请求的方法中（比如`get`或者`post`）传递`proxies`参数就可以了。示例代码如下：

```python
import requests

url = "http://httpbin.org/get"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

proxy = {
    'http': '171.14.209.180:27829'
}

resp = requests.get(url,headers=headers,proxies=proxy)
with open('xx.html','w',encoding='utf-8') as fp:
    fp.write(resp.text)
```

#### `4.5`**Cookie:**

如果在一个响应中包含了`cookie`，那么可以利用`cookies`属性拿到这个返回的`cookie`值：

```python
import requests

url = "http://www.renren.com/PLogin.do"
data = {"email":"970138074@qq.com",'password':"pythonspider"}
resp = requests.get('http://www.baidu.com/')
print(resp.cookies)
print(resp.cookies.get_dict())
```

#### `4.6` **Session**：

之前使用`urllib`库，是可以使用`opener`发送多个请求，多个请求之间是可以共享`cookie`的。那么如果使用`requests`，也要达到共享`cookie`的目的，那么可以使用`requests`库给我们提供的`session`对象。注意，这里的`session`不是web开发中的那个session，这个地方只是一个会话的对象而已。还是以登录人人网为例，使用`requests`来实现。示例代码如下：

```python
import requests

url = "http://www.renren.com/PLogin.do"
data = {"email":"970138074@qq.com",'password':"pythonspider"}
headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
}

# 登录
session = requests.session()
session.post(url,data=data,headers=headers)

# 访问大鹏个人中心
resp = session.get('http://www.renren.com/880151247/profile')

print(resp.text)
```

#### `4.7`**处理不信任的SSL证书：**

对于那些已经被信任的SSL整数的网站，比如`https://www.baidu.com/`，那么使用`requests`直接就可以正常的返回响应（`verify`）。示例代码如下：

```python
resp = requests.get('http://www.12306.cn/mormhweb/',verify=False)
print(resp.content.decode('utf-8'))
```



## 第二章 数据提取

### **==1-`xpath`语法于`xlml`库==**

#### `1.1`什么是`XPath`？

`xpath`（`XML Path Language`）是一门在`XML`和`HTML`文档中查找信息的语言，可用来在`XML`和`HTML`文档中对元素和属性进行遍历。

#### `1.2 XPath`开发工具：

1. `Chrome`插件`XPath` `Helper`.
2. `Firefox`插件`Try` `XPath`.

#### `1.3` `XPath`语法：

1. 选取节点：

   XPath 使用路径表达式来选取 XML 文档中的节点或者节点集。这些路径表达式和我们在常规的电脑文件系统中看到的表达式非常相似。

   | 表达式   | 描述                                                         | 示例           | 结果                            |
   | :------- | :----------------------------------------------------------- | -------------- | ------------------------------- |
   | nodename | 选取此节点的所有子节点                                       | bookstore      | 选取bookstore下所有的子节点     |
   | /        | 如果是在最前面，代表从根节点选取。否则选择某节点下的某个节点 | /bookstore     | 选取根元素下所有的bookstore节点 |
   | //       | 从全局节点中选择节点，随便在哪个位置                         | //book         | 从全局节点中找到所有的book节点  |
   | @        | 选取某个节点的属性                                           | //book[@price] | 选择所有拥有price属性的book节点 |
   | .        | 当前节点                                                     | ./a            | 选取当前节点下的a标签           |

2. 谓语：

   谓语用来查找某个特定的节点或者包含某个指定的值的节点，被嵌在方括号中。
   在下面的表格中，我们列出了带有谓语的一些路径表达式，以及表达式的结果：

   | 路径表达式                   | 描述                                  |
   | ---------------------------- | ------------------------------------- |
   | /bookstore/book[1]           | 选取bookstore下的第一个子元素         |
   | /bookstore/book[last()]      | 选取bookstore下的倒数第二个book元素。 |
   | bookstore/book[position()<3] | 选取bookstore下前面两个子元素。       |
   | //book[@price]               | 选取拥有price属性的book元素           |
   | //book[@price=10]            | 选取所有属性price等于10的book元素     |

3. 通配符：

   `*`表示通配符：

   | 通配符 | 描述                 | 示例         | 结果                          |
   | :----- | :------------------- | :----------- | :---------------------------- |
   | *      | 匹配任意节点         | /bookstore/* | 选取bookstore下的所有子元素。 |
   | @*     | 匹配节点中的任何属性 | //book[@*]   | 选取所有带有属性的book元素。  |

4. 选取多个路径：

   通过在路径表达式中使用“|”运算符，可以选取若干个路径。
   示例如下：

   ```python
   //bookstore/book | //book/title
   # 选取所有book元素以及book元素下所有的title元素
   ```

#### `1.4` `lxml`库：

> `lxml` 是 一个`HTML/XML`的解析器，主要的功能是如何解析和提取 `HTML/XML` 数据。
> `lxml`和正则一样，也是用 C 实现的，是一款高性能的 `Python HTML/XML` 解析器，我们可以利用之前学习的`XPath`语法，来快速的定位特定元素以及节点信息。
> `lxml python` 官方文档：http://lxml.de/index.html
> 需要安装C语言库，可使用 `pip` 安装：`pip install lxml`

1. 基本使用：

   我们可以利用他来解析HTML代码，并且在解析HTML代码的时候，如果HTML代码不规范，他会自动的进行补全。示例代码如下：

   ```python
   # 使用 lxml 的 etree 库
   from lxml import etree 
   
   text = '''
   <div>
       <ul>
            <li class="item-0"><a href="link1.html">first item</a></li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-inactive"><a href="link3.html">third item</a></li>
            <li class="item-1"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a> # 注意，此处缺少一个 </li> 闭合标签
        </ul>
    </div>
   '''
   
   #利用etree.HTML，将字符串解析为HTML文档
   html = etree.HTML(text) 
   
   # 按字符串序列化HTML文档
   result = etree.tostring(html) 
   
   print(result)
   ```

   输入结果如下：

   ```python
   <html><body>
   <div>
       <ul>
            <li class="item-0"><a href="link1.html">first item</a></li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-inactive"><a href="link3.html">third item</a></li>
            <li class="item-1"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
   </ul>
    </div>
   </body></html>
   ```

2. 从文件中读取`html`代码：

   除了直接使用字符串进行解析，lxml还支持从文件中读取内容。我们新建一个hello.html文件：

   ```html
   <!-- hello.html -->
   <div>
       <ul>
            <li class="item-0"><a href="link1.html">first item</a></li>
            <li class="item-1"><a href="link2.html">second item</a></li>
            <li class="item-inactive"><a href="link3.html"><span class="bold">third item</span></a></li>
            <li class="item-1"><a href="link4.html">fourth item</a></li>
            <li class="item-0"><a href="link5.html">fifth item</a></li>
        </ul>
    </div>
   ```

   然后利用`etree.parse()`方法来读取文件。示例代码如下：

   ```python
   from lxml import etree
   
   # 读取外部文件 hello.html
   html = etree.parse('hello.html')
   result = etree.tostring(html, pretty_print=True)
   
   print(result)
   ```

   输入结果和之前是相同的。

3. 在`lxml`中使用`XPath`语法：

   1. 获取所有li标签：

      ```python
       from lxml import etree
      
       html = etree.parse('hello.html')
       print type(html)  # 显示etree.parse() 返回类型
      
       result = html.xpath('//li')
      
       print(result)  # 打印<li>标签的元素集合
      ```

   2. 获取所有`li`元素下的所有`class`属性的值：

      ```python
      from lxml import etree
      
       html = etree.parse('hello.html')
       result = html.xpath('//li/@class')
      
       print(result)
      ```

   3. 获取`li`标签下`href`为`www.baidu.com`的`a`标签：

      ```python
       from lxml import etree
      
       html = etree.parse('hello.html')
       result = html.xpath('//li/a[@href="www.baidu.com"]')
      
       print(result)
      ```

   4. 获取li标签下所有`span`标签：

      ```python
      from lxml import etree
      
       html = etree.parse('hello.html')
      
       #result = html.xpath('//li/span')
       #注意这么写是不对的：
       #因为 / 是用来获取子元素的，而 <span> 并不是 <li> 的子元素，所以，要用双斜杠
      
       result = html.xpath('//li//span')
      
       print(result)
      ```

   5. 获取`li`标签下的`a`标签里的所有`class`：

      ```python
      from lxml import etree
      
       html = etree.parse('hello.html')
       result = html.xpath('//li/a//@class')
      
       print(result)
      ```

   6. 获取最后一个`li`的`a`的`href`属性对应的值：

      ```python
      from lxml import etree
      
       html = etree.parse('hello.html')
      
       result = html.xpath('//li[last()]/a/@href')
       # 谓语 [last()] 可以找到最后一个元素
      
       print(result)
      ```

   7. 获取倒数第二个`li`元素的内容：

      ```python
       from lxml import etree
      
       html = etree.parse('hello.html')
       result = html.xpath('//li[last()-1]/a')
      
       # text 方法可以获取元素内容
       print(result[0].text)
      ```

   8. 获取倒数第二个`li`元素的内容的第二种方式：

      ```python
      from lxml import etree
      
       html = etree.parse('hello.html')
       result = html.xpath('//li[last()-1]/a/text()')
      
       print(result)
      ```

#### `1.5` `chrome`相关问题：

在62版本中有一个bug，在页面302重定向的时候不能记录FormData数据。这个是这个版本的一个bug。详细见以下链接：https://stackoverflow.com/questions/34015735/http-post-payload-not-visible-in-chrome-debugger。
在金丝雀版本中已经解决了这个问题，可以下载这个版本继续，链接如下：https://www.google.com/chrome/browser/canary.html

### **==`2-BeautifulSoup4`库==**

> 和 lxml 一样，Beautiful Soup 也是一个HTML/XML的解析器，主要的功能也是如何解析和提取 HTML/XML 数据。
> lxml 只会局部遍历，而Beautiful Soup 是基于HTML DOM（Document Object Model）的，会载入整个文档，解析整个DOM树，因此时间和内存开销都会大很多，所以性能要低于lxml。
> BeautifulSoup 用来解析 HTML 比较简单，API非常人性化，支持CSS选择器、Python标准库中的HTML解析器，也支持 lxml 的 XML解析器。
> Beautiful Soup 3 目前已经停止开发，推荐现在的项目使用Beautiful Soup 4。

#### `2.1 BeautifulSoup4`库：

1. 安装：`pip install bs4`；
2. 中文文档：https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html

#### `2.2`几大解析工具对比：

| 解析工具      | 解析速度 | 使用难度 |
| ------------- | -------- | -------- |
| BeautifulSoup | 最慢     | 最简单   |
| lxml          | 快       | 简单     |
| 正则          | 最快     | 最难     |

#### `2.3`简单使用：

```python
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

#创建 Beautiful Soup 对象
# 使用lxml来进行解析
soup = BeautifulSoup(html,"lxml")

print(soup.prettify())
```

#### `2.4`四个常用的对象：

`Beautiful Soup`将复杂`HTML`文档转换成一个复杂的树形结构,每个节点都是`Python`对象,所有对象可以归纳为4种: 

1. `Tag`;
2. `NavigatableString` ;
3. `BeautifulSoup` ;
4. `Comment`

##### `2.4.1` `Tag`：

`Tag` 通俗点讲就是 `HTML` 中的一个个标签。示例代码如下：

```python
from bs4 import BeautifulSoup

html = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title" name="dromouse"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1"><!-- Elsie --></a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
"""

#创建 Beautiful Soup 对象
soup = BeautifulSoup(html,'lxml')


print soup.title
# <title>The Dormouse's story</title>

print soup.head
# <head><title>The Dormouse's story</title></head>

print soup.a
# <a class="sister" href="http://example.com/elsie" id="link1"><!-- Elsie --></a>

print soup.p
# <p class="title" name="dromouse"><b>The Dormouse's story</b></p>

print type(soup.p)
# <class 'bs4.element.Tag'>
```

```python
print soup.name
# [document] #soup 对象本身比较特殊，它的 name 即为 [document]

print soup.head.name
# head #对于其他内部标签，输出的值便为标签本身的名称

print soup.p.attrs
# {'class': ['title'], 'name': 'dromouse'}
# 在这里，我们把 p 标签的所有属性打印输出了出来，得到的类型是一个字典。

print soup.p['class'] # soup.p.get('class')
# ['title'] #还可以利用get方法，传入属性的名称，二者是等价的

soup.p['class'] = "newClass"
print soup.p # 可以对这些属性和内容等等进行修改
# <p class="newClass" name="dromouse"><b>The Dormouse's story</b></p>
```

##### `2.4.2` `NavigableString`：

如果拿到标签后，还想获取标签中的内容。那么可以通过`tag.string`获取标签中的文字。示例代码如下：

```python
print soup.p.string
# The Dormouse's story

print type(soup.p.string)
# <class 'bs4.element.NavigableString'>thon
```

##### `2.4.3` `BeautifulSoup`：

`BeautifulSoup` 对象表示的是一个文档的全部内容.大部分时候,可以把它当作 `Tag` 对象,它支持 遍历文档树 和 搜索文档树 中描述的大部分的方法.
因为 `BeautifulSoup` 对象并不是真正的`HTML`或`XML`的`tag`,所以它没有`name`和`attribute`属性.但有时查看它的 .`name` 属性是很方便的,所以 `BeautifulSoup` 对象包含了一个值为 “[`document`]” 的特殊属性 .`name`

```python
soup.name
# '[document]'
```

##### `2.4.4` Comment：

`Tag` , `NavigableString` , `BeautifulSoup` 几乎覆盖了`html`和`xml`中的所有内容,但是还有一些特殊对象.容易让人担心的内容是文档的注释部分:

```python
markup = "<b><!--Hey, buddy. Want to buy a used parser?--></b>"
soup = BeautifulSoup(markup)
comment = soup.b.string
type(comment)
# <class 'bs4.element.Comment'>
```

Comment 对象是一个特殊类型的 `NavigableString` 对象:

```python
comment
# 'Hey, buddy. Want to buy a used parser'
```

#### `2.5` 遍历文档书：

1.  `contents`和`children`：

   ```python
   html_doc = """
   <html><head><title>The Dormouse's story</title></head>
   
   <p class="title"><b>The Dormouse's story</b></p>
   
   <p class="story">Once upon a time there were three little sisters; and their names were
   <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
   <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
   <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
   and they lived at the bottom of a well.</p>
   
   <p class="story">...</p>
   """
   
   from bs4 import BeautifulSoup
   soup = BeautifulSoup(html_doc,'lxml')
   
   head_tag = soup.head
   # 返回所有子节点的列表
   print(head_tag.contents)
   
   # 返回所有子节点的迭代器
   for child in head_tag.children:
       print(child)
   ```

2. `strings` 和 `stripped_strings`：

   如果tag中包含多个字符串 [2] ,可以使用 .strings 来循环获取：

   ```python
   for string in soup.strings:
       print(repr(string))
       # u"The Dormouse's story"
       # u'\n\n'
       # u"The Dormouse's story"
       # u'\n\n'
       # u'Once upon a time there were three little sisters; and their names were\n'
       # u'Elsie'
       # u',\n'
       # u'Lacie'
       # u' and\n'
       # u'Tillie'
       # u';\nand they lived at the bottom of a well.'
       # u'\n\n'
       # u'...'
       # u'\n'
   ```

   输出的字符串中可能包含了很多空格或空行,使用 .`stripped_strings` 可以去除多余空白内容：

   ```python
   for string in soup.stripped_strings:
       print(repr(string))
       # u"The Dormouse's story"
       # u"The Dormouse's story"
       # u'Once upon a time there were three little sisters; and their names were'
       # u'Elsie'
       # u','
       # u'Lacie'
       # u'and'
       # u'Tillie'
       # u';\nand they lived at the bottom of a well.'
       # u'...'
   ```

#### `2.6`搜索文档书：

##### `2.6.1` `find`方法`find_all`方法：

搜索文档树，一般用得比较多的就是两个方法，一个是`find`，一个是`find_all`。`find`方法是找到第一个满足条件的标签后就立即返回，只返回一个元素。`find_all`方法是把所有满足条件的标签都选到，然后返回回去。使用这两个方法，最常用的用法是出入`name`以及`attr`参数找出符合要求的标签。

```python
soup.find_all("a",attrs={"id":"link2"})
```

或者是直接传入属性的的名字作为关键字参数：

```python
soup.find_all("a",id='link2')
```

##### `2.6.2` `select`方法：

使用以上方法可以方便的找出元素。但有时候使用`css`选择器的方式可以更加的方便。使用`css`选择器的语法，应该使用`select`方法。以下列出几种常用的`css`选择器方法：

1. 通过标签名查找：

   ```python
   print(soup.select('a'))
   ```

2. 通过类名查找：

   通过类名，则应该在类的前面加一个`.`比如要查找`class=sister`的标签。示例代码如下：

   ```python
   print(soup.select('.sister'))
   ```

3. 通过id查找：

   通过id查找，应该在id的名字前面加一个＃号。示例代码如下：

   ```python
   print(soup.select("#link1"))
   ```

4. 组合查找：

   组合查找即和写 class 文件时，标签名与类名、id名进行的组合原理是一样的，例如查找 p 标签中，id 等于 link1的内容，二者需要用空格分开：

   ```python
   print(soup.select("p #link1"))
   ```

5. 通过属性查找：

   查找时还可以加入属性元素，属性需要用中括号括起来，注意属性和标签属于同一节点，所以中间不能加空格，否则会无法匹配到。示例代码如下：

   ```python
   print(soup.select('a[href="http://example.com/elsie"]'))
   ```

6. 获取内容：

   以上的 `select` 方法返回的结果都是列表形式，可以遍历形式输出，然后用 `get_text`() 方法来获取它的内容:

   ```python
   soup = BeautifulSoup(html, 'lxml')
   print type(soup.select('title'))
   print soup.select('title')[0].get_text()
   
   for title in soup.select('title'):
       print title.get_text()
   ```

### ==*`3-`正则表达式和`re`模块：*==

#### `3.1`什么是正则表达式：

通俗理解：按照一定的规则，从某个字符串中匹配出想要的数据。这个规则就是正则表达式。
标准答案：https://baike.baidu.com/item/正则表达式/1700215?fr=aladdin

#### `3.2` 正则表达式常用匹配规则：

##### `3.2.1` 匹配某个字符串：

```python
text = 'hello'
ret = re.match('he',text)
print(ret.group())
>> he
以上便可以在hello中，匹配出he。
```

##### `3.2.2` 点（.）匹配任意的字符：

```python
text = "ab"
ret = re.match('.',text)
print(ret.group())
>> a
但是点（.）不能匹配不到换行符。示例代码如下：
text = "ab"
ret = re.match('.',text)
print(ret.group())
>> AttributeError: 'NoneType' object has no attribute 'group'
```

##### `3.2.3` \d匹配任意的数字：

```python
text = "123"
ret = re.match('\d',text)
print(ret.group())
>> 1
```

##### `3.2.4` \D匹配任意的非数字：

```python
text = "a"
ret = re.match('\D',text)
print(ret.group())
>> a
```

##### `3.2.5` \s匹配的是空白字符（包括：\n，\t，\r和空格）：

```python
text = "\t"
ret = re.match('\s',text)
print(ret.group())
>> 空白
```

##### `3.2.6` \w匹配的是`a-z`和**`A-Z`**以及数字和下划线：

```python
text = "_"
ret = re.match('\w',text)
print(ret.group())
>> _
```

##### `3.2.7` \W匹配的是和\w相反的：

```python
text = "+"
ret = re.match('\W',text)
print(ret.group())
>> +
```

##### `3.2.8` [ ]组合的方式，只要满足中括号中的某一项都算匹配成功：

```python
text = "0731-88888888"
ret = re.match('[\d\-]+',text)
print(ret.group())
>> 0731-88888888
```

##### `3.2.9` 之前讲到的几种匹配规则，其实可以使用中括号的形式来进行替代：

- **\d：[0-9]**
- **\D：0-9**
- **\w：[0-9a-zA-Z_]**
- **\W：[^0-9a-zA-Z_**]

##### `3.2.10` 匹配多个字符：

###### `3.2.10.1` `*`：可以匹配0或者任意多个字符。示例代码如下：

```python
text = "0731"
 ret = re.match('\d*',text)
 print(ret.group())
 >> 0731
```

以上因为匹配的要求是`\d`，那么就要求是数字，后面跟了一个星号，就可以匹配到0731这四个字符。

###### `3.2.10.2` `+`：可以匹配1个或者多个字符。最少一个。示例代码如下：

```python
 text = "abc"
 ret = re.match('\w+',text)
 print(ret.group())
 >> abc
```

因为匹配的是`\w`，那么就要求是英文字符，后面跟了一个加号，意味着最少要有一个满足`\w`的字符才能够匹配到。如果text是一个空白字符或者是一个不满足\w的字符，那么就会报错。示例代码如下：

```python
 text = ""
 ret = re.match('\w+',text)
 print(ret.group())
 >> AttributeError: 'NoneType' object has no attribute
```

###### `3.2.10.3` `?`：匹配的字符可以出现一次或者不出现（0或者1）。示例代码如下：

```python
text = "123"
ret = re.match('\d?',text)
print(ret.group())
>> 1
```

###### `3.2.10.4` `{m}`：匹配m个字符。示例代码如下：

```python
text = "123"
ret = re.match('\d{2}',text)
print(ret.group())
>> 12
```

###### `3.2.10.5` `{m,n}`：匹配m-n个字符。在这中间的字符都可以匹配到。示例代码如下：

```python
text = "123"
ret = re.match('\d{1,2}',text)
prit(ret.group())
>> 12
```

如果text只有一个字符，那么也可以匹配出来。示例代码如下：

```python
text = "1"
ret = re.match('\d{1,2}',text)
prit(ret.group())
>> 1
```

###### `3.2.10.6` 小案例：

1. 验证手机号码：手机号码的规则是以`1`开头，第二位可以是`34587`，后面那9位就可以随意了。示例代码如下：

   ```python
   text = "18570631587"
    ret = re.match('1[34587]\d{9}',text)
    print(ret.group())
    >> 18570631587
   ```

   而如果是个不满足条件的手机号码。那么就匹配不到了。示例代码如下：

   ```python
    text = "1857063158"
    ret = re.match('1[34587]\d{9}',text)
    print(ret.group())
    >> AttributeError: 'NoneType' object has no attribute
   ```

2. 验证邮箱：邮箱的规则是邮箱名称是用`数字、数字、下划线`组成的，然后是`@`符号，后面就是域名了。示例代码如下：

   ```python
   text = "hynever@163.com"
    ret = re.match('\w+@\w+\.[a-zA-Z\.]+',text)
    print(ret.group())
   ```

3. 验证URL：URL的规则是前面是`http`或者`https`或者是`ftp`然后再加上一个冒号，再加上一个斜杠，再后面就是可以出现任意非空白字符了。示例代码如下：

   ```python
    text = "http://www.baidu.com/"
    ret = re.match('(http|https|ftp)://[^\s]+',text)
    print(ret.group())
   ```

4. 验证身份证：身份证的规则是，总共有18位，前面17位都是数字，后面一位可以是数字，也可以是小写的x，也可以是大写的X。示例代码如下：

   ```python
   text = "3113111890812323X"
    ret = re.match('\d{17}[\dxX]',text)
    print(ret.group())
   ```

###### `3.2.10.7` ^（脱字号）：表示以...开始：

```python
text = "hello"
ret = re.match('^h',text)
print(ret.group())
# 如果是在中括号中，那么代表的是取反操作.
```

###### `3.2.10.8` $：表示以...结束：

```python
# 匹配163.com的邮箱
text = "xxx@163.com"
ret = re.search('\w+@163\.com$',text)
print(ret.group())
>> xxx@163.com
```

###### `3.2.10.9` |：匹配多个表达式或者字符串：

```python
text = "hello|world"
ret = re.search('hello',text)
print(ret.group())
>> hello
```

###### `3.2.10.10` 贪婪模式和非贪婪模式：

```python
# 贪婪模式：正则表达式会匹配尽量多的字符。默认是贪婪模式。
# 非贪婪模式：正则表达式会尽量少的匹配字符。
# 示例代码如下：
text = "0123456"
ret = re.match('\d+',text)
print(ret.group())
# 因为默认采用贪婪模式，所以会输出0123456
>> 0123456


# 可以改成非贪婪模式，那么就只会匹配到0。示例代码如下
text = "0123456"
ret = re.match('\d+?',text)
print(ret.group())
```

###### `3.2.10.11` 案例：匹配**`0-100`**之间的数字：

```python
text = '99'
ret = re.match('[1-9]?\d$|100$',text)
print(ret.group())
>> 99
# 而如果text=101，那么就会抛出一个异常。示例代码如下：
text = '101'
ret = re.match('[1-9]?\d$|100$',text)
print(ret.group())
>> AttributeError: 'NoneType' object has no attribute 'group'
```

###### `3.2.10.12` 转义字符和原生字符串：

```python
# 在正则表达式中，有些字符是有特殊意义的字符。因此如果想要匹配这些字符，那么就必须使用反斜# # 杠进行转义。比如$代表的是以...结尾，如果想要匹配$，那么就必须使用\$。示例代码如下：
text = "apple price is \$99,orange paice is $88"
ret = re.search('\$(\d+)',text)
print(ret.group())
>> $99
# 原生字符串：
# 在正则表达式中，\是专门用来做转义的。在Python中\也是用来做转义的。因此如果想要在普通的字# 符串中匹配出\，那么要给出四个\。示例代码如下：
text = "apple \c"
ret = re.search('\\\\c',text)
print(ret.group())
# 因此要使用原生字符串就可以解决这个问题：
text = "apple \c"
ret = re.search(r'\\c',text)
print(ret.group())
```

#### `3.3 re`模块中常用函数：

##### `3.3.1` `match`:

从开始的位置进行匹配。如果开始的位置没有匹配到。就直接失败了。示例代码如下：

```python
text = 'hello'
ret = re.match('h',text)
print(ret.group())
>> h
```

如果第一个字母不是`h`，那么就会失败。示例代码如下

```python
text = 'ahello'
ret = re.match('h',text)
print(ret.group())
>> AttributeError: 'NoneType' object has no attribute 'group'
```

如果想要匹配换行的数据，那么就要传入一个`flag=re.DOTALL`，就可以匹配换行符了。示例代码如下：

```python
text = "abc\nabc"
ret = re.match('abc.*abc',text,re.DOTALL)
print(ret.group())
```

##### `3.3.2` `search`:

在字符串中找满足条件的字符。如果找到，就返回。说白了，就是只会找到第一个满足条件的。

```python
text = 'apple price $99 orange price $88'
ret = re.search('\d+',text)
print(ret.group())
>> 99
```

##### `3.3.3` 分组:

在正则表达式中，可以对过滤到的字符串进行分组。分组使用圆括号的方式。 

1. `group`：和`group(0)`是等价的，返回的是整个满足条件的字符串。  

2. `groups`：返回的是里面的子组。索引从1开始。  

3. `group(1)`：返回的是第一个子组，可以传入多个。

   ```python
   示例代码如下：
   text = "apple price is $99,orange price is $10"
   ret = re.search(r".*(\$\d+).*(\$\d+)",text)
   print(ret.group())
   print(ret.group(0))
   print(ret.group(1))
   print(ret.group(2))
   print(ret.groups())
   ```

##### `3.3.4` `findall`:

找出所有满足条件的，返回的是一个列表。

```python
text = 'apple price $99 orange price $88'
ret = re.findall('\d+',text)
print(ret)
>> ['99', '88']
```

##### `3.3.5` `sub`:

用来替换字符串。将匹配到的字符串替换为其他字符串。

```python
text = 'apple price $99 orange price $88'
ret = re.sub('\d+','0',text)
print(ret)
>> apple price $0 orange price $0
```

`sub`函数的案例，获取拉勾网中的数据：

```python
html = """
<div>
<p>基本要求：</p>
<p>1、精通HTML5、CSS3、 JavaScript等Web前端开发技术，对html5页面适配充分了解，熟悉不同浏览器间的差异，熟练写出兼容各种浏览器的代码；</p>
<p>2、熟悉运用常见JS开发框架，如JQuery、vue、angular，能快速高效实现各种交互效果；</p>
<p>3、熟悉编写能够自动适应HTML5界面，能让网页格式自动适应各款各大小的手机；</p>
<p>4、利用HTML5相关技术开发移动平台、PC终端的前端页面，实现HTML5模板化；</p>
<p>5、熟悉手机端和PC端web实现的差异，有移动平台web前端开发经验，了解移动互联网产品和行业，有在Android,iOS等平台下HTML5+CSS+JavaScript（或移动JS框架）开发经验者优先考虑；6、良好的沟通能力和团队协作精神，对移动互联网行业有浓厚兴趣，有较强的研究能力和学习能力；</p>
<p>7、能够承担公司前端培训工作，对公司各业务线的前端（HTML5\CSS3）工作进行支撑和指导。</p>
<p><br></p>
<p>岗位职责：</p>
<p>1、利用html5及相关技术开发移动平台、微信、APP等前端页面，各类交互的实现；</p>
<p>2、持续的优化前端体验和页面响应速度，并保证兼容性和执行效率；</p>
<p>3、根据产品需求，分析并给出最优的页面前端结构解决方案；</p>
<p>4、协助后台及客户端开发人员完成功能开发和调试；</p>
<p>5、移动端主流浏览器的适配、移动端界面自适应研发。</p>
</div>
"""

ret = re.sub('</?[a-zA-Z0-9]+>',"",html)
print(ret)
```

##### `3.3.6` `split`:

使用正则表达式来分割字符串。

```python
text = "hello world ni hao"
ret = re.split('\W',text)
print(ret)
>> ["hello","world","ni","hao"]
```

##### `3.3.7` `compile`:

对于一些经常要用到的正则表达式，可以使用`compile`进行编译，后期再使用的时候可以直接拿过来用，执行效率会更快。而且`compile`还可以指定`flag=re.VERBOSE`，在写正则表达式的时候可以做好注释。示例代码如下：

```python
text = "the number is 20.50"
r = re.compile(r"""
                \d+ # 小数点前面的数字
                \.? # 小数点
                \d* # 小数点后面的数字
                """,re.VERBOSE)
ret = re.search(r,text)
print(ret.group())
```

## 第三章 数据存储

###  **==`1-` `json`文件处理==**

#### `1.1` 什么是`json`:

JSON(JavaScript Object Notation, JS 对象标记) 是一种轻量级的数据交换格式。它基于 ECMAScript (w3c制定的js规范)的一个子集，采用完全独立于编程语言的文本格式来存储和表示数据。简洁和清晰的层次结构使得 JSON 成为理想的数据交换语言。 易于人阅读和编写，同时也易于机器解析和生成，并有效地提升网络传输效率。更多解释请见：https://baike.baidu.com/item/JSON/2462549?fr=aladdin

#### `1.2` `Json`支持数据格式：

1. 对象（字典）。使用花括号。
2. 数组（列表）。使用方括号。
3. 整形、浮点型、布尔类型还有null类型。
4. 字符串类型（字符串必须要用双引号，不能用单引号）。
5. 多个数据之间使用逗号分开。
6. **注意：json本质上就是一个字符串。**

#### `1.3` 字典列表转`JSON`：

```python
import json

books = [
    {
        'title': '钢铁是怎样练成的',
        'price': 9.8
    },
    {
        'title': '红楼梦',
        'price': 9.9
    }
]

json_str = json.dumps(books,ensure_ascii=False)
print(json_str)
```

因为json在dump的时候，只能存放ascii的字符，因此会将中文进行转义，这时候我们可以使用ensure_ascii=False关闭这个特性。
在Python中。只有基本数据类型才能转换成JSON格式的字符串。也即：int、float、str、list、dict、tuple。

#### `1.4` 将`json`数据直接`dump`到文件中：

`json`模块中除了`dumps`函数，还有一个`dump`函数，这个函数可以传入一个文件指针，直接将字符串`dump`到文件中。示例代码如下：

```python
books = [
    {
        'title': '钢铁是怎样练成的',
        'price': 9.8
    },
    {
        'title': '红楼梦',
        'price': 9.9
    }
]
with open('a.json','w') as fp:
    json.dump(books,fp)
```

#### `1.5` 将一个`json`字符串`load`成`python`对象

```python
json_str = '[{"title": "钢铁是怎样练成的", "price": 9.8}, {"title": "红楼梦", "price": 9.9}]'
books = json.loads(json_str,encoding='utf-8')
print(type(books))
print(books)
```

#### `1.6` 直接从文件中读取`json`：

```python
import json
with open('a.json','r',encoding='utf-8') as fp:
    json_str = json.load(fp)
    print(json_str)
```

### **==2`-` `CSV` 文件处理==**

#### `2.1` 读取csv文件：

```python
import csv

with open('stock.csv','r') as fp:
    reader = csv.reader(fp)
    titles = next(reader)
    for x in reader:
        print(x)
```

这样操作，以后获取数据的时候，就要通过下表来获取数据。如果想要在获取数据的时候通过标题来获取。那么可以使用`DictReader`。示例代码如下：

```python
import csv

with open('stock.csv','r') as fp:
    reader = csv.DictReader(fp)
    for x in reader:
        print(x['turnoverVol'])
```

#### `2.2` 写入数据到`csv`文件中：

写入数据到csv文件，需要创建一个`writer`对象，主要用到两个方法。一个是`writerow`，这个是写入一行。一个是`writerows`，这个是写入多行。示例代码如下：

```python
import csv

headers = ['name','age','classroom']
values = [
    ('zhiliao',18,'111'),
    ('wena',20,'222'),
    ('bbc',21,'111')
]
with open('test.csv','w',newline='') as fp:
    writer = csv.writer(fp)
    writer.writerow(headers)
    writer.writerows(values)
```

也可以使用字典的方式把数据写入进去。这时候就需要使用`DictWriter`了。示例代码如下：

```python
import csv

headers = ['name','age','classroom']
values = [
    {"name":'wenn',"age":20,"classroom":'222'},
    {"name":'abc',"age":30,"classroom":'333'}
]
with open('test.csv','w',newline='') as fp:
    writer = csv.DictWriter(fp,headers)
    writer = csv.writeheader()
    writer.writerow({'name':'zhiliao',"age":18,"classroom":'111'})
    writer.writerows(values)
```

### **==`3-` `MySql`数据库==**

#### `3.1` 安装`Mysql`:

1. 在官网：https://dev.mysql.com/downloads/windows/installer/5.7.html
2. 如果提示没有`.NET Framework`框架。那么就在提示框中找到下载链接，下载一个就可以了。
3. 如果提示没有`Microsoft Virtual C++ x64(x86)`，那么百度或者谷歌这个软件安装即可。
4. 如果没有找到。那么私聊我。

#### `3.2` `navicat`：

navicat是一个操作mysql数据库非常方便的软件。使用他操作数据库，就跟使用excel操作数据是一样的。

#### `3.3` 安装驱动程序：

Python要想操作MySQL。必须要有一个中间件，或者叫做驱动程序。驱动程序有很多。比如有`mysqldb`、`mysqlclient`、`pymysql`等。在这里，我们选择用`pymysql`。安装方式也是非常简单，通过命令`pip install pymysql`即可安装。

#### `3.4` 数据库连接：

数据库连接之前。首先先确认以下工作完成，这里我们以一个`pymysql_test`数据库.以下将介绍连接`mysql`的示例代码

```python
 import pymysql

    db = pymysql.connect(
        host="127.0.0.1",
        user='root',
        password='root',
        database='pymysql_test',
        port=3306
    )
    cursor = db.cursor()
    cursor.execute("select 1")
    data = cursor.fetchone()
    print(data)
    db.close()
```

#### `3.5` 插入数据：

```python
import pymysql

db = pymysql.connect(
    host="127.0.0.1",
    user='root',
    password='root',
    database='pymysql_test',
    port=3306
)
cursor = db.cursor()
sql = """
insert into user(
    id,username,gender,age,password
  ) 
  values(null,'abc',1,18,'111111');
"""
cursor.execute(sql)
db.commit()
db.close()
```



如果在数据还不能保证的情况下，可以使用以下方式来插入数据：

```python
sql = """
insert into user(
    id,username,gender,age,password
  ) 
  values(null,%s,%s,%s,%s);
"""

cursor.execute(sql,('spider',1,20,'222222'))
```

#### `3.6` 查找数据：

使用`pymysql`查询数据。可以使用`fetch*`方法。  

1. `fetchone()`：这个方法每次之获取一条数据。  
2. `fetchall()`：这个方法接收全部的返回结果。  
3. `fetchmany(size)`：可以获取指定条数的数据。
   示例代码如下：

```python
cursor = db.cursor()

sql = """
select * from user
"""

cursor.execute(sql)
while True:
    result = cursor.fetchone()
    if not result:
        break
    print(result)
db.close()
```

或者是直接使用`fetchall`，一次性可以把所有满足条件的数据都取出来：

```python
cursor = db.cursor()

sql = """
select * from user
"""

cursor.execute(sql)
results = cursor.fetchall()
for result in results:
    print(result)
db.close()
```

或者是使用`fetchmany`，指定获取多少条数据：

```python
cursor = db.cursor()

sql = """
select * from user
"""

cursor.execute(sql)
results = cursor.fetchmany(1)
for result in results:
    print(result)
db.close()
```

#### `3.7` 删除数据

```pythoN
cursor = db.cursor()

sql = """
delete from user where id=1
"""

cursor.execute(sql)
db.commit()
db.close()
```

#### `3.8` 更新数据：

```pythoN
conn = pymysql.connect(host='localhost',user='root',password='root',database='pymysql_demo',port=3306)
cursor = conn.cursor()

sql = """
update user set username='aaa' where id=1
"""
cursor.execute(sql)
conn.commit()

conn.close()
```

## 第四章 爬虫进阶

### ==**`1-` 多线程爬虫**==

