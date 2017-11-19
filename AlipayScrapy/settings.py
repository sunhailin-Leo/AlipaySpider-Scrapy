# -*- coding: utf-8 -*-

# Scrapy的名字
BOT_NAME = 'AlipayScrapy'

# 爬虫模块
SPIDER_MODULES = ['AlipayScrapy.spiders']
NEWSPIDER_MODULE = 'AlipayScrapy.spiders'

# MongoDB配置
# MONGODB 主机名
MONGODB_HOST = "127.0.0.1"
# MONGODB 端口号
MONGODB_PORT = 27017
# 数据库名称
MONGODB_DB_NAME = "Alipay_Scrapy"
# 存放数据的表名称
MONGODB_COLLECTION = "c_bill_info"

# LOG配置
LOG_FILE = "Alipay.log"
LOG_LEVEL = "DEBUG"
LOG_ENCODING = "UTF-8"

# Scrapy User-agent(用了selenium之后其实可以去掉的)
USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/55.0.2883.87 UBrowser/6.2.3637.220 Safari/537.36'

# 遵循robots.txt的规则(至于什么事robots.txt自行百度)
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
# CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 16
# CONCURRENT_REQUESTS_PER_IP = 16

# Cookies的开启(默认也是True)
COOKIES_ENABLED = True
COOKIES_DEBUG = True

# 关闭telnet 命令行
# TELNETCONSOLE_ENABLED = False

# 启动或关闭中间件
SPIDER_MIDDLEWARES = {
    # 'AlipayScrapy.middlewares.AlipayscrapySpiderMiddleware': 543,
    'scrapy.contrib.spidermiddleware.referer.RefererMiddleware': True
}

# 启动或关闭下载中间件
# DOWNLOADER_MIDDLEWARES = {
#    'AlipayScrapy.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# 配置管道
ITEM_PIPELINES = {
    'AlipayScrapy.pipelines.AlipayScrapyPipeline': 300
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# AUTOTHROTTLE_ENABLED = True
# The initial download delay
# AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED = True
# HTTPCACHE_EXPIRATION_SECS = 0
# HTTPCACHE_DIR = 'httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES = []
# HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
