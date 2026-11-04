import requests
import configparser
from common.logger import log


class HttpBinApi:
    def __init__(self):
        # 1. 实例化一个配置解析器
        self.config = configparser.ConfigParser()
        # 2. 读取刚刚建好的 config.ini 文件
        self.config.read("./config.ini", encoding="utf-8")
        # 3. 从配置文件的 [env] 节点下，把 base_url 读出来
        self.base_url = self.config.get("env", "base_url")

    def get_request(self, params):
        url = f"{self.base_url}/get"
        log.info(f"发送get请求：url: {url}，参数={params}")
        response = requests.get(url, params=params)
        log.info(f'收到响应：状态码={response.status_code},内容={response.text[100]}...')
        return response

    def post_login(self, username, password):
        url = f"{self.base_url}/post"
        payload = {"username": username, "password": password}
        log.info(f"发送 POST 请求登录: url={url}, 账号={username}")
        response = requests.post(url, json=payload)
        return response
