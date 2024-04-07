import logging
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

LOG_FORMAT = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.WARNING, format=LOG_FORMAT, encoding='utf-8')

from feishu_logging.handler import FeiShuWebhookHandler
log_feishu = logging.getLogger("feishu")
url = os.environ["feishu_url"]
http_handler = FeiShuWebhookHandler(url,"goods_system")
http_handler.setLevel(logging.DEBUG)
log_feishu.addHandler(http_handler)


log_feishu.error("错误测试")
import time
time.sleep(5)