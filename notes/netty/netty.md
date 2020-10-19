Netty in action 读书笔记

[TOC]

---

# CH1



---

# CH2



# CH3

netty的组件和设计。

-   Channel--Socket
-   EventLoop--控制流，多线程处理
-   ChannelFuture--异步通知

![img](https://raw.githubusercontent.com/dongzhonghua/dongzhonghua.github.io/master/img/blog/20140608174140640.jpeg)

## EventLoop

-   一个EventLoopGroup包含一个或多个EventLoop
-   一个EventLoop在他的生命周期内只和一个Thread绑定
-   所有有EventLoop处理的I/O事件都将在他专有的Thread上被处理（消除了同步的需求）
-   一个channel在他的生命周期内只注册于一个EventLoop
-   一个EventLoop坑会被分配给一个或者多个channel

## channelFuture

Netty中所有的I/O操作都是异步的。netty提供了ChannelFuture接口，其addListener（）方法注册了一个ChannelFutureListener，以便在某个操作完成时得到通知。

## ChennelHandler

处理入站和出站数据的应用程序逻辑的容器

## ChannelPipeline

提供了ChannelHandler链的容器，并定义了用于再改脸上传播入站和出站事件流的API。

