## 哔哩哔哩完结动画异步爬虫

### 一、 用到的包
- 异步库：
> aoihttp
> asyncio

- 数据处理库：
> pandas
> json
> xlswriter

- 其他：
> requests

主要用来获取代理，**这里的get_proxy()函数仍然是同步的**，可能发生的卡顿就是在获取代理的地方。

### 二、 各个函数的用途

#### 1. 代理相关

两个函数：分别是 **get_proxy()** 和**delete_proxy()** 函数。代码内置了 [jhao104](https://github.com/jhao104/proxy_pool) 在GitHub开源的动态代理池。安装完成后，先启动redis数据库，然后启动main函数即可。通过浏览器访问 [http://127.0.0.1:5010](http://127.0.0.1:5010)，配合相应请求方式可以获取到代理。代理的来源是网上的免费代理。

- get_proxy()函数

获取一个代理，这里采用的是requets库获取，返回text文本类型；

- delete_proxy()函数

删除一个代理，仍然是get方法。

#### 2. fetch()函数

- 采用async声明该函数是需要异步处理的函数；

- 用 while 1 封装（或者while True），保证每次拿到的代理都是可用的，如不可用则删除，再次获取，知道可以访问网页为止；
- 使用 async with 上下文管理器保证session的正常运行；

#### 3. get_html()和parse_html()

- 这两个函数用来获取html页面和解析；
- headers中需要指明 **referer**，必不可少；
- semaphore为信息量，控制并发线程数量；
- 通过aiohttp.ClientSession()建立异步客户端；
- 在异步处理过程中的sleep必须采用asyncio.sleep()函数；
- parse_html()函数中必须声明data为全局变量；
- 使用data+=info来拼接数据；

#### 4. 其他
- main函数中的代码均为协程的一般格式；
- data_save()函数中采用xlsxwriter引擎， *因为python引擎在存储时总是报错* ；

#### 5. 使用方式
- 下载源码：
> git clone git@github.com:Gjh9508/asyncbili.git
> 或者到 https://github.com/Gjh9508/asyncbili 下载源码
- 安装依赖：
> pip3 install -r requirements
- 启动程序：
> python3 asyncbili.py
