[TOC]

## redis实现消息队列

Redis也可以实现消息队列，但是只适合只有一组消费者的消息队列。不过Redis没有消息队列的高级特性，没有ack保证。



使用`lpop rpop lpush rpush` 这几个命令可以实现Redis的消息队列。当然其他组合也可以作为栈来使用。

### 队列为空的情况怎么办

队列为空会导致空轮询，可以用sleep来解决，但是sleep会导致消息延迟增大。所以也可以用阻塞读来进行。`blpop` 

如果线程一直阻塞，Redis的客户端连接就变成了闲置连接，闲置太久，服务器一般会主动断开连接。这个时候blpop就会抛出异常。所以需要捕获异常并且重试。



## 延时队列

延时队列可以用zset来实现。将到期时间作为zset的score，然后多个线程轮询zset获取到期的任务进行处理。因为有多个线程，需要考虑并发争抢任务。



其他的延时队列实现方式：

**消息中间件**

比如Kafka基于时间轮自定义了一个用于实现延迟功能的定时器（SystemTimer），Kafka中的时间轮（TimingWheel）是一个存储定时任务的环形队列，可以进行相关的延时队列设置。

**netty**

[Netty](https://links.jianshu.com/go?to=http%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI3ODcxMzQzMw%3D%3D%26mid%3D2247491548%26idx%3D3%26sn%3Dcbb7e36f2d41f2e80feeec5d78b4de13%26chksm%3Deb539aeadc2413fc5d82cb18bb552b84a7fa37764c728e89885d2ed7d0a983978bff29a1e5ab%26scene%3D21%23wechat_redirect)也有基于时间轮算法来实现延时队列。[Netty](https://links.jianshu.com/go?to=http%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzI3ODcxMzQzMw%3D%3D%26mid%3D2247491548%26idx%3D3%26sn%3Dcbb7e36f2d41f2e80feeec5d78b4de13%26chksm%3Deb539aeadc2413fc5d82cb18bb552b84a7fa37764c728e89885d2ed7d0a983978bff29a1e5ab%26scene%3D21%23wechat_redirect)在构建延时队列主要用HashedWheelTimer，HashedWheelTimer底层数据结构是使用DelayedQueue，采用时间轮的算法来实现。



**DelayQueue来实现延时队列**

Java中有自带的DelayQueue数据类型，我们可以用这个来实现延时队列。DelayQueue是封装了一个PriorityQueue（优先队列），在向DelayQueue队列中添加元素时，会给元素一个Delay（延迟时间）作为排序条件，队列中最小的元素会优先放在队首，对于队列中的元素只有到了Delay时间才允许从队列中取出。这种实现方式是数据保存在内存中，可能面临数据丢失的情况，同时它是无法支持分布式系统的。







