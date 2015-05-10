#某科学的选课系统-数据库PJ
###基于Flask+SQLAlchemy

Demo: [http://xk.ihcblog.com](http://xk.ihcblog.com)   
复旦大学内网可用   
如域名未能解析,请手动修改HOSTS指向10.141.247.162

---
##功能:
* 基本功能
  * a.登录登出控制、个人资料修改
  * b.学生选课、查询、退课
  * c.管理员增删改查课程、增删改查用户、由课程查学生、由学生查课程后台选课
  * d.教师查自己学生、给分
* 额外功能
  * a.学生选课自动列出历史给分(数据来源:[GPATools](https://github.com/hackerzhou/GPATool))
  * b.后台数据分析并图标展示
  * c.课程推荐功能

---
##部署说明
* 安装依赖
  * pip install -r requirements.txt
* 数据库初始化
  * create database fdxk;
  * python manager.py db init (if the folder migrations does not exist)
  * python manager.py db migrate
  * python manager.py db upgrade
* 运行
  * python run.py
* 部署至服务器
  * 自己问谷哥→_→

---
##协议
* 本项目依照GPL V2开源
* Copyright [ihciah](http://www.ihcblog.com) & qzane