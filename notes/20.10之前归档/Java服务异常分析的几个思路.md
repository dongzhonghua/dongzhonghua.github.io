Java服务异常分析的几个思路

# Java服务异常分析的几个思路

1.  首先使用top命令查看CPU使用情况。

```java
jps // 拿到Java进程的$pid
top -Hp $pid // 对单独的进程，显示线程资源消耗情况。
```

top（cpu）、free（内存）、df（磁盘）、dstat（网络流量）、pstack、vmstat、strace（底层系统调用）

![问题查看](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/问题查看.png)

![问题查看1](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/问题查看1.png)

https://cloud.tencent.com/developer/article/1600345

```
top命令显示当前系统正在执行的进程的相关信息，包括进程ID、内存占用率、CPU占用率等
-b 批处理
-c 显示完整的治命令
-I 忽略失效过程
-s 保密模式
-S 累积模式
-i<时间> 设置间隔时间
-u<用户名> 指定用户名
-p<进程号> 指定进程
-n<次数> 循环显示的次数
```

2.  找到具体的线程，分析这个线程在干嘛

https://www.xncoding.com/2018/06/25/java/jstack.html

jps（进程）、jmap（内存）、jstack（线程）、jinfo（参数）等。

-    jps：查询当前机器所有JAVA进程信息 
-    jmap：输出某个 Java 进程内存情况（如产生那些对象及数量等） 
-    jstack：打印某个 Java 线程的线程栈信息 
-    jinfo：用于查看 jvm 的配置参数

```java
jstack $pid // 获取线程堆栈信息
```

3.  cpu火焰图

------

### 火焰图

### async-profiler简介

1.  基于采样的轻量级诊断工具，支持cpu、lock、mem、thread、cachemiss等分析
2.  可以分析jvm/native/kelnel调用栈
3.  可以轻松生成火焰图

项目地址：https://github.com/jvm-profiling-tools/async-profiler

### **下载压缩包**

### wget https://github.com/jvm-profiling-tools/async-profiler/releases/download/v1.6/async-profiler-1.6-linux-x64.tar.gz

### **解压缩**

### tar -zxvf async-profiler-1.6-linux-x64.tar.gz

### 使用流程

解压后我们会得到一个profiler.sh脚本，主要功能皆通过该脚本完成

### 分析CPU

1.  获取分析的进程号：jps -v
2.  执行脚本 ./profiler.sh -e cpu -d 60 -f cpu.svg pid
3.  sz cpu.svg 到本地并用chrome打开火焰图即可

### 分析内存分配

1.  获取分析的进程号：jps -v
2.  执行脚本 ./profiler.sh -e alloc -d 60 -f mem_alloc.svg pid
3.  sz mem_alloc.svg 到本地并用chrome打开火焰图即可

### 分析锁

1.  获取分析的进程号：jps -v
2.  执行脚本 ./profiler.sh -e lock -d 60 -f lock.svg pid
3.  sz lock.svg 到本地并用chrome打开火焰图即可



### 分析线程状态

1.  获取分析的进程号：jps -v
2.  执行脚本 ./profiler.sh -e wall -t -i 5ms -f thread.svg pid
3.  sz thread.svg 到本地并用chrome打开火焰图即可

### 其他常用指令与功能

1.   ./profiler.sh list pid 查看支持的事件
2.  分析cachemiss：./profiler.sh -d 30 -e cache-misses pid
3.  相关脚本参数详情可参见github，有详细说明

火焰图分析指南

http://www.brendangregg.com/flamegraphs.html