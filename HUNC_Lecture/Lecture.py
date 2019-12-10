# -*- conding:utf-8 -*-
"""
@author:ym
@time:12-2019/12/8
@describe: 获得所有讲座信息，返回JSON格式，只需要在调用函数
"""
import json
import random
import re
from lxml import html

import requests


class Lecture(object):
    USER_AGENT_LIST = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center "
        "PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322;"
        " .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; "
        ".NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2;"
        " .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2;"
        " .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) "
        "Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
        "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko)"
        " Chrome/19.0.1036.7 Safari/535.20",
        "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, "
        "like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, "
        "like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; "
        ".NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; "
        ".NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, "
        "like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64;"
        "Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; "
        ".NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; "
        "SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; "
        "Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; "
        "Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727;"
        " .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
        "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML,"
        " like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
        "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
        "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/58.0.3029.110 Safari/537.36"
    ]
    """
    所有
    """
    user_agent = ""
    headers = {}

    def __init__(self):
        self.change_user_agent()


    def change_user_agent(self):
        self.user_agent = random.choice(self.USER_AGENT_LIST)
        self.headers["User-Agent"] = self.user_agent

    def get_lushang(self, num):
        """
        :return:返回麓山讲座信息
        {
            code:  200  //正常返回   300 //数据处理出问题，提醒   400 //服务器出现问题，pass
        }
        num:36麓山大讲堂
        num:37第135期“麓山校友、企业家论坛
        """
        url = "http://wap.hnuc.edu.cn/column/" + str(num) + "/index.shtml"
        rt = {}
        try:
            response = requests.get(url=url, headers=self.headers)
            rt["code"] = "200"
        except ConnectionError:
            rt = {"code": "404"}
            return json.dumps(rt, ensure_ascii=False)
        try:

            response = response.text
            tree = html.fromstring(response)
            content = tree.xpath("/html/body/div[4]/div[2]/div[2]/div[1]/ul/li[1]")[0]
            name = content.xpath("./a/text()")[0]
            newurl = content.xpath("./a/@href")[0]
            newurl = "http://wap.hnuc.edu.cn" + str(newurl)
            time = content.xpath("./span/text()")[0]
            rt["name"] = str(name)
            rt["link"] = newurl
            rt["time"] = str(time)
        except IndexError:
            rt = {"code": "300"}
            return json.dumps(rt, ensure_ascii=False)
        return json.dumps(rt, ensure_ascii=False)

    def get_create_space(self):
        """
        :return:  返回麓山创客讲座信息
        URL：https://mp.weixin.qq.com/mp/homepage?__biz=MzAxNjk4ODU4MQ==&hid=9&sn=89d99173ee964c4f60288b5daf66f6
        c7&scene=18#wechat_redirect
        """
        url = "https://mp.weixin.qq.com/mp/homepage?__biz=MzAxNjk4ODU4MQ==&hid" \
              "=9&sn=89d99173ee964c4f60288b5daf66f6c7&scene=18#wechat_redirect"
        rt = {}
        try:
            response = requests.get(url=url, headers=self.headers).text
            rt["code"] = "200"
            # print(response)
        except ConnectionError:
            rt = {"code": "404"}
            return json.dumps(rt, ensure_ascii=False)
        try:
            msg = re.findall("var data={.*};", response)[0]
            link = re.findall("\"link\":\".*?\",", msg)[0]
            name = re.findall("\"title\":\".*?\",", msg)[0]
            time = str(name).replace("\"title\":\"麓山创客行专题讲座——", "").replace("期\",", "").replace(".", "-")
            link = str(link).replace("\"", "").replace("link:", "").replace(",", "")
            name = str(name).replace("\"title\":\"", "").replace("\"", "").replace(",", "")
        except IndexError:
            rt = {"code": "300"}
            return json.dumps(rt, ensure_ascii=False)
        rt["name"] = str(name)
        rt["link"] = str(link)
        rt["time"] = str(time)
        return json.dumps(rt, ensure_ascii=False)


if __name__ == '__main__':
    test = Lecture()
    
    print(test.get_create_space())
