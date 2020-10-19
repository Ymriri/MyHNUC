# python实现HNUC部分讲座信息实时推送

需要的环境：Python 、~~酷Q CQHTTP插件~~、Mysql、Mirai(这里使用的是裙主大大封装[simple-qq](https://github.com/ForteScarlet/simple-robot-core))
python 需要下载的包：schedule、 requests 、lxml、pymysql

额外需要Mysql 存储数据：
  表名：lecture    
   属性：lecture_id、lecture_url, lecture_time, lecture_name lecture 自增

很难受的就是因为疫情，很多讲座不公开，只在个别院发布（学校超过一定人数需要向上申请）？？？计划全部打乱。 
毕业前需要听15个讲座才给毕业，emmmm，要不是看到有人点了start，基本不会更新了。那就更新一下咯
有疑问联系Q：1021644865,后续会把公众号推文和QQ动态关于讲座的爬取也增加进来
更新会在gitee.com和GitHub同步！

# [湖南强智科技教务系统全部模拟](https://gitee.com/ym_0101/HutbEduAdminSystem/tree/master/venv)
  * 自动登录
  * 自动评教
  * 获得课表
  * 获取全校课表
  * 自动抢课
  * 抢课带简陋页面
  * ~~查找学生信息~~
  * ~~查找老师信息~~

# 计划
 * JAVA仅仅是实现接口发送接收信息
 * python实现爬虫和推送
 * 添加微信机器人推送和监听公众号（暂时使用正则匹配和人工匹配是否是讲座信息，后期看情况使用NLP自动处理）
 * 分布式+微服务？ 看情况吧
 * 赞点了更多更新更快，hah
