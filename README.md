# feishu-logging-handler
通过webhook将自定义服务的消息推送至飞书

特点：
- 支持异步，不需要等待http请求提高性能

# 安装
pip install feishu-logging-handler

# 配置
- 创建一个飞书群组
- 点击群设置，添加一个机器人，并生成Webhook地址
- 可以设置关键词过滤


# 使用方式
初始化：
```
from feishu_logging.handler import FeiShuWebhookHandler
log_feishu = logging.getLogger("feishu")
http_handler = FeiShuWebhookHandler("https://open.feishu.cn/open-apis/bot/v2/hook/xxx","key_word")
http_handler.setLevel(logging.DEBUG)
log_feishu.addHandler(http_handler)
```

写日志:
```
log_feishu = logging.getLogger("feishu")
log_feishu.error("错误测试")
```

填入Webhook地址和关键词（或项目名称）即可
