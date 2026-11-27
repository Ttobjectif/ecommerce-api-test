import pytest
from api.order_api import EcommerceApi
from common.db_util import query_db, execute_db


def test_create_order_and_check_db(get_token):
    api = EcommerceApi()
    api.headers = {"Authorization": f"Bearer {get_token}"}

    # 1. 查下单前库存
    before_res = query_db('SELECT stock FROM products WHERE id = "1001"')
    before_stock = before_res[0][0]
    print(f"下单前库存: {before_stock}")

    # 2. 调用真实下单接口
    res = api.create_order()
    assert res.status_code == 200

    # 3. 查下单后库存
    after_res = query_db('SELECT stock FROM products WHERE id = "1001"')
    after_stock = after_res[0][0]
    print(f"下单后库存: {after_stock}")

    # 4. 动态断言
    assert after_stock == before_stock - 1


def test_oversell_prevention(get_token):
    api = EcommerceApi()
    api.headers = {"Authorization": f"Bearer {get_token}"}

    # 1. 强行把库存改为 1
    execute_db('UPDATE products SET stock = 1 WHERE id = "1001"')

    # 2. 第一次下单（应该成功）
    res1 = api.create_order()
    assert res1.status_code == 200

    # 3. 第二次下单（应该被拦截）
    res2 = api.create_order()
    assert res2.json()["code"] == 400

    # 4. 查库验证
    result = query_db('SELECT stock FROM products WHERE id = "1001"')
    assert result[0][0] == 0