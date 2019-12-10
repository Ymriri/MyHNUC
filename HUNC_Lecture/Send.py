# -*- conding:utf-8 -*-
"""
@author:ym
@time:12-2019/12/9-
"""
import requests
import pymysql
import json
import time

# USER1 是QQ号
USER1 = 1448265203
USER2 = 1961834221

# GROUP 是QQ群
GROUP = 492703951
class LectureMes():
    lecture_name = ""
    lectrue_id = ""
    lectrue_time = ""


class Update(object):
    def __init__(self):
        # 首先创造出空类型,都是json格式的
        # 第一个会SQL 然后更新
        # 更新都是根据名字来更新的
        self.lectrue = {"LuShan": None, "CreatPlace": None, "Lecture": None}

    def send_all(self, mes):
        self.__send_QQ(flag=2, mes=mes)
        self.__send_QQ(flag=196, mes=mes)

    def update_lushan(self, mes, where):
        """
        :param mes:
        :param where:
        :return:
        """
        # print(mes["name"])
        # print(where)
        if self.lectrue[str(where)] == str(mes["name"]):
            # print("临时化成功")
            return False
        else:
            # 询问数据库
            try:
                if self.__select_sql(mes):
                    # 更新数据
                    self.__insert_sql(mes)
                    self.lectrue[str(where)] = str(mes["name"])
                    return True
                else:
                    # 说明数据库有，直接覆盖程序临时数据
                    self.lectrue[str(where)] = str(mes["name"])
                    return False
            except Exception as i:
                print(i)
                self.__send_QQ(mes=str(self.__get_now_time()) + ":Send/49:数据更新出错！", flag=1)
        return False

    def __get_now_time(self):
        # 获得当前的时间
        return time.strftime('%m-%d-%H:%M:%S ', time.localtime(time.time()))

    def __select_sql(self, mes):
        """
        查询sql 是否有和mes一样的数据
        :param mes: json
        :return: bool  没有返回true
        """
        try:
            db = pymysql.connect(host="localhost", port=3306, user="root", passwd="你的密码",
                                 db="python_database")
            cursor = db.cursor()
            selectsql = "SELECT * FROM python_database.lecture where lecture_name = \"" + str(mes["name"]) + "\";"
            state = cursor.execute(selectsql)
            # print("状态："+str(state))
            cursor.close()
            if state == 0:
                return True
            else:
                return False
        except:
            self.__send_QQ(flag=1, mes=str(self.__get_now_time() + "  Send/81:数据库比较出现错误!"))
        return False

    def __insert_sql(self, mes):
        """
        :param mes: json
        :return: 插入成功返回True
        """
        try:
            db = pymysql.connect(host="localhost", port=3306, user="root", passwd="你的密码",
                                 db="python_database")
            cursor = db.cursor()
            insertSql = "INSERT INTO `python_database`.`lecture` ( `lecture_url`, `lecture_time`, `lecture_name`) " \
                        "VALUES ( %s, %s, %s);"
            # print(str(mes["link"]))
            # print(str(mes["time"]))
            # print(str(mes["name"]))
            li = (str(mes["link"]), str(mes["time"]), str(mes["name"]))
            # print(li)
            try:
                cursor.execute(insertSql, li)
                # print(1)
                db.commit()  # 如果是对数据库操作 需要commit
                cursor.close()
                return True
            except Exception as e:
                print(e)
                cursor.close()
                db.rollback()  # 回滚数据
        except:
            print("Error: unable to insert data" + str(self.get_now_time()))
        self.__send_QQ(flag=1, mes=str(self.__get_now_time() + " Send/98:数据更新插入失败！"))
        return False

    def __send_QQ(self, flag, mes):  # 只允许自己调用
        """
        这里使用了酷Q的http发送QQ信息
        :param flag: 1是发送信息给自己 2是发到群里
        :param mes: json
        :return: 是否发送成功
        """
        url = "http://127.0.0.1:5700/"
        """
        {"data":{"message_id":199477},"retcode":0,"status":"ok"}
        """
        data = {}
        try:
            sendMes = "讲座名字：" + str(mes["name"]) + "\n\n发布时间：" + str(mes["time"]) + "\n\n链接：" + str(mes["link"])
        except:
            # 如果报错说明是 提醒的错误信息！
            sendMes = str(mes)
        # print(sendMes)
        result = None
        if flag == 1:
            # 只发给我一个人
            data["user_id"] = USER1
            data["message"] = sendMes
            url = url + "send_private_msg"
            result = requests.post(url=url, data=data)
        elif flag == 196:
            data["user_id"] = USER2
            data["message"] = sendMes
            url = url + "send_private_msg"
            result = requests.post(url=url, data=data)
        else:
            url = url + "send_group_msg"
            data["group_id"] = GROUP
            data["message"] = sendMes
            result = requests.post(url=url, data=data)
        try:
            # result = requests.get(url=url)
            # print(result.text)
            result = result.json()
            # print(result)
            if result["status"] == "ok":
                return True
            else:
                print("Send/128：发送失败1")
                return False
        except:
            print("Send/131:发送失败2")
            return False

#
# if __name__ == '__main__':
#     test = Update()
#     print(test.get_now_time())
