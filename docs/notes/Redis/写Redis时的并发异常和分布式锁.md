最近公司里有一个并发业务。多个线程消费一个kafka数据流，这个kafka数据流里数据的某个字段有重复。需要根据这个字段来做下去重。

一开始的方案是利用Redis来实现，先查Redis如果没有的话则setex。后来发现这个并不能保证并发安全性，后来的结果还是有重复的数据。

经过分析，发现是有的重复数据相隔极短。比如说A1和A2两条数据。如果A1 get不到，则说明没有，这个时候去写redis。但是还没写进去呢。A2也去get，如果A1还没写进去的话，A2就get不到。这个时候就出现了并发不安全了。

解决方案就是用redis另一个函数。类似于分布式锁的方式。

```java
set(key, value, "NX", "EX", expireSeconds);  // SET IF NOT EXIST，而且还是原子的
// 操作成功，返回“OK”，否则返回null
```

如果此时返回ok，就说明这个数据不重复，如果返回null，就说明数据不重复。

看jedis的set函数

```java
  /**
   * Set the string value as value of the key. The string can't be longer than 1073741824 bytes (1
   * GB).
   * @param key
   * @param value
   * @param nxxx NX|XX, NX -- Only set the key if it does not already exist. XX -- Only set the key
   *          if it already exist.
   * @param expx EX|PX, expire time units: EX = seconds; PX = milliseconds
   * @param time expire time in the units of <code>expx</code>
   * @return Status code reply
   */
  public String set(final String key, final String value, final String nxxx, final String expx,
      final long time) {
    checkIsInMultiOrPipeline();
    client.set(key, value, nxxx, expx, time);
    return client.getStatusCodeReply();
  }
```

对应的Redis命令如下

```shell
SET resource_name my_random_value NX PX 30000
```

该命令仅在密钥不存在（NX选项）且到期时间为30000毫秒（PX选项）时才设置密钥。密钥设置为“我的*随机*值”。该值在所有客户端和所有锁定请求中必须唯一。

基本上，使用随机值是为了以安全的方式释放锁，并且脚本会告诉Redis：仅当密钥存在且存储在密钥上的值恰好是我期望的值时，才删除该密钥。这是通过以下Lua脚本完成的：

```lua
if redis.call("get",KEYS[1]) == ARGV[1] then
    return redis.call("del",KEYS[1])
else
    return 0
end
```

为了避免删除另一个客户端创建的锁，这一点很重要。例如，一个客户端可能获取了该锁，在某些操作中被阻塞的时间超过了该锁的有效时间（密钥将过期的时间），然后又删除了某个其他客户端已经获取的锁。仅使用DEL是不安全的，因为一个客户端可能会删除另一个客户端的锁。使用上述脚本时，每个锁都由一个随机字符串“签名”，因此仅当该锁仍是客户端尝试将其删除时设置的锁时，该锁才会被删除。