# nginx

## 安装和卸载nginx的方法:

```shell


#apt安装nginx方法
sudo apt-add-repository ppa:nginx/development
sudo apt-get update
sudo apt-get install nginx

#apt卸载nginx方法
#卸载方法1.
# 删除nginx，保留配置文件
sudo apt-get remove nginx
#删除配置文件
rm -rf /etc/nginx

#罗列出与nginx相关的软件并删除
dpkg --get-selections|grep nginx
sudo apt-get --purge remove nginx
sudo apt-get --purge remove nginx-common
sudo apt-get --purge remove nginx-core
#卸载方法2.
#删除nginx连带配置文件
sudo apt-get purge nginx # Removes everything.包括配置文件

#卸载不再需要的nginx依赖程序
sudo apt-get autoremove

#全局查找与nginx相关的文件
sudo  find  /  -name  nginx*

#比较靠谱的解决办法是：root权限下载命令行敲入如下命令：

rm -rf /etc/nginx/
rm -rf /usr/sbin/nginx
rm /usr/share/man/man1/nginx.1.gz
apt-get remove nginx*
```

## nginx命令

```shell
nginx #打开 nginx
nginx -t   #测试配置文件是否有语法错误
nginx -s reopen #重启Nginx
nginx -s reload  #重新加载Nginx配置文件，然后以优雅的方式重启Nginx
nginx -s stop  #强制停止Nginx服务
nginx -s quit  #优雅地停止Nginx服务（即处理完所有请求后再停止服务）

nginx [-?hvVtq] [-s signal] [-c filename] [-p prefix] [-g directives]

-?,-h      : 打开帮助信息
-v       : 显示版本信息并退出
-V       : 显示版本和配置选项信息，然后退出
-t       : 检测配置文件是否有语法错误，然后退出
-q       : 在检测配置文件期间屏蔽非错误信息
-s signal    : 给一个 nginx 主进程发送信号：stop（强制停止）, quit（优雅退出）, reopen（重启）, reload（重新加载配置文件）
-p prefix    : 设置前缀路径（默认是：/usr/share/nginx/）
-c filename   : 设置配置文件（默认是：/etc/nginx/nginx.conf）
-g directives  : 设置配置文件外的全局指令
```