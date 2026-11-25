import sqlite3
from api.order_api import EcommerceApi

api = EcommerceApi()

def test_create_order_and_check_db(get_token):
    from api.order_api import EcommerceApi
    api = EcommerceApi()
    api.headers = {"Authorization": f"Bearer {get_token}"}
    # 1. 先查一下现在的库存
    conn = sqlite3.connect('mock_server/ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stock FROM products WHERE id = "1001"')
    before_stock = cursor.fetchone()[0]
    conn.close()

    # 2. 调用真实下单接口
    res = api.create_order()
    assert res.status_code == 200

    # 3. 再查一下下单后的库存
    conn = sqlite3.connect('mock_server/ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stock FROM products WHERE id = "1001"')
    after_stock = cursor.fetchone()[0]
    conn.close()

    print(f"下单前库存: {before_stock}, 下单后库存: {after_stock}")

    # 4. 核心断言：下单后的库存，必须等于下单前的库存 - 1！
    assert after_stock == before_stock - 1


def test_oversell_prevention(get_token):
    from api.order_api import EcommerceApi
    api = EcommerceApi()
    api.headers = {"Authorization": f"Bearer {get_token}"}
    # 1. 强行改库存为 1
    conn = sqlite3.connect('mock_server/ecommerce.db', timeout=5)
    cursor = conn.cursor()
    try:
        cursor.execute('UPDATE products SET stock = 1 WHERE id = "1001"')
        conn.commit()
    finally:
        cursor.close()
        conn.close()

    # 2. 第一次下单（此时库存有1个）
    res1 = api.create_order()
    assert res1.status_code == 200
    assert res1.json()["code"] == 200  # 确认第一次下单业务成功
    print("第一次下单成功，库存应该变成0了")

    # 3. 第二次下单（此时库存已经是0）
    res2 = api.create_order()
    assert res2.status_code == 200  # HTTP状态码依然会是200

    # 断言：检查 JSON 里的业务 code 是不是 400
    res_json = res2.json()
    print(f"第二次下单的响应内容: {res_json}")

    assert res_json["code"] == 400
    assert res_json["msg"] == "库存不足，下单失败"