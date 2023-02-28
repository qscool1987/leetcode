# 网站部署说明
# 安装必要组件
## 安装python3 mysql
yum install python3

yum install pip3

yum install mysql

yum install mysql-server

pip3 install pymysql

1. systemctl status mysqld.service 启动mysql
2. 用conf/leetcode.sql中的sql语句创建表结构
3. 进入dao/ 更改dao.py 中的mysql账号密码为自己的mysql账号密码

## 安装flask 搭建网站后端
pip3 install flask

cd lc_notify/ && python app.py

## 安装nginx
yum install nginx 

将 conf/nginx.conf 替换 /etc/nginx/nginx.conf, 注意更改配置中的ip:port

## 部署前端
web/* 目录为前端项目目录, 将其部署到/usr/share/nginx/html/leetcode下

注意：前端脚本中访问后段的ip:port 同样要更改，如果不部署前端则忽略

mv web/* /usr/share/nginx/html/leetcode

## 统计程序 建议配置crontab定时执行
python lc_notify.py

# 其他说明
## log 说明
lc_notify.log 为lc_notify.py运行时的日志

web_server_access.log 为supervisor launch app.py web服务的日志

web_server_err.log 为supervisor launch app.py web服务时的错误日志

## supervisor (可选) 强烈推荐用 supervisor管理后端服务
安装 supervisor
yum install -y supervisor

supervisor 启动配置文件
用conf/my_app.py 替换/etc/supervisord.d/flask_web_app.ini

启动和关闭 supervisor
systemctl start supervisord 
systemctl stop supervisord

supervisorctl status # 查看服务状态 
supervisorctl stop flask_web_app # 停止服务
supervisorctl start flask_web_app # 启动服务

## 项目目录介绍
dao/ 为与数据库交互的对象目录

scripts/ 为运维脚本目录

log/ 日志目录

conf/ 配置目录

web/ 前端项目目录

app.py 后端入口脚本 启动服务端： 执行 python app.py

lc_notify.py 统计程序脚本，可以用crontab 定时执行



