[TOC]

# docker常用命令

## Docker简介
Docker是一个开源的应用容器引擎，让开发者可以打包应用及依赖包到一个可移植的镜像中，然后发布到任何流行的Linux或Windows机器上。使用Docker可以更方便地打包、测试以及部署应用程序。

## 安装
> curl -fsSL https://get.docker.com | bash -s docker --mirror Aliyun 
>
> https://cr.console.aliyun.com/cn-hangzhou/instances/mirrors（配置国内镜像加速）


## 常用命令

### 搜索镜像
docker search java

### 下载镜像
docker pull java:8

### 查看镜像版本

>   由于`docker search`命令只能查找出是否有该镜像，不能找到该镜像支持的版本，所以我们需要通过`Docker Hub`来搜索支持的版本。

-   进入`Docker Hub`的官网，地址：https://hub.docker.com
-   然后搜索需要的镜像：