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
```shell
docker search java
```



### 下载镜像
```shell
docker pull java:8
```



### 查看镜像版本

>   由于`docker search`命令只能查找出是否有该镜像，不能找到该镜像支持的版本，所以我们需要通过`Docker Hub`来搜索支持的版本。

-   进入`Docker Hub`的官网，地址：https://hub.docker.com，然后搜索需要的镜像，查看版本。

-   下载镜像：

```shell
docker pull nginx:1.17.0
```



### 列出镜像

```shell
docker images
```

### 删除镜像

-   指定名称删除镜像：

```
docker rmi java:8
```

-   指定名称删除镜像（强制）：

```
docker rmi -f java:8
```

-   删除所有没有引用的镜像：

```
docker rmi `docker images | grep none | awk '{print $3}'`
```

-   强制删除所有镜像：

```
docker rmi -f $(docker images)
```

### 打包镜像

```
# -t 表示指定镜像仓库名称/镜像名称:镜像标签 .表示使用当前目录下的Dockerfile文件
docker build -t mall/mall-admin:1.0-SNAPSHOT .
```

## Docker容器常用命令

### 新建并启动容器

```
docker run -p 80:80 --name nginx \
-e TZ="Asia/Shanghai" \
-v /mydata/nginx/html:/usr/share/nginx/html \
-d nginx:1.17.0
```

-   -p：将宿主机和容器端口进行映射，格式为：宿主机端口:容器端口；
-   --name：指定容器名称，之后可以通过容器名称来操作容器；
-   -e：设置容器的环境变量，这里设置的是时区；
-   -v：将宿主机上的文件挂载到宿主机上，格式为：宿主机文件目录:容器文件目录；
-   -d：表示容器以后台方式运行。

-   [OPTIONS] 参数说明：

| --add-host list                | 添加自定义主机到ip映射(书写格式为：主机:ip)                  |
| ------------------------------ | ------------------------------------------------------------ |
| -a, --attach list              | 附加到STDIN、STDOUT或STDERR上                                |
| --blkio-weight uint16          | Block IO (相对权重)，取值10到1000之间，0为禁用(默认0)        |
| --blkio-weight-device list     | Block IO weight (相对于设备的权重) (默认为数组的形式)        |
| --cap-add list                 | 添加Linux功能                                                |
| --cap-drop list                | 删除Linux功能                                                |
| --cgroup-parent string         | 容器的可选父级对照组项                                       |
| --cidfile string               | 将容器ID写入文件                                             |
| --cpu-period int               | 限制CPU CFS(完全公平调度程序)周期                            |
| --cpu-quota int                | 限制CPU CFS(完全公平的调度程序)上限                          |
| --cpu-rt-period int            | 限制CPU运行时周期(以微秒为单位)                              |
| --cpu-rt-runtime int           | 限制CPU实时运行时间(以微秒为单位)                            |
| -c, --cpu-shares int           | CPU 共享 (相对权重的设定)                                    |
| --cpus decimal                 | 设定cpu的数量                                                |
| --cpuset-cpus string           | 允许执行的cpu (0-3,0,1)                                      |
| --cpuset-mems string           | 允许执行的MEMs (0-3,0,1)                                     |
| -d, --detach                   | 在后台运行容器并打印容器ID                                   |
| --detach-keys string           | 覆盖分离容器的键序列                                         |
| --device list                  | 向容器添加主机设备                                           |
| --device-cgroup-rule list      | 向 cgroup 允许的设备列表中添加一个或多个规则                 |
| --device-read-bps list         | 限定设备的读取速率（单位: byte/s）（默认为 []）              |
| --device-read-iops list        | 限定设备的读取速率（单位：IO/s）（默认为 []）                |
| --device-write-bps list        | 限定设备的写入速率（单位: byte/s）（默认为 []）              |
| --device-write-iops list       | 限定设备的写入速率（单位：IO/s）（默认为 []）                |
| --disable-content-trust        | 跳过镜像验证(默认为 true)                                    |
| --dns list                     | 设置自定义DNS服务器                                          |
| --dns-option list              | 设置DNS选项                                                  |
| --dns-search list              | 设置自定义的DNS搜索域                                        |
| --entrypoint string            | 覆盖镜像的默认入口点                                         |
| -e, --env list                 | 设置环境变量                                                 |
| --env-file list                | 读取环境变量内容                                             |
| --expose list                  | 公开一个端口或多个端口                                       |
| --group-add list               | 添加其他要加入的组                                           |
| --health-cmd string            | 命令运行以检查健康                                           |
| --health-interval duration     | 运行检查之间的时间(ms\|s\|m\|h)(默认为 0s)                   |
| --health-retries int           | 连续的失败需要报告不健康                                     |
| --health-start-period duration | 启动健康重试倒计时前容器初始化的启动周期(ms\|s\|m\|h)(默认为 0s) |
| --health-timeout duration      | 健康检查运行情况的最大时间值 格式为：(ms\|s\|m\|h) (默认 0s) |
| --help                         | 打印出使用情况                                               |
| -h, --hostname string          | 定义容器主机名                                               |
| --init                         | 在容器中运行初始化，以转发信号并获取进程                     |
| -i, --interactive              | 即使没有连接，也保持STDIN开放                                |
| --ip string                    | 设定容器的 IPv4 地址 (例如，192.168.155.139)                 |
| --ip6 string                   | 设定IPv6地址(例如，2001:db8::33)                             |
| --ipc string                   | 使用IPC模式                                                  |
| --isolation string             | 容器隔离技术                                                 |
| --kernel-memory bytes          | 内核内存限制                                                 |
| -l, --label list               | 在容器上设置元数据                                           |
| --label-file list              | 在以行分隔的标签文件中读取                                   |
| --link list                    | 向另一个容器添加链接                                         |
| --link-local-ip list           | 容器 IPv4/IPv6 链接本地地址                                  |
| --log-driver string            | 设定容器的日志驱动                                           |
| --log-opt list                 | 设定日志驱动器选项                                           |
| --mac-address string           | 配置容器MAC地址(例如，92:d0:c6:0a:29:33)                     |
| -m, --memory bytes             | 设定内存限额                                                 |
| --memory-reservation bytes     | 内存软限制                                                   |
| --memory-swap bytes            | 交换限制等于内存加上交换:'-1'，以启用无限交换                |
| --memory-swappiness int        | 优化容器内存交换 (0 到 100) (默认为 -1)                      |
| --mount mount                  | 将文件系统挂载附加到容器                                     |
| --name string                  | 为容器指定一个名称                                           |
| --network string               | 将容器连接到网络                                             |
| --network-alias list           | 为容器连接的网络添加别名                                     |
| --no-healthcheck               | 禁止任何容器指定 HEALTHCHECK                                 |
| --oom-kill-disable             | 禁止OOM事件被杀死                                            |
| --oom-score-adj int            | 优化主机的OOM事件 ，参数范围 (-1000 到 1000)                 |
| --pid string                   | 设定PID命名                                                  |
| --pids-limit int               | 优化容器pid限制(如果设置-1则为无限制)                        |
| --privileged                   | 赋予容器扩展的权限                                           |
| -p, --publish list             | 将容器的端口发布到主机                                       |
| -P, --publish-all              | 将所有公开的端口发布到随机端口                               |
| --read-only                    | 将容器的根文件系统挂载为只读（后面会详细讲到）               |
| --restart string               | 配置容器的重启策略，当容器退出时重新启动(默认为“no”)         |
| --rm                           | 当容器退出时自动移除这个容器                                 |
| --runtime string               | 使用容器的运行时                                             |
| --security-opt list            | 指定docker启动的安全项                                       |
| --shm-size bytes               | /dev/shm 的大小（这个可以使其容量进行动态的扩展）            |
| --sig-proxy                    | 设置代理接收京城信号 (默认为 true)                           |
| --stop-signal string           | 停止容器的信号 (默认为 "SIGTERM")                            |
| --stop-timeout int             | 设置超时停止容器(以秒为单位)                                 |
| --storage-opt list             | 设定容器的存储驱动程序选项                                   |
| --sysctl map                   | 指定系统控制项 (默认为 map[] 的格式)                         |
| --tmpfs list                   | 挂载tmpfs目录                                                |
| -t, --tty                      | 为当前容器分配一个客户端                                     |
| --ulimit ulimit                | 启动需要限制的项(默认为数组的形式)                           |
| -u, --user string              | 用户名或UID(格式为: <name\|uid>[:<group\|gid>])              |
| --userns string                | 使用用户名称空间                                             |
| --uts string                   | 使用UTS名称空间                                              |
| -v, --volume list              | 绑定安装卷（关于容器卷，在Docker容器数据卷中会具体的讲解）   |
| --volume-driver string         | 容器的可选卷驱动程序                                         |
| --volumes-from list            | 指定容器装载卷                                               |
| -w, --workdir string           | 容器内的工作目录                                             |



### 列出容器

-   列出运行中的容器：

```
docker ps
```

-   列出所有容器：

```
docker ps -a
```

### 停止容器

注意：`$ContainerName`表示容器名称，`$ContainerId`表示容器ID，可以使用容器名称的命令，基本也支持使用容器ID，比如下面的停止容器命令。

```
docker stop $ContainerName(or $ContainerId)
```

例如：

```
docker stop nginx
#或者
docker stop c5f5d5125587
```

### 强制停止容器

```
docker kill $ContainerName
```

### 启动容器

```
docker start $ContainerName
```

### 进入容器

>   https://blog.csdn.net/skh2015java/article/details/80229930



### 删除容器

-   删除指定容器：

```
docker rm $ContainerName
```

-   按名称通配符删除容器，比如删除以名称`mall-`开头的容器：

```
docker rm `docker ps -a | grep mall-* | awk '{print $1}'`
```

-   强制删除所有容器；

```
docker rm -f $(docker ps -a -q)
```

### 查看容器的日志

-   查看容器产生的全部日志：

```
docker logs $ContainerName
```

-   动态查看容器产生的日志：

```
docker logs -f $ContainerName
```

### 查看容器的IP地址

```
docker inspect --format '{{ .NetworkSettings.IPAddress }}' $ContainerName
```

### 修改容器的启动方式

```
# 将容器启动方式改为always
docker container update --restart=always $ContainerName
```

### 同步宿主机时间到容器

```
docker cp /etc/localtime $ContainerName:/etc/
```

### 指定容器时区

```
docker run -p 80:80 --name nginx \
-e TZ="Asia/Shanghai" \
-d nginx:1.17.0
```

### 查看容器资源占用状况

-   查看指定容器资源占用状况，比如cpu、内存、网络、io状态：

```
docker stats $ContainerName
```

-   查看所有容器资源占用情况：

```
docker stats -a
```

### 查看容器磁盘使用情况

```
docker system df
```

### 执行容器内部命令

```
docker exec -it $ContainerName /bin/bash
```

### 指定账号进入容器内部

```
# 使用root账号进入容器内部
docker exec -it --user root $ContainerName /bin/bash
```

### 查看所有网络

```
docker network ls
[root@local-linux ~]# docker network ls
NETWORK ID          NAME                     DRIVER              SCOPE
59b309a5c12f        bridge                   bridge              local
ef34fe69992b        host                     host                local
a65be030c632        none     
```

### 创建外部网络

```
docker network create -d bridge my-bridge-network
```

### 指定容器网络

```
docker run -p 80:80 --name nginx \
--network my-bridge-network \
-d nginx:1.17.0
```

## 修改镜像的存放位置

-   查看Docker镜像的存放位置：

```
docker info | grep "Docker Root Dir"
```

-   关闭Docker服务：

```
systemctl stop docker
```

-   先将原镜像目录移动到目标目录：

```
mv /var/lib/docker /mydata/docker
```

-   建立软连接：

```
ln -s /mydata/docker /var/lib/docker
```