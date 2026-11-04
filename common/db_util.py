import sqlite3
from common.logger import log


def query_db(sql):
    log.info(f"--- 开始查询本地模拟数据库，SQL: {sql} ---")

    # 1. 连接内存数据库
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    try:
        # 2. 模拟造一条数据
        cursor.execute("CREATE TABLE orders (item_id TEXT, status TEXT)")
        cursor.execute("INSERT INTO orders VALUES ('10086', 'PAID')")

        # 3. 执行传进来的 SQL
        cursor.execute(sql)
        result = cursor.fetchall()

        log.info(f"数据库查询结果: {result}")
        return result

    finally:
        cursor.close()
        conn.close()
        log.info("--- 数据库连接已关闭 ---")