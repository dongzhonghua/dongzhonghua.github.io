[TOC]

# 使用nettty来实现一个简单的RPC

## TODO
-[ ] 客户端获取结果有没有一个更好的办法，去看看掘金小册。
-[ ] future的实现原理？有没有更好的future的实现？
-[ ] 代理工厂那个地方实现的还是不够优雅
-[ ] zookeeper注册中心等
-[ ] 加入更多的rpc的功能？

## 原理
RPC(remote process call), 远程过程调用。它主要实现的功能就是调用另外一个进程的函数但是像是在调用本地的一样。既然是跨进程通信，我们自然就想到了利用socket来进行通信。只要把调用的信息封装起来，通过socket传到另一个进行然后解码，通过代理调用函数就可以完成整个过程。其中最重要的也就是socket通信的部分，使用netty可以非常方便的实现socket通信。

广义的来讲一个完整的 RPC 包含了很多组件，包括服务发现，服务治理，远程调用，调用链分析，网关等等。今天先从一个简单的demo做起。



![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/rpc%E5%8E%9F%E7%90%86.png)

1. client 会调用本地动态代理 proxy
2. 这个代理会将调用通过协议转序列化字节流
3. 通过 netty 网络框架，将字节流发送到服务端
4. 服务端在受到这个字节流后，会根据协议，反序列化为原始的调用，利用反射原理调用服务方提供的方法
5. 如果请求有返回值，又需要把结果根据协议序列化后，再通过 netty 返回给调用方

代码地址

## 协议

rpc的协议主要是考虑如何把一次rpc调用过程描述清楚，利用socket通信，rpc调用过程需要编程字节流传输，所以需要还需要编解码。



## 服务器端

## 客户端



## 参考
> 主要参考：https://juejin.cn/post/6844903957622423560
> https://www.w3cschool.cn/architectroad/architectroad-rpc-framework.html
> https://github.com/pjmike/springboot-rpc-demo
> 提供了非常好的解决思路：https://xilidou.com/2018/09/26/dourpc-remoting/