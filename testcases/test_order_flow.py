import pytest
import allure
from ruamel.yaml import YAML
from api.order_api import EcommerceApi

api = EcommerceApi()


def load_test_data():
    yaml = YAML()
    with open("./data/test_data.yaml", "r", encoding="utf-8") as f:
        return yaml.load(f)


@allure.feature("电商业务基础链路")
@allure.story("数据驱动：查询真实商品详情")
@pytest.mark.parametrize("data", load_test_data())
def test_get_product(data):
    # 从 YAML 中取出商品 ID
    product_id = data["product_id"]

    # 调用封装好的查询方法
    res = api.get_product(product_id)

    # 如果预期是 iPhone，说明是正常商品
    if data["expected_name"] == "iPhone":
        assert res.status_code == 200
        assert res.json()["name"] == data["expected_name"]
        print(f"查询正常商品 {product_id} 成功")

    # 如果预期是 not_found，说明查的是不存在的商品
    else:
        assert res.status_code == 404
        assert res.json()["msg"] == "not found"
        print(f"查询异常商品 {product_id} 拦截成功")