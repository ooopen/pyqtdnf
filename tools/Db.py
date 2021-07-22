#coding:utf-8
import time
from threading import Thread

import mysql.connector


class Db():
    connList = []

    # 每个连接最大使用次数
    useTimes = 10
    # 默认开启的线程数量
    threadNum = 10
    # 获取连接超时时间(ms)
    maxGetConnTime = 1000
    # mysql配置
    cfg = {'user': 'root', 'password': '', 'host': '127.0.0.1', 'database': 'test'}

    #初始化连接池
    def __init__(self):
        for i in range(self.threadNum):
            con = self.connect()
            self.connList.append(con)

    #获取连接
    def connect(self):
        cnx = mysql.connector.connect(**self.cfg)
        cursor = cnx.cursor()

        return {"cnx": cnx, "cursor": cursor, "useTime": 0}

    #从连接池获取可用连接
    def getConn(self):
        for i in range(self.maxGetConnTime):
            if (len(self.connList) > 0):
                return self.connList.pop(0)
            time.sleep(0.001)
        return None

    #执行具体sql并返回
    def execute(self, query, arg=()):
        conn = self.getConn()
        if (conn == None):
            print("无可用连接")
            return

        cursor = conn['cnx'].cursor()
        cursor.execute(query, arg)
        emp_no = cursor.lastrowid
        rt = cursor.fetchall()
        dataList = []
        for x in rt:
            dataList.append(dict(zip(cursor.column_names, x)))  # 添加字段名称

        # 关闭游标
        conn['cnx'].commit()
        cursor.close()

        # 默认连接最多使用次数
        if (conn['useTime'] < self.useTimes):

            conn['useTime'] = conn['useTime'] + 1
        else:
            # 关闭连接
            conn['cnx'].close()

            # 补充新的连接
            conn = self.connect()

        self.connList.append(conn)  # 把连接塞回去

        # 返回结果
        return {"data":dataList,'lastrowid':emp_no}


# ret = Db()
#
#
# def run():
#     query = ("SELECT * FROM auction "
#              "WHERE id BETWEEN %s AND %s")
#
#     data = ret.execute(query, (1, 2))
#     for i in data:
#         print(i)
#
# #为了查看mysql的连接数效果
# time.sleep(3)
#
# #开启100个线程进行测试
# for i in range(100):
#     thread = Thread(target=run, name=run.__name__,
#                     args=()  # 元组
#                     )
#     thread.start()
# time.sleep(1)
# for i in ret.list:
#     print(i)
