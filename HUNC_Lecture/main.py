# -*- conding:utf-8 -*-
"""
@author:ym
@time:12-2019/12/8-
"""
from Lecture import Lecture
import schedule
import functools
import time
from Send import Update
import json
def catch_exceptions(cancel_on_failure=False):
    def catch_exceptions_decorator(job_func):
        @functools.wraps(job_func)
        def wrapper(*args, **kwargs):
            try:
                return job_func(*args, **kwargs)
            except:
                import traceback
                print(traceback.format_exc())
                if cancel_on_failure:
                    return schedule.CancelJob

        return wrapper

    return catch_exceptions_decorator


@catch_exceptions(cancel_on_failure=True)
def lushang(job, update):
        # 获得麓山信息
        mes = job.get_lushang(36)
        mes = json.loads(mes)
        print(mes)
        if str(mes["code"]) != str("200"):
            pass
        else:
            if update.update_lushan(mes=mes, where="LuShan"):
                update.send_all(mes=mes)
        # 获得学术信息
        mes = job.get_lushang(37)
        mes = json.loads(mes)
        print(mes)
        if str(mes["code"]) != str("200"):
            pass
        else:
            if update.update_lushan(mes=mes, where="Lecture"):
                update.send_all(mes=mes)
        # 获得创客中心信息
        mes = job.get_create_space()
        mes = json.loads(mes)
        print(mes)
        if str(mes["code"]) != str("200"):
            pass
        else:
            if update.update_lushan(mes=mes, where="CreatPlace"):
                update.send_all(mes=mes)

# if __name__ == '__main__':
job = Lecture()
update = Update()
# 每分钟执行一次
schedule.every(30).seconds.do(lushang, job,update)
while 1:
    schedule.run_pending()
    time.sleep(1)