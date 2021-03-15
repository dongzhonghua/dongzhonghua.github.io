[TOC]

# Redis单线程多线程的一些问题

## 1. 为什么Redis6之前是单线程设计？

首先，这里说的单线程不是值整个Redis都是单线程，Redis4，5不是单线程程序。Redis的单线程是指Redis接受连接，接收数据解析协议，发送结果等命令的执行都是在主线程中执行。还是有很多



![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B.png)

![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis线程模型2.png)