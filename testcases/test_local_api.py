import requests
import sqlite3


def test_create_order_and_check_db():
    # 1. 先查一下现在的库存
    conn = sqlite3.connect('mock_server/ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT stock FROM products WHERE id = "1001"')
    before_stock = cursor.fetchone()[0]
    conn.close()

    # 2. 调用真实下单接口
    url = "http://127.0.0.1:5000/api/orders/create"
    res = requests.post(url)
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