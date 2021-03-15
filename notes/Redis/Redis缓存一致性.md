# 背景

本文结合一些自己理解，讲解cache miss等情况下如何保证缓存和db的一致性，下面的例子中缓存以redis为例

## 读

先redis，redis没有就读db

## 写

有几种

```undefined
1.先更新redis再更新db
2.先更新db再更新redis
3.先更新DB再删除redis
4.先删除redis再更新DB
5.延迟双删
6.延迟删除等变种
```

# 各种写场景与db redis一致性

## 1.先更新redis再更新db

按下面步骤会有问题,AB是两个线程

```undefined
A_update_redis
B_update_redis
B_update_db
A_update_db
```

最终db是a值但是redis是b值，不一致

## 2.先更新db再更新redis

```undefined
A_update_db
B_update_db
B_update_redis
A_update_redis
```

最终db是b值但是redis是a值

## 3.先更新DB再删除redis

```undefined
A_update_db
B_update_db
B_rm_redis
A_rm_redis
```

是不是不明白。想不出来怎么不一致了？
 不是这样的，没这么简单，第二次rm_redis就会保证后面的redis和db是一致的
 实际是下面这种形式

```undefined
A_get_data
redis_cache_miss
A_get_db
B_update_db
B_rm_redis
(此时如果拿db是b值，但是redis没有值)
A_update_redis
```

依赖于A_update_redis在B_update_db之后，极端情况
 此时redis是old，db是new

## 4.先删除redis再更新DB

```undefined
A_rm_redis
B_get_data
B_redis_miss
B_get_db
B_update_redis
A_update_db
```

此时redis是old值，db是new值

# 5.延迟双删

即

```undefined
rm_redis
update_db
sleep xxx ms
rm_redis
```

这样叫做双删，最后一次sleep一段时间再rm_redis保证再次读请求回溯打到db，用最新值写redis

# 6.思考变种

上面的3和5情况可以直接变种，即

```undefined
update_db
sleep xxx ms
rm_redis
```

解决了3中的极端情况（靠sleep解决），
 并且减少5中第一次不必要的rm redis请求
 当然，这个rm_redis还可以考虑异步化（提高吞吐）以及重试（避免异步处理失败），这里不展示

# 总结

从db回源到redis，需要考虑上面这些极端情况的case

## 适用场景

当然这些极端情况本身要求同一个key是多写的，这个根据业务需求来看是否需要，比如某些场景本身就是写少读多的

最终从网上看到的延迟双删变种为延迟删除redis也是一种优化