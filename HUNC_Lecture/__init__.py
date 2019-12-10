# -*- conding:utf-8 -*-
"""
@author:ym
@time:12-2019/12/8-
"""
import json

import requests
import re
import schedule as schedule
from datetime import datetime

import functools


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
def bad_task():
    print("now")
    return 1 / 0


schedule.every(5).minutes.do(bad_task)

