[TOC]

# Redis持久化

一般情况下，Redis主节点不会进行持久化操作。

## AOF

### AOF重写

由于aof文件可能再运行过程中逐渐变得非常大，所以Redis提供了bgrewriteaof指令用于对aof日志的瘦身。其原理就是开辟一个新的线程用来吧内存中的元素转换成一系列的Redis操作指令，序列化到一个新的aof文件中去。序列化完成之后再将操作期间发生的增量的操作追加到这个aof日志中。

## RDB

## 混合持久化

两种持久化方式各有优缺点，rdb比较快，但是会丢失大量数据。但是aof又相对慢很多。所以Redis4.0带来了一个新的持久化选项，混合持久化。可以将rdb文件和rdb之后的aof日志放在一起。