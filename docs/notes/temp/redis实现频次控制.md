我们经常会遇到这样的需求，例如：

- 每个用户1秒内最多产生一次有效的点赞
- 一个小时内最多只能发5个帖子
- 每天只能跟10个陌生人聊天
- PK时3秒内累计1000分会产生一次暴击

# 方案一、使用zset将历史记录存下来

要统计频次，最简单直接的方法就把历史记录存下来，有了历史记录想怎么统计都可以。使用zset可以很容易的实现。以一个用户一个小时内最多只能发5个帖子的需求为例:

key： userId

value： 这一次操作的唯一标识，比如帖子id

score：发帖时间戳

示例代码如下：

```java
// 使用zcount获取一个小时内的发帖数量
String key = key(userId);
long startTime = System.currentTimeMillis() - TimeUnit.HOURS.toMillis(1);
int count = redis.zcount(key, startTime, Long.MAX_VALUE);

if (count > THRESHOLD) {
	// 超过阈值，拒绝本次请求
} else {
	// 未超过阈值，执行发帖操作﻿
  // 记录本次操作
	double score = (double)System.currentTimeMillis(); // score使用当前时间戳
	String member = postId; // member使用记录id
	redis.pipeline(p -> {
		p.zadd(key, score, member);
		p.zremrangeByRank(key, 0, -(LIMIT + 1)); // 这里要限制zset的size，以免影响性能
        // Redis Zremrangebyrank 命令用于移除有序集中，指定排名(rank)区间内的所有成员。
		p.expire(key, EXPIRE);
	});
}
```

# 方案二、巧用过期时间

以一个小时内最多只能发5个帖子的需求为例，示例代码如下：

```java
long expireTime = TimeUnit.HOURS.toMillis(1);
String key = String.valueOf(userId);
long count = redis.incr(key);
long ttl = redis.pttl(key);
if (ttl <= 0) {
	redis.pexpire(expireTime);
}

if (count > THRESHOLD) {
	// 超过阈值，拒绝本次请求
} else {
	// 未超过阈值，执行发帖操作
}
```

# 方案三、巧用key

这个方案的思路是将当前时间追加到key里，过期时间只要比时间窗口长就可以了。适用于时间窗口是自然时间（自然周、自然日、自然小时）的场景，比如：一个用户一天内（与24小时内区别一下）只能发5个动态，示例代码如下：

```java
String currentDay = "0420"; // 以4月20日为例
String key = key(userId, currentDay);
long count = redis.pipeline(p -> {
	Response<Long> cnt = redis.incr(key);
	redis.expire(EXPIRE); // 这里可以简单的使用固定过期时间，只要比时间窗口长即可
	return cnt;
});

if (count > THRESHOLD) {
	// 超过阈值，拒绝本次请求
} else {
	// 未超过阈值，执行发帖操作
}
```

# 方案四. key-value实现滑动时间窗口

有些场景下要求滑动的时间窗口，例如：PK时3秒内累计1000分会产生一次暴击。对于这样的需求，方案二和方案三就力不从心了，需要另一种实现方案，示例代码如下：

```java
// 累加当前秒的分数amount
long currentTimeSeconds = System.currentTimeMills / 1000;
String key = key(userId, currentTimeSeconds);
redis.pipeline(p -> {
	redis.incrBy(key, amount);
	redis.expire(EXPIRE);
}
// 分别取出前三秒的分数并求和
List<String> keys = LongStream.range(0, 3)
	.map(i -> key(userId, currentTimeSeconds - i))
	.collect(Collectors.toList());
int[] amounts = redis.pipeline(keys, RedisPipeline::get);
if (sum(amounts) > THRESHOLD) {
	// 超过阈值，产生暴击
} else {
	// 未超过阈值
}
```

该方案需要读取时间窗口内多个最小时间单位的数据，涉及多个key的读取，所以存在读放大的问题，时间窗口内的key数量越多，性能开销越大。

对于读放大的问题，我们可以结合应用场景和时间窗口的大小，选择适当的最小时间单位。例如：时间窗口是10秒，如果最小时间单位是1秒，那么我们需要读取10个key，如果将最小时间单位调整至2秒，那么我们读取的key的数量就下降到了5个。

# 方案五. hash优化滑动时间窗口

这个方案主要是为了优化方案四的读放大问题。

思路是将时间切成一个个时间片，每个时间片存储若干个最小时间单位。设置好时间片的长度，使得时间窗口在时间片上滑动时最多横跨两个时间片，这时候可以将读放大或者写放大的系数限制在2以内。

使用hash来存储时间片，最小时间单元存储在hash的元素里。

以PK时3秒内累计1000分会产生一次暴击为例，示例代码如下：

```java
// 为了便于理解，代码写的比较简单直接，没有考虑复用性
long now = System.currentTimeMillis() / 1000;
long currentMinute = now / 60; // 以一分钟为一个时间片
long currentSecond = now % 60; // 以一秒钟为最小时间单元

int[] amounts = redis.pipeline(p -> {
    // 累加当前秒的分数amount
    p.hincrby(key(userId, currentMinute), currentSecond, amount);
    if (currentSecond > 60 - 3) {
    	// 快到当前时间片的边界了，额外往下一分钟的时间片里写一次，这样读取的时候就不需要跨时间片了
        p.hincrby(key(userId, currentMinute + 1), currentSecond - 60, amount);
    }
    // 读取前三秒的分数并求和
    return p.hmget(key(userId, currentMinute), currentSecond, currentSecond - 1, currentSecond - 2);
});

if (sum(amounts) > THRESHOLD) {
	// 超过阈值，产生暴击
} else {
	// 未超过阈值
}
```

以上是使用redis实现频次计数及控制的五种方案及示例代码。抛砖引玉，大家还有什么其他方法，欢迎评论区留言讨论。