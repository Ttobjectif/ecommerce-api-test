import pytest
import logging
import allure
from ruamel.yaml import YAML
from api.order_api import HttpBinApi
from common.logger import log
from common.db_util import query_db

api = HttpBinApi()


def load_test_data():
    yaml = YAML()
    with open("./data/test_data.yaml", "r", encoding="utf-8") as f:
        return yaml.load(f)


@allure.feature("电商业务测试")
@allure.story("测试 HttpBin 接口")
@pytest.mark.parametrize("data", load_test_data())
def test_get_request(data):
    allure.dynamic.title(f"测试用户: {data['name']} - 动作: {data['action']}")
    allure.attach(str(data), name="请求参数", attachment_type=allure.attachment_type.TEXT)

    # 调用封装好的方法，只传 params
    response = api.get_request(params=data)

    assert response.status_code == 200, f"请求失败，状态码: {response.status_code}，响应内容: {response.text}"
    assert response.json()["args"]["name"] == data["name"]


@allure.feature("电商核心链路")
@allure.story("接口依赖：查商品 -> 购物车")
def test_business_flow(get_token):
    logging.info("---第一步：查询商品---")
    search_params = {"keyword": "iphon"}
    search_res = api.get_request(params=search_params)
    assert search_res.status_code == 200

    item_id = "10086"
    log.info(f"提取到商品id: {item_id}")

    log.info("---第二步：加入购物车---")
    cart_res = api.post_login(username="buy_01", password=f"buy_{item_id}")
    assert cart_res.status_code == 200
    assert "10086" in cart_res.json()["json"]["password"]
    log.info("---链路测试通过---")

    log.info("--- 第三步：查数据库验证 ---")
    sql = "SELECT status FROM orders WHERE item_id = '10086'"
    db_result = query_db(sql)
    assert db_result[0][0] == 'PAID'
    log.info("--- 数据库校验通过，订单状态为已支付 ---")
