import pytest
from api.order_api import HttpBinApi
from common.logger import log

api = HttpBinApi()


@pytest.fixture(scope="session")
def get_token():
    log.info("========== 开始执行全局登录操作 ==========")
    # 调用登录接口
    response = api.post_login("admin", "123456")

    # 提取 token
    token = response.json()["json"]["username"]

    log.info(f"========== 登录成功，获取到 Token: {token} ==========")
    return token