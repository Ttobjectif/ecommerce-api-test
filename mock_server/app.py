from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 假装是真实的Token
FAKE_TOKEN = "admin_token_123"

# 初始化一个简单的SQLite数据库和商品表
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS products (id TEXT, name TEXT, stock INT)')
    # 初始插入一件库存为 10 的 iPhone
    cursor.execute('INSERT OR REPLACE INTO products VALUES ("1001", "iPhone", 10)')
    conn.commit()
    conn.close()


# 登录接口
@app.route('/api/login', methods=['POST'])
def login():
    # 无论谁登录，只要发了 POST，就给他发这个 Token
    return jsonify({"code": 200, "token": FAKE_TOKEN})

# 查询商品接口
@app.route('/api/products/<product_id>', methods=['GET'])
def get_product(product_id):
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify({"id": result[0], "name": result[1], "stock": result[2]})
    return jsonify({"msg": "not found"}), 404

# 下单接口
@app.route('/api/orders/create', methods=['POST'])
def create_order():
    auth_header = request.headers.get('Authorization')
    if auth_header != f"Bearer {FAKE_TOKEN}":
        return jsonify({"code": 401, "msg": "未授权，请先登录"}), 401
    conn = sqlite3.connect('ecommerce.db', timeout=5)
    cursor = conn.cursor()
    # 扣减库存
    try:
        # 扣减库存
        cursor.execute('UPDATE products SET stock = stock - 1 WHERE id = "1001" AND stock > 0')

        # 如果库存不足
        if cursor.rowcount == 0:
            return jsonify({"code": 400, "msg": "库存不足，下单失败"})

        conn.commit()
        return jsonify({"code": 200, "msg": "success"})

    finally:
        # 一定执行的
        cursor.close()
        conn.close()

if __name__ == '__main__':
    init_db()
    app.run(port=5000)