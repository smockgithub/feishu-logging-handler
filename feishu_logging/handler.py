import logging
# import asyncio
from threading import Thread
import httpx
import json
import time
from cachetools import LRUCache, TTLCache
import base64

class FeiShuWebhookHandler(logging.Handler):
    """
    通过webhook将自定义服务的消息推送至飞书
    """
    connection = None
    cache = TTLCache(maxsize=1024,ttl=60)

    def __init__(self,webhook_url,key_word="feishu",cache_time=0,filter_key=[]):
        """初始化logger

        Args:
            webhook_url (_type_): 飞书机器人url
            key_word (str, optional): 关键词过滤. Defaults to "feishu".
            cache (int, optional): 同时间内同error不再重复推送，如果为0则每次都推送（too many request）. Defaults to 0.
        """
        logging.Handler.__init__(self)
        self.url = webhook_url
        self.key_word = key_word
        self.cache_time = cache_time
        if cache_time>0:
            self.cache = TTLCache(maxsize=1024,ttl=cache_time)
        self.filter_key = filter_key

    def mapLogRecord(self, record):
        """
        Default implementation of mapping the log record into a dict
        that is sent as the CGI data. Overwrite in your class.
        Contributed by Franz Glasner.
        """
        if self.filter_key:
            result = {}
            for key in self.filter_key:
                if key in record.__dict__:
                    result[key] = record.__dict__[key]
            return result
        else:
            return record.__dict__

    @classmethod
    def getConnection(cls):
        """
        get a HTTP[S]Connection.

        Override when a custom connection is required, for example if
        there is a proxy.
        """
        if not cls.connection:
            cls.connection = httpx.Client(default_encoding="utf-8")
        
        return cls.connection

    @staticmethod
    def post(connection:httpx.Client,url,payload_message):
        try:
            res = connection.post(url=url,json=payload_message)
            if res.status_code!=200:
                print("feishu logging handler error : {}".format(res.text))
        except Exception as e:
            print("feishu logging handler error : {}".format(e))
    
    @staticmethod
    def send(connection,url,payload_message):
        # asyncio.run(FeiShuWebhookHandler.post(connection,url,payload_message))
        FeiShuWebhookHandler.post(connection,url,payload_message)

    def emit(self, record):
        """
        Emit a record.
        """
        try:
            timeArray = time.localtime(int(record.created))
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            payload_message = {
                "msg_type": "text",
                "content": {
                    # @ 单个用户 <at user_id="ou_xxx">名字</at>
                    "text": "[{}] [{}] ".format(otherStyleTime,self.key_word) + "\r\n" + json.dumps(self.mapLogRecord(record),indent=1,ensure_ascii=False)
                    # @ 所有人 <at user_id="all">所有人</at>
                    # "text": content + "<at user_id=\"all\">test</at>"
                }
            }

            # 判断是否要推送
            if self.cache_time!=0:
                b = base64.b64encode(bytes(record.msg, 'utf-8')) # bytes
                base64_str = b.decode('utf-8') # convert bytes to string
                value = self.cache.get(base64_str)
                if value:
                    # print("feishu logger 命中缓存略过本条消息")
                    return
                else:
                    self.cache[base64_str] = base64_str

            connection = self.getConnection()
            url = self.url

            # asyncio.run(FeiShuWebhookHandler.post(connection,url,payload_message))
            # print("end 这里应该是最先出现的")

            t1 = Thread(target=FeiShuWebhookHandler.send, args=(connection,url,payload_message,))
            t1.start()
            # join() 等待线程终止，要不然一直挂起
            
        except Exception:
            self.handleError(record)
        
