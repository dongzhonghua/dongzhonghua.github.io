[TOC]

# 如何让你的网站支持https?

## 申请证书

SSL 证书通常需要购买，也有免费的，通过第三方 SSL 证书机构颁发。你也可以在云服务商上购买，但是一般免费的 ssl 证书只能支持单个域名。

我用的是阿里云的SSL证书，可以申请免费的。地址如下：
> https://common-buy.aliyun.com/?spm=5176.2020520154.0.0.1f8956a7lXJtr0&commodityCode=cas

![阿里云SSL证书购买.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/阿里云SSL证书购买.png)

![阿里云SSL证书下载.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/阿里云SSL证书下载.png)

下载证书，我选的是NGINX版本。
![阿里云SSL证书NGINX.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/阿里云SSL证书NGINX.png)

下载下来是两个文件，一个是.pem文件，一个是.key文件。把这两个文件上传到服务器，我是放在nginx/ssl目录下。接下来就配置nginx就可以了。

## 配置NGINX

直接把我的复制过来：

```nginx
user www-data;
worker_processes auto;
pid /run/nginx.pid;

events {
	worker_connections 768;
	# multi_accept on;
}

http {
    server {
        listen			        80;
        listen                  443 ssl;
        server_name             www.example.com;
        ssl_certificate         /etc/nginx/ssl/xxx.pem; # 你的pem和key文件的路径
        ssl_certificate_key     /etc/nginx/ssl/xxx.key;

        location / {
            root /etc/nginx/html;
            index index.html;
        }
    }

	sendfile on;
	tcp_nopush on;
	tcp_nodelay on;
	keepalive_timeout 65;
	types_hash_max_size 2048;
	# server_tokens off;


	include /etc/nginx/mime.types;
	default_type application/octet-stream;


	ssl_protocols TLSv1 TLSv1.1 TLSv1.2; # Dropping SSLv3, ref: POODLE
	ssl_prefer_server_ciphers on;


	access_log /var/log/nginx/access.log;
	error_log /var/log/nginx/error.log;

	gzip on;
	gzip_disable "msie6";


	include /etc/nginx/conf.d/*.conf;
	include /etc/nginx/sites-enabled/*;
}

```

现在重启NGINX访问网站就可以使用https了，访问http也会自动跳转到https。

参考：
https://juejin.im/post/6844904063688179720