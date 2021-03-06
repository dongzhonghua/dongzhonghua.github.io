[TOC]

# 方法区？

方法区（Method area）是可供各个线程共享的运行时内存区域，它存储了每一个类的结构信息，相当于把程序中共性的部分抽离出来。

例如：运行时常量池（Runtime constant pool）。字段和方法数据、构造函数和普通方法的字节码内容，还包括一些在类、实例、接口初始化时用到的特殊方法。
方法区在虚拟机启动的时候创建，方法区的容量可以是固定的，也可以随着程序的执行实现动态扩展，并在不需要过多空间的时候自动回收。方法区在实际内存中可以是不连续的。


## JDK7 之前
在 JDK 之前，方法区位于永久代（PermGen），永久代和堆相互隔离，永久代的大小在 JVM 中可以设定一个固定值，不可变。方法区是一种jvm的规范，而永久代是一种实现，并且只有 HotSpot 才有 “PermGen space”，而对于其他类型的虚拟机，如 JRockit（Oracle）、J9（IBM） 并没有“PermGen space”。由于方法区主要存储类的相关信息，所以对于动态生成类的情况比较容易出现永久代的内存溢出。

> 永久代是 Hotspot 虚拟机特有的概念，是方法区的一种实现，别的 JVM 都没有这个东西。永久代与新生代和老年代相样，前者并不是位于堆中，后后两者是位于堆中的。

在这个时候永久代就是方法区的实现，这个时期默认方法区即永久代。在这个时候永久代里面存放了很多东西，例如，符号引用（Symbols）、字符串常量池（interned strings）、类的静态变量（class static variables）、运行时常量池以及其它信息。由于这个时候方法区是由永久代实现的，那么方法区出现异常后会抛出这样的信息：java.lang.OutOfMemoryError: PermGen， 这里的 PermGen 就是永久代的意思，从这个就可以看出此时的方法区的实现是永久代。

## JDK7
在这个时候官方以及发现用永久代实现方法区容易导致内存泄漏的问题了，同时为了后面将 Hotspot 虚拟机与其他虚拟机整合，已经有将方法区改用其他的方式类实现了，但是并没有动工！此时只是将原本位于永久代中的字符串常量、类的静态变量池转移到了 Java Heap 中，还有符号引用转移到了 Native Memory
此时你使用 String 类的 intern() 方法，你会发现与 jdk6 及以前出现不一样的 结果。

> 在 Jdk6 以及以前的版本中，字符串的常量池是放在堆的 Perm 区的，Perm 区是一个类静态的区域，主要存储一些加载类的信息，常量池，方法片段等内容，默认大小只有 4m，一旦常量池中大量使用 intern 是会直接产生 java.lang.OutOfMemoryError:PermGen space 错误的。

## JDK8 及以后
取消永久代，方法区由元空间（Metaspace）实现，元空间仍然与堆不相连，但与堆共享物理内存，逻辑上可认为在堆中。

> 元空间的本质和永久代类似，都是对 JVM 规范中方法区的实现。不过元空间与永久代之间最大的区别在于：元空间并不在虚拟机中，而是使用本地内存。，理论上取决于 32 位/64 位系统可虚拟的内存大小。可见也不是无限制的，需要配置参数。

在之前的永久代实现中，如果要修改方法区的大小配置，需要使用 PermSize ，MaxPermSize 参数，而改为元空间之后，就需要使用 MetaspaceSize，MaxMetaspaceSize。

## 为什么移除永久代？
字符串存在永久代中，容易出现性能问题和内存溢出。
永久代大小不容易确定，PermSize 指定太小容易造成永久代 OOM
永久代会为 GC 带来不必要的复杂度，并且回收效率偏低。
Oracle 可能会将 HotSpot 与 JRockit 合二为一。



# 常量池、运行时常量池、字符串常量池

在JDK7之前，字符串常量是存在永久带Perm 区的，JDK7开始在将常量池迁移到堆中，这个变化也导致了String的新特性，接下来，我们按照jdk7开始后的版本进行介绍。

![字符串常量池的位置.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/字符串常量池的位置.png)

## 常量池分类

1. 运行时常量池
2. Class文件常量池
3. 字符串常量池

## Class文件常量池

.java经过编译后生成的.class文件，是Class文件的资源仓库。

常量池中主要存放俩大常量：字面量（文本字符串，final常量）和符号引用（类和接口的全局定名，字段的名称和描述，方法的名称和描述），如下图：

![常量池结构.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/常量池结构.png)

## 运行时常量池（Constant Pool）

运行时常量池是方法区的一部分。在Class常量池中，用于存放编译期间生成的字面量和符号量，在类加载完之后，存入运行时常量池中。而运行时常量池期间也有可能加入新的常量（如：String.intern方法）

## String常量池，

String常量池，JVM为了减少字符串对象的重复创建，在堆区开一段内存存放字符串。



<style type="text/css">
    h1 { counter-reset: h2counter; }
    h2 { counter-reset: h3counter; }
    h3 { counter-reset: h4counter; }
    h4 { counter-reset: h5counter; }
    h5 { counter-reset: h6counter; }
    h6 { }
    h2:before {
      counter-increment: h2counter;
      content: counter(h2counter) ".\0000a0\0000a0";
    }
    h3:before {
      counter-increment: h3counter;
      content: counter(h2counter) "."
                counter(h3counter) ".\0000a0\0000a0";
    }
    h4:before {
      counter-increment: h4counter;
      content: counter(h2counter) "."
                counter(h3counter) "."
                counter(h4counter) ".\0000a0\0000a0";
    }
    h5:before {
      counter-increment: h5counter;
      content: counter(h2counter) "."
                counter(h3counter) "."
                counter(h4counter) "."
                counter(h5counter) ".\0000a0\0000a0";
    }
    h6:before {
      counter-increment: h6counter;
      content: counter(h2counter) "."
                counter(h3counter) "."
                counter(h4counter) "."
                counter(h5counter) "."
                counter(h6counter) ".\0000a0\0000a0";
    }
</style>