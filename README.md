# 支付宝爬虫(Scrapy版本)

---

<h3 id="Q&A">问题反馈</h3>
在使用中有任何问题，可以反馈给我，以下联系方式跟我交流

* Author: Leo
* Wechat: Leo-sunhailin 
* E-mail: 379978424@qq.com 
* Github URL: [项目链接]()

---

* 目录
    * [目前的进度](#Now)
    * [开发环境](#DevelopEnv)
    * [安装方式](#HowToInstall)
    * [功能](#Function)
    * [技术点](#TechPoints)
    * [题外话](#FreeChat)
    * [未来的进度](#Future)

---

<h3 id="Now">目前的进度</h3>

* 2017年10月 参加DoraHacks时:

    * 当时能够获取到账单和账户信息.

* 大概在2017年11月~12月的样子：
    
    * 开始出现跳出验证码页面了.原因应该是支付宝反爬的模型增强了.
    
    * 这段时间维护时间不多,都是个人测试没有更新代码上去

* 2018年1月:
    
    * 将更新提上日程,在测试二维码登录.先上个半成品
    
    * 原先密码登陆的现在基本上不能用了.因为个人页面多了一种反爬手段,其次就是跳出二维码页面.

    * 上面这些问题,将在之后尽量解决.


---

<h3 id="DevelopEnv">开发环境</h3>

* 系统版本：Win10 x64

* Python版本：3.4.4
    
    * Python库版本列表:
     
        * Pillow: 5.0.0
    
        * Scrapy：1.4.0
        
        * selenium：3.8.1
        
        * requests：2.18.4
        
        * pymongo：3.6.0
        
        * python_dateutil：2.6.1

* Ps: 一定要配好Python的环境,不然Scrapy的命令可能会跑不起来
* 
---

<h3 id="DevelopEnv">安装和运行方式</h3>
* 安装库

```Python
    # 项目根目录下,打开命令行
    pip install -r requirements.txt
```

* 启动

```Python
    # 项目根目录下,启动爬虫
    scrapy crawl AlipaySpider -a username="你的用户名" -a password="你的密码"
    
    # 必选参数
    -a username=<账号>
    -a password=<密码>
    
    # 可选参数
    -a option=<爬取类型>
    # 1 -> 购物; 2 -> 线下; 3 -> 还款; 4 -> 缴费
    # 这里面有四种类型数据对应四种不同的购物清单
    
    #####################################################
    # 实验版本
    scrapy crawl AlipayQR
    
    # 暂时还没有参数, 能登陆到个人页面了.
```

---

<h3 id="Function">功能</h3>

1. 模拟登录支付宝(账号密码和二位都可以登陆)
2. 获取自定义账单记录和花呗剩余额度(2017年10月份的时候个人页面还有花呗总额度的,后面改版没有了.再之后又出现了,应该是支付宝内部在做调整)
3. 数据存储在MongoDB中(暂时存储在MongoDB,后续支持sqlite,json或其他格式的数据)
4. 日志记录系统,启动爬虫后会在项目根目录下创建一个Alipay.log的文件(同时写入文件和输出在控制台)

---

<h3 id="TechPoints">技术点</h3>

吐槽一下: 这点可能没啥好说,因为代码是从自己之前写的用非框架的代码搬过来的,搬过来之后主要就是适应Scrapy这个框架,理解框架的意图和执行顺序以及项目的结构,然后进行兼容和测试。

我这个项目主要就用到Spider模块(即爬虫模块),Pipeline和item(即写数据的管道和实体类)

Downloader的那块基本没做处理,因为核心还是在用selenium + webdriver,解析页面用的是Scrapy封装好的Selector.

<strong>Scrapy具体的流程看下图: (从官方文档搬过来的)</strong>

![image](http://scrapy-chs.readthedocs.io/zh_CN/0.24/_images/scrapy_architecture.png)

---

<h3 id="FreeChat">题外话</h3>

题外话模块: 
    上一段讲到了一个Selector,这个是东西是Scrapy基于lxml开发的,但是真正用的时候其实和lxml的selector有点区别.
    
举个例子吧：
```Python
# 两段相同的标签获取下面的文字的方式
# lxml
name = str(tr.xpath('td[@class="name"]/p/a/text()').strip()

# Scrapy
name = tr.xpath('string(td[@class="name"]/p/a)').extract()[0].strip()
```
两行代码对同一个标签的文字提取的方法有些不一样,虽然到最后的结果一样。

lxml中有一个"string(.)"方法也是为了提取文字,但是这个方法是要在先指定了父节点或最小子节点后再使用,就可以获取父节点以下的所有文字或最小子节点对应的文字信息.

而Scrapy的Selector则可以在"string(.)"里面写入标签,方便定位,也很清晰的看出是要去获取文字信息.

具体区别其实可以对比下我非框架下的和Scrapy框架下的代码,里面用xpath定位的方式有点不一样.

1. selenium + lxml: [非框架](https://github.com/sunhailin-Leo/Alipay-Spider)
2. Scrapy + selenium: [Scrapy](https://github.com/sunhailin-Leo/AlipaySpider-Scrapy)

---

<h3 id="Future">未来的进度</h3>

1. 数据源保存的可选择性(从多源选择单源写入到多源写入)
2. 修改配置文件的自由度(增加修改settings.py的参数)
3. 尽可能优化爬虫的爬取速度
4. 研究Scrapy的自定义命令的写法,提高扩展性