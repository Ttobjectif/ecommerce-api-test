import sqlite3
from common.logger import log

# 默认连接 mock_server 数据库
DB_PATH = "./mock_server/ecommerce.db"

def query_db(sql):
    """通用查询方法"""
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        return cursor.fetchall()
    except Exception as e:
        log.error(f"查询失败: {sql}, 报错: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()

def execute_db(sql):
    """通用修改方法（增删改）"""
    conn = sqlite3.connect(DB_PATH, timeout=5)
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        conn.commit()
    except Exception as e:
        conn.rollback()
        log.error(f"执行失败: {sql}, 报错: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()