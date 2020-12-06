[TOC]

Redis提供了基于“发布/订阅”模式的消息机制，此种模式下，消息发布者和订阅者不进行直接通信，发布者客户端向指定的频道（channel）发布消息，订阅该频道的每个客户端都可以收到该消息，如图所示。Redis提供了若干命令支持该功能，在实际应用开发时，能够为此类问题提供实现方法。

## Redis发布订阅

Redis主要提供了发布消息、订阅频道、取消订阅以及按照模式订阅和取消订阅等命令。

### 1.  发布消息

```undefined
publish channel message
```

下面操作会向channel：sports频道发布一条消息“Tim won thechampionship”，返回结果为订阅者个数，因为此时没有订阅，所以返回结果为0：

```css
127.0.0.1:6379> publish channel:sports "Tim won the championship"
(integer) 0
```

### 2.  订阅消息

```css
subscribe channel [channel ...]
```

订阅者可以订阅一个或多个频道，下面操作为当前客户端订阅了channel：sports频道：

```css
127.0.0.1:6379> subscribe channel:sports
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "channel:sports"
3) (integer) 1
```

此时另一个客户端发布一条消息：

```css
127.0.0.1:6379> publish channel:sports "James lost the championship"
(integer) 1
```

当前订阅者客户端会收到如下消息：

```css
127.0.0.1:6379> subscribe channel:sports
Reading messages... (press Ctrl-C to quit)
...
1) "message"
2) "channel:sports"
3) "James lost the championship"
```

有关订阅命令有两点需要注意：

-   客户端在执行订阅命令之后进入了订阅状态，只能接收subscribe、psubscribe、unsubscribe、punsubscribe的四个命令。
-   新开启的订阅客户端，无法收到该频道之前的消息，因为Redis不会对
     发布的消息进行持久化。

和很多专业的消息队列系统（例如Kafka、RocketMQ）相比，Redis的发布订阅略显粗糙，例如无法实现消息堆积和回溯。但胜在足够简单，如果当前场景可以容忍的这些缺点，也不失为一个不错的选择。

### 3.  取消订阅

```css
unsubscribe [channel [channel ...]]
```

客户端可以通过unsubscribe命令取消对指定频道的订阅，取消成功后，不会再收到该频道的发布消息：

```css
127.0.0.1:6379> unsubscribe channel:sports
1) "unsubscribe"
2) "channel:sports"
3) (integer) 0
```

### 4. 按照模式订阅和取消订阅

```css
psubscribe pattern [pattern...]
punsubscribe [pattern [pattern ...]]
```

除了subcribe和unsubscribe命令，Redis命令还支持glob风格的订阅命令psubscribe和取消订阅命令punsubscribe，例如下面操作订阅以it开头的所有频道：

```
127.0.0.1:6379> psubscribe it*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "it*"
3) (integer) 1
```
### 5. 查询订阅
1）查看活跃的频道
```
pubsub channels [pattern]
```
所谓活跃的频道是指当前频道至少有一个订阅者，其中[pattern]是可以指定具体的模式：
```
127.0.0.1:6379> pubsub channels
1) "channel:sports"
2) "channel:it"
3) "channel:travel"
127.0.0.1:6379> pubsub channels channel:*r*
1) "channel:sports"
2) "channel:travel"
```
2）查看频道订阅数
```
pubsub numsub [channel ...]
```
当前channel：sports频道的订阅数为2：
```
127.0.0.1:6379> pubsub numsub channel:sports
1) "channel:sports"
2) (integer) 2
```
3）查看模式订阅数
```
pubsub numpat
```
当前只有一个客户端通过模式来订阅：

```
127.0.0.1:6379> pubsub numpat
(integer) 1
```

## 原理

Redis是使用C实现的，通过分析 Redis 源码里的 [pubsub.c](https://github.com/dongzhonghua/redis-3.0-annotated/blob/unstable/src/pubsub.c) 文件，了解发布和订阅机制的底层实现，籍此加深对 Redis 的理解。

通过 SUBSCRIBE 命令订阅某频道后，redis-server 里维护了一个字典，字典的键就是一个个 channel ，而字典的值则是一个链表，链表中保存了所有订阅这个 channel 的客户端。SUBSCRIBE 命令的关键，就是将客户端添加到给定 channel 的订阅链表中。

通过 PUBLISH 命令向订阅者发送消息，redis-server 会使用给定的频道作为键，在它所维护的 channel 字典中查找记录了订阅这个频道的所有客户端的链表，遍历这个链表，将消息发布给所有订阅者。

![redis-pub-sub.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis-pub-sub.png)

前面说到，Redis 将所有接受和发送信息的任务交给 channel 来进行，而所有 channel 的信息就储存在 redisServer 这个结构中：


```c
struct redisServer {
     // 省略 ...  　　
     dict *pubsub_channels; // Map channels to list of subscribed clients  　　
     // 省略 ...  　　
     };
```


pubsub_channels 是一个字典，字典的键就是一个个 channel ，而字典的值则是一个链表，链表中保存了所有订阅这个 channel 的客户端。

举个例子，如果在一个 redisServer 实例中，有一个叫做 news 的频道，这个频道同时被client_123 和 client_456 两个客户端订阅，那么这个 redisServer 结构看起来应该是这样子：
![订阅发布redis-server结构.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/订阅发布redis-server结构.png)

可以看出，实现 SUBSCRIBE 命令的关键，就是将客户端添加到给定 channel 的订阅链表中。

### SUBSCRIBE 命令的实现

函数 pubsubSubscribeChannel 是 SUBSCRIBE 命令的底层实现，它完成了将客户端添加到订阅链表中的工作：

```c
// 订阅指定频道
// 订阅成功返回 1 ，如果已经订阅过，返回 0
int pubsubSubscribeChannel(redisClient *c, robj *channel) {
    struct dictEntry *de;
    list *clients = NULL;
    int retval = 0;
    /* Add the channel to the client -> channels hash table */
    // dictAdd 在添加新元素成功时返回 DICT_OK
    // 因此这个判断句表示，如果新订阅 channel 成功，那么 。。。
    if (dictAdd(c->pubsub_channels, channel, NULL) == DICT_OK) {
        retval = 1;
        incrRefCount(channel);
        /* Add the client to the channel -> list of clients hash table */
        // 将 client 添加到订阅给定 channel 的链表中
        // 这个链表是一个哈希表的值，哈希表的键是给定 channel
        // 这个哈希表保存在 server.pubsub_channels 里
        de = dictFind(server.pubsub_channels, channel);
        if (de == NULL) {
            // 如果 de 等于 NULL
            // 表示这个客户端是首个订阅这个 channel 的客户端
            // 那么创建一个新的列表， 并将它加入到哈希表中
            clients = listCreate();
            dictAdd(server.pubsub_channels, channel, clients);
            incrRefCount(channel);

        } else {
            // 如果 de 不为空，就取出这个 clients 链表
            clients = dictGetVal(de);

        }
        // 将客户端加入到链表中
        listAddNodeTail(clients, c);

    }
    /* Notify the client */
    addReply(c, shared.mbulkhdr[3]);
    addReply(c, shared.subscribebulk);
    // 返回订阅的频道
    addReplyBulk(c, channel);
    // 返回客户端当前已订阅的频道和模式数量的总和
    addReplyLongLong(c, dictSize(c->pubsub_channels) + listLength(c->pubsub_patterns));
    return retval;
}
```

### PUBLISH 命令的实现

使用 PUBLISH 命令向订阅者发送消息，需要执行以下两个步骤：

1) 使用给定的频道作为键，在 redisServer.pubsub_channels 字典中查找记录了订阅这个频道的所有客户端的链表，遍历这个链表，将消息发布给所有订阅者。

2) 遍历 redisServer.pubsub_patterns 链表，将链表中的模式和给定的频道进行匹配，如果匹配成功，那么将消息发布到相应模式的客户端当中。

举个例子，假设有两个客户端分别订阅 it.news 频道和 it.* 模式，当执行命令PUBLISH it.news "hello moto" 的时候， it.news 频道的订阅者会在步骤 1 收到信息，而当PUBLISH 进行到步骤 2 的时候， it.* 模式的订阅者也会收到信息。

PUBLISH 命令的实际实现由 pubsubPublishMessage 函数完成，它的完整定义如下：

```c
// 发送消息 
int pubsubPublishMessage(robj *channel, robj *message) {
    int receivers = 0;
    struct dictEntry *de;
    listNode *ln;
    listIter li;
    /* Send to clients listening for that channel */
    // 向所有频道的订阅者发送消息 
    de = dictFind(server.pubsub_channels, channel);
    if (de) {
        list *list = dictGetVal(de); // 取出所有订阅者 
        listNode *ln;
        listIter li;
        // 遍历所有订阅者， 向它们发送消息 
        listRewind(list, &li);
        while ((ln = listNext(&li)) != NULL) {
            redisClient *c = ln->value;
            addReply(c, shared.mbulkhdr[3]);
            addReply(c, shared.messagebulk);
            addReplyBulk(c, channel); // 打印频道名 
            addReplyBulk(c, message); // 打印消息 
            receivers++; // 更新接收者数量 
        }
    }
    /* Send to clients listening to matching channels */
    // 向所有被匹配模式的订阅者发送消息 
    if (listLength(server.pubsub_patterns)) {
        listRewind(server.pubsub_patterns, &li); // 取出所有模式 
        channel = getDecodedObject(channel);
        while ((ln = listNext(&li)) != NULL) {
            pubsubPattern *pat = ln->value; // 取出模式 
            // 如果模式和 channel 匹配的话 
            // 向这个模式的订阅者发送消息 
            if (stringmatchlen((char *) pat->pattern->ptr,
                               sdslen(pat->pattern->ptr),
                               (char *) channel->ptr,
                               sdslen(channel->ptr), 0)) {
                addReply(pat->client, shared.mbulkhdr[4]);
                addReply(pat->client, shared.pmessagebulk);
                addReplyBulk(pat->client, pat->pattern); // 打印被匹配的模式 
                addReplyBulk(pat->client, channel); // 打印频道名 
                addReplyBulk(pat->client, message); // 打印消息 
                receivers++; // 更新接收者数量 
            }
        }
        decrRefCount(channel); // 释放用过的 channel 
    }
    return receivers; // 返回接收者数量 
}
```



## 业务场景

明确了Redis发布订阅的原理和基本流程后，我们来看一下Redis的发布订阅到底具体能做什么。

**1、异步消息通知**

比如渠道在调支付平台的时候，我们可以用回调的方式给支付平台一个我们的回调接口来通知我们支付状态，还可以利用Redis的发布订阅来实现。比如我们发起支付的同时订阅频道`pay_notice_` + `wk` (假如我们的渠道标识是wk，不能让其他渠道也订阅这个频道)，当支付平台处理完成后，支付平台往该频道发布消息，告诉频道的订阅者该订单的支付信息及状态。收到消息后，根据消息内容更新订单信息及后续操作。

当很多人都调用支付平台时，支付时都去订阅同一个频道会有问题。比如用户A支付完订阅频道`pay_notice_wk`，在支付平台未处理完时，用户B支付完也订阅了`pay_notice_wk`，当A收到通知后，接着B的支付通知也发布了，这时渠道收不到第二次消息发布。因为同一个频道收到消息后，订阅自动取消，也就是订阅是一次性的。

所以我们订阅的订单支付状态的频道就得唯一，一个订单一个频道，我们可以在频道上加上订单号`pay_notice_wk`+orderNo保证频道唯一。这样我们可以把频道号在支付时当做参数一并传过去，支付平台处理完就可以用此频道发布消息给我们了。（实际大多接口用回调通知，因为用Redis发布订阅限制条件苛刻，系统间必须共用一套Redis）

![redis使用场景支付.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis使用场景支付.png)


2、任务通知
比如通过跑批系统通知应用系统做一些事（跑批系统无法拿到用户数据，且应用系统又不能做定时任务的情况下）。如每天凌晨3点提前加载一些用户的用户数据到Redis，应用系统不能做定时任务，可以通过系统公共的Redis来由跑批系统发布任务给应用系统，应用系统收到指令，去做相应的操作。

![Redis发布订阅应用任务通知.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/Redis发布订阅应用任务通知.png)
这里需要注意的是在线上集群部署的情况下，所有服务实例都会收到通知，都要做同样的操作吗？完全没必要。可以用Redis实现锁机制，其中一台实例拿到锁后执行任务。另外如果任务比较耗时，可以不用锁，可以考虑一下任务分片执行。当然这不在本文的讨论范畴，这里不在赘述。

3、参数刷新加载

众所周知，我们用Redis无非就是将系统中不怎么变的、查询又比较频繁的数据缓存起来，例如我们系统首页的轮播图啊，页面的动态链接啊，一些系统参数啊，公共数据啊都加载到Redis，然后有个后台管理系统去配置修改这些数据。

打个比方我们首页的轮播图要再增加一个图，那我们就在后管系统加上，加上就完事了吗？当然没有，因为Redis里还是老数据。那你会说不是有过期时间吗？是的，但有的过期时间设置的较长如24小时并且我们想立即生效怎么办？这时候我们就可以利用Redis的发布订阅机制来实现数据的实时刷新。当我们修改完数据后，点击刷新按钮，通过发布订阅机制，订阅者接收到消息后调用重新加载的方法即可。（有点没看懂这个说的，还有这个有没有其他的方案？）

![redis发布订阅应用场景刷新缓存.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis发布订阅应用场景刷新缓存.png)


参考：
https://www.jianshu.com/p/58dcc12e84f9
https://www.cnblogs.com/duanxz/p/6053520.html