# feishu-logging-handler
通过webhook将自定义服务的消息推送至飞书

## 更新记录
- 1.0.6 修复了bug、stack_info并且可以换行输出
- 1.0.5 增加stack_info的支持
- 1.0.5 增加了error不是str的支持(特别是try except的时候)


特点：
- 异步有可能会遇到loop已释放的问题，调整为同步。启用多线程，所以性能ok
- 增加缓存支持，重复消息设置一个时间周期，不会重复发送
- 支持 filter_key 来过滤部分error的key

# 安装
pip install feishu-logging-handler -i https://pypi.org/simple

# 配置
- 创建一个飞书群组
- 点击群设置，添加一个机器人，并生成Webhook地址
- 可以设置关键词过滤


# 使用方式
初始化：
```
from feishu_logging.handler import FeiShuWebhookHandler
log_feishu = logging.getLogger("feishu")
http_handler = FeiShuWebhookHandler("https://open.feishu.cn/open-apis/bot/v2/hook/xxx","key_word",cache_time=10,filter_key=["funcName","msg","levelname","args","pathname","lineno","threadName","stack_info"]) # cache_time = 0为不启用cache,cache_time单位为秒
http_handler.setLevel(logging.DEBUG)
log_feishu.addHandler(http_handler)
```

```
注意是否会初始化多次 addHandler 如果多次会请求多次
if not log_feishu.handlers:
    http_handler = FeiShuWebhookHandler("https://open.feishu.cn/open-apis/bot/v2/hook/xxx","key_word",cache_time=10,filter_key=["funcName","msg","levelname","args","pathname","lineno","threadName","stack_info"]) # cache_time = 0为不启用cache
    http_handler.setLevel(logging.DEBUG)
    log_feishu.addHandler(http_handler)
```

写日志:
```
log_feishu = logging.getLogger("feishu")
log_feishu.error("错误测试")
```

填入Webhook地址和关键词（或项目名称）即可
