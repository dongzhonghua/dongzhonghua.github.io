[toc]

## 异步复制丢失

对于Redis主节点与从节点之间的数据复制，是异步复制的，当客户端发送写请求给master节点的时候，客户端会返回OK，然后同步到各个slave节点中。

如果此时master还没来得及同步给slave节点时发生宕机，那么master内存中的数据会丢失；

要是master中开启持久化设置数据可不可以保证不丢失呢？答案是否定的。在master 发生宕机后，sentinel集群检测到master发生故障，重新选举新的master，如果旧的master在故障恢复后重启，那么此时它需要同步新master的数据，此时新的master的数据是空的（假设这段时间中没有数据写入）。那么旧master中的数据就会被刷新掉，此时数据还是会丢失。
## redis主从模式脑裂问题

redis的集群脑裂是指因为网络问题，导致redis master节点跟redis slave节点和sentinel集群处于不同的网络分区，此时因为sentinel集群无法感知到master的存在，所以将slave节点提升为master节点。此时存在两个不同的master节点，就像一个大脑分裂成了两个。
![redis主从脑裂.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/redis主从脑裂.png)集群脑裂问题中，如果客户端还在基于原来的master节点继续写入数据，那么新的master节点将无法同步这些数据，当网络问题解决之后，sentinel集群将原先的master节点降为slave节点，此时再从新的master中同步数据，将会造成大量的数据丢失。




## 解决方案

在了解了上面的两种数据丢失场景后，我们如何保证数据可以不丢失呢？在分布式系统中，衡量一个系统的可用性，我们一般情况下会说4个9,5个9的系统达到了高可用（99.99%，99.999%，据说淘宝是5个9）。对于redis集群，我们不可能保证数据完全不丢失，只能做到使得尽量少的数据丢失。


```
min-replicas-to-write 3
min-replicas-max-lag 10
```

**第一个参数表示连接到master的最少slave数量**
**第二个参数表示slave连接到master的最大延迟时间**
按照上面的配置，要求至少3个slave节点，且数据复制和同步的延迟不能超过10秒，否则的话master就会拒绝写请求，配置了这两个参数之后，如果发生集群脑裂，原先的master节点接收到客户端的写入请求会拒绝，就可以减少数据同步之后的数据丢失。