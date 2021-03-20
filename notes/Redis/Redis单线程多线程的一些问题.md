[TOC]

# Redis单线程多线程的一些问题

## 1. 为什么Redis6之前是单线程设计？

首先，这里说的单线程不是值整个Redis都是单线程，Redis4，5不是单线程程序。Redis的单线程是指Redis接受连接，接收数据解析协议，发送结果等命令的执行都是在主线程中执行。还是有很多模块有各自的线程在执行任务。

Redis基于Reactor模式开发了网络事件处理器，这个处理器被称为文件事件处理器。它的组成结构为4部分：多个套接字、IO多路复用程序、文件事件分派器、事件处理器。
因为文件事件分派器队列的消费是单线程的，所以Redis才叫单线程模型。

Redis单个线程的原因：


- Redis的主要瓶颈不在cpu，而在内存和网络IO
- 使用单线程设计，可以简化数据库结构的设计
- 可以减少多线程锁带来的性能损耗




![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis%E7%BA%BF%E7%A8%8B%E6%A8%A1%E5%9E%8B.png)

![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis线程模型2.png)

## 2. 什么是IO多线程

 既然Redis的主要瓶颈不在CPU，为什么又要引入IO多线程？Redis的整体处理流程如下图：
![redis读写过程.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis%E8%AF%BB%E5%86%99%E8%BF%87%E7%A8%8B.png)
​ 结合上图可知，当 socket 中有数据时，Redis 会通过系统调用将数据从内核态拷贝到用户态，供 Redis 解析用。这个拷贝过程是阻塞的，术语称作 “同步 IO”，数据量越大拷贝的延迟越高，解析协议时间消耗也越大，糟糕的是这些操作都是在主线程中处理的，特别是链接数特别多的情况下，这种情况更加明显。基于以上原因，Redis作者提出了Thread/IO线程，既将接收与发送数据来使用多线程并行处理，从而降低主线程的等待时间。