import pytest
from api.order_api import EcommerceApi
from common.logger import log

api = EcommerceApi


@pytest.fixture(scope="session")
def get_token():
    log.info("========== 开始执行全局登录操作 ==========")
    api = EcommerceApi()

    # 调用登录接口
    res = api.login()
    assert res.status_code == 200

    # 提取 token
    token = res.json()["token"]

    log.info(f"========== 登录成功，获取到 Token: {token} ==========")
    return token