import requests
import configparser
from common.logger import log


class EcommerceApi:
    def __init__(self):
        # 1. 实例化一个配置解析器
        self.config = configparser.ConfigParser()
        # 2. 读取刚刚建好的 config.ini 文件
        self.config.read("./config.ini", encoding="utf-8")
        # 3. 从配置文件的 [env] 节点下，把 base_url 读出来
        self.base_url = self.config.get("env", "base_url")
        # 预留放 Token
        self.headers = {}

    def login(self):
        """去后端拿 Token"""
        url = f"{self.base_url}/api/login"
        response = requests.post(url, timeout=5, proxies={"http": None, "https": None})
        return response

    def create_order(self):
        """调用真实的本地下单接口"""
        url = f"{self.base_url}/api/orders/create"
        log.info(f"发起真实下单请求，URL: {url}")
        response = requests.post(url, timeout=5, headers=self.headers, proxies={"http": None, "https": None})
        log.info(f"下单响应结果，状态码: {response.status_code}, 内容: {response.text}")
        return response

    def get_product(self, product_id="1001"):
        """调用本地查询商品接口"""
        url = f"{self.base_url}/api/products/{product_id}"
        log.info(f"查询商品信息，ID: {product_id}")
        response = requests.get(url, timeout=5, proxies={"http": None, "https": None})
        log.info(f"查询商品响应: {response.text}")
        return response
