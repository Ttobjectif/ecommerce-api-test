from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# 初始化一个极简的 SQLite 数据库和商品表
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS products (id TEXT, name TEXT, stock INT)')
    # 初始插入一件库存为 10 的 iPhone
    cursor.execute('INSERT OR REPLACE INTO products VALUES ("1001", "iPhone", 10)')
    conn.commit()
    conn.close()

init_db()

@app.route('/api/products/1001', methods=['GET'])
def get_product():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM products WHERE id = "1001"')
    result = cursor.fetchone()
    conn.close()
    if result:
        return jsonify({"id": result[0], "name": result[1], "stock": result[2]})
    return jsonify({"msg": "not found"}), 404

# 下单接口：扣减库存
@app.route('/api/orders/create', methods=['POST'])
def create_order():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    # 扣减库存
    cursor.execute('UPDATE products SET stock = stock - 1 WHERE id = "1001"')
    conn.commit()
    conn.close()
    return jsonify({"code": 200, "msg": "success"})

if __name__ == '__main__':
    app.run(port=5000)