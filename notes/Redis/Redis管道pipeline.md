[TOC]

## pipeline

pipeine并不是redis服务器提供的技术，这个技术本质上是redis客户端提供的，和服务器没有什么关系。Pipline只不过是把多条请求变成了一条请求。



## redis压测

可以使用redis-benchmark -t set -q来进行压测。

```
# 不使用管道执行get set 100000次请求
[root@iz2zeaf3cg1099kiidi06mz ~]# redis-benchmark -t get,set -q -n 100000
SET: 55710.31 requests per second
GET: 54914.88 requests per second
# 每次pipeline组织的命令个数 为 100
[root@iz2zeaf3cg1099kiidi06mz ~]# redis-benchmark -P 100 -t get,set -q -n 100000
SET: 1020408.19 requests per second
GET: 1176470.62 requests per second
# 每次pipeline组织的命令个数 为 10000
[root@iz2zeaf3cg1099kiidi06mz ~]# redis-benchmark -P 10000 -t get,set -q -n 100000
SET: 321543.41 requests per second
GET: 241545.89 requests per second
```



## pipeline原理

pipeline把多次命令都放到一起执行了，为什么这么快呢。其实原因还是在于IO。Redis执行命令是比较快的，重点在于IO比较耗时，read时如果缓冲区没有数据就需要等待，write时如果缓冲区慢了也需要等待。而pipline把这些多个耗时的操作都放到一起了。相当于Redis每次读都能读到好几条命令去执行。

> Pipeline管道机制不单单是为了减少RTT的一种方式，它实际上大大提高了在Redis服务器中每秒可执行的总操作量。原因是，在没有使用管道机制的情况下，从访问数据结构和产生回复的角度来看，为每个命令提供服务是非常便宜的。但是从底层套接字的角度来看，这是非常昂贵的，这涉及read（）和write（）系统调用，从用户态切换到内核态，这种上下文切换开销是巨大。而使用Pipeline的情况下，通常使用单个read（）系统调用读取许多命令，然后使用单个write（）系统调用传递多个回复。这样就提高了每秒可执行的操作数