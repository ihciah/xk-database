#某科学的选课系统-数据库PJ
###初步计划采用Flash框架实现

---
##功能:
* 基本功能
  * a.登录登出控制、资料修改
  * b.选课、查询、退课
  * c.管理员添加课程、后台选课
* 额外功能
  * a.教师账号登录、查看学生列表、详细信息
  * b.学生选课自动列出历史给分
  * c.后台数据分析并图标展示
  * d.课程列表导入
* 更多待续...

---
##部署说明
* 数据库初始化
  * python manager.py db init(if the folder migrations does not exist)
  * python manager.py db migrate
  * python manager.py db upgrade
* 运行
  * python run.py
* 依赖
  * pip install -r requirements.txt

---
##协议
* 本项目依照GPL V2开源
* Copyright [ihciah](http://www.ihcblog.com) & qzane