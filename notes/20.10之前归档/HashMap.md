## HashMap 知识点，常见的面试题

[TOC]

Map家族：

<img src="https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/map%E5%AE%B6%E6%97%8F.png" alt="img" style="zoom:50%;" />

### 1. HashMap的内部数据结构

数组 + 链表/红黑树

### 2. HashMap允许空键空值么

HashMap最多只允许一个键为Null(多条会覆盖)，但允许多个值为Null

### 3. 影响HashMap性能的重要参数

初始容量：`创建哈希表(数组)时桶的数量，默认为 16`
负载因子：哈希表在其容量自动增加之前可以达到多满的一种尺度，默认为 0.75

### 4. HashMap的工作原理

HashMap是基于hashing的原理，我们使用put(key, value)存储对象到HashMap中，使用get(key)从HashMap中获取对象

### 5. HashMap中put()的工作原理

![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/hashmap%E7%9A%84put%E5%8E%9F%E7%90%86%E5%9B%BE.png)

### 6.HashMap 的底层数组长度为何总是2的n次方

HashMap根据用户传入的初始化容量，利用无符号右移和按位或运算等方式计算出第一个大于该数的2的幂。

- 使数据分布均匀，减少碰撞
- 当length为2的n次方时，h&(length - 1) 就相当于对length取模，而且在速度、效率上比直接取模要快得多

### 7. JDK1.8中做了哪些优化优化？

- `数组+链表改成了数组+链表或红黑树`
- `链表的插入方式从头插法改成了尾插法`
- `扩容的时候1.7需要对原数组中的元素进行重新hash定位在新数组的位置，1.8采用更简单的判断逻辑，位置不变或索引+旧容量大小；`
- 在插入时，1.7先判断是否需要扩容，再插入，1.8先进行插入，插入完成再判断是否需要扩容；

### 8.HashMap线程安全方面会出现什么问题

- 在jdk1.7中，在多线程环境下，扩容时会造成环形链或数据丢失。
- 在jdk1.8中，在多线程环境下，会发生数据覆盖的情况

### 9. 那么为什么默认是16呢？怎么不是4？不是8？

关于这个默认容量的选择，JDK并没有给出官方解释，那么这应该就是个经验值，既然一定要设置一个默认的2^n 作为初始值，那么就需要在效率和内存使用上做一个权衡。这个值既不能太小，也不能太大。

太小了就有可能频繁发生扩容，影响效率。太大了又浪费空间，不划算。

所以，16就作为一个经验值被采用了。

### 10. HashMap线程安全方面会出现什么问题

1.put的时候导致的多线程数据不一致

比如有两个线程A和B,首先A希望插入一个key-valu对到HashMap中,首先计算记录所要落到的 hash桶的索引坐标,然后获取到该桶里面的链表头结点,此时线程A的时间片用完了,而此时线程B被调度得以执行,和线程A一样执行,只不过线程B成功将记录插到了桶里面,假设线程A插入的记录计算出来的 hash桶索引和线程B要插入的记录计算出来的 hash桶索引是一样的,那么当线程B成功插入之后,线程A再次被调度运行时,它依然持有过期的链表头但是它对此一无所知,以至于它认为它应该这样做,如此一来就覆盖了线程B插入的记录,这样线程B插入的记录就凭空消失了,造成了数据不一致的行为。

2.resize而引起死循环

这种情况发生在HashMap自动扩容时,当2个线程同时检测到元素个数超过 数组大小 ×负载因子。此时2个线程会在put()方法中调用了resize(),两个线程同时修改一个链表结构会产生一个循环链表(JDK1.7中,会出现resize前后元素顺序倒置的情况)。接下来再想通过get()获取某一个元素,就会出现死循环。

如果还不明白的话看这两篇文章就可以：

- [HashMap死循环](https://blog.csdn.net/qq_37141773/article/details/85112743)
- [HashMap线程不安全的体现](https://www.cnblogs.com/developer_chan/p/10450908.html)

### 11. 为什么1.8改用红黑树

比如某些人通过找到你的hash碰撞值，来让你的HashMap不断地产生碰撞，那么相同key位置的链表就会不断增长，当你需要对这个HashMap的相应位置进行查询的时候，就会去循环遍历这个超级大的链表，性能及其地下。java8使用红黑树来替代超过8个节点数的链表后，查询方式性能得到了很好的提升，从原来的是O(n)到O(logn)。

### 12. 1.8中的扩容为什么逻辑判断更简单

元素在重新计算hash之后，因为n变为2倍，那么n-1的mask范围在高位多1bit(红色)，因此新的index就会发生这样的变化：

![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/hashmap%E7%9A%84resize%E5%8E%9F%E7%90%86.png)

因此，我们在扩充HashMap的时候，不需要像JDK1.7的实现那样重新计算hash，只需要看看原来的hash值新增的那个bit是1还是0就好了，是0的话索引没变，是1的话索引变成“原索引+oldCap”，可以看看下图为16扩充为32的resize示意图：

![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/hashmap%E7%9A%84resize%E8%BF%87%E7%A8%8B.png)

这个设计确实非常的巧妙，既省去了重新计算hash值的时间，而且同时，由于新增的1bit是0还是1可以认为是随机的，因此resize的过程，均匀的把之前的冲突的节点分散到新的bucket了。这一块就是JDK1.8新增的优化点。有一点注意区别，JDK1.7中rehash的时候，旧链表迁移新链表的时候，如果在新表的数组索引位置相同，则链表元素会倒置，但是从上图可以看出，JDK1.8不会倒置。

### 13.HashMap中hash函数怎么是是实现的？还有哪些 hash 的实现方式？

　　1. 对key的hashCode做hash操作（高16bit不变，低16bit和高16bit做了一个异或）；
　　2. h & (length-1); //通过位操作得到下标index。

　　还有数字分析法、平方取中法、分段叠加法、 除留余数法、 伪随机数法。


![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/hashmap%E9%9D%A2%E8%AF%95%E9%A2%98%E5%9B%BE%E7%89%87.png)