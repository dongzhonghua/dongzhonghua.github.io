[TOC]

# 使用nettty来实现一个简单的RPC

## TODO
- [ ] 客户端获取结果有没有一个更好的办法，去看看掘金小册。

- [ ] future的实现原理？有没有更好的future的实现？

    这里好像是一个可行的解决方案https://github.com/Snailclimb/guide-rpc-framework/blob/master/docs/%E4%BD%BF%E7%94%A8CompletableFuture%E4%BC%98%E5%8C%96%E6%8E%A5%E5%8F%97%E6%9C%8D%E5%8A%A1%E6%8F%90%E4%BE%9B%E7%AB%AF%E8%BF%94%E5%9B%9E%E7%BB%93%E6%9E%9C.md

- [ ] 代理工厂那个地方实现的还是不够优雅
- [ ] zookeeper注册中心等
- [ ] 加入更多的rpc的功能？

## 原理
RPC(remote process call), 远程过程调用。它主要实现的功能就是调用另外一个进程的函数但是像是在调用本地的一样。既然是跨进程通信，我们自然就想到了利用socket来进行通信。只要把调用的信息封装起来，通过socket传到另一个进行然后解码，通过代理调用函数就可以完成整个过程。其中最重要的也就是socket通信的部分，使用netty可以非常方便的实现socket通信。

广义的来讲一个完整的 RPC 包含了很多组件，包括服务发现，服务治理，远程调用，调用链分析，网关等等。今天先从一个简单的demo做起。



![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/myrpc%E6%A1%86%E6%9E%B6.png)

1. client 会调用本地动态代理 proxy
2. 这个代理会将调用通过协议转序列化字节流
3. 通过 netty 网络框架，将字节流发送到服务端
4. 服务端在受到这个字节流后，会根据协议，反序列化为原始的调用，利用反射原理调用服务方提供的方法
5. 如果请求有返回值，又需要把结果根据协议序列化后，再通过 netty 返回给调用方

代码地址:  https://github.com/dongzhonghua/my-rpc.git

## 协议

rpc的协议主要是考虑如何把一次rpc调用过程描述清楚，利用socket通信，rpc调用过程需要编程字节流传输，所以需要还需要编解码。

写一部分主要定义：

1. 请求和相应格式
2. 编解码器
3. 序列化方式

## 服务器端

服务器端使用netty就可以

```java
package xyz.dsvshx.server.netty;

import javax.annotation.PreDestroy;

import org.springframework.beans.factory.InitializingBean;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import io.netty.bootstrap.ServerBootstrap;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.ChannelPipeline;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioServerSocketChannel;
import io.netty.handler.codec.LengthFieldBasedFrameDecoder;
import lombok.extern.slf4j.Slf4j;
import xyz.dsvshx.common.protocol.RpcDecoder;
import xyz.dsvshx.common.protocol.RpcEncoder;
import xyz.dsvshx.common.protocol.RpcRequest;
import xyz.dsvshx.common.protocol.RpcResponse;
import xyz.dsvshx.common.protocol.serialize.JSONSerializer;

/**
 * @author dongzhonghua
 * Created on 2021-03-03
 */
@Component
@Slf4j
public class NettyServer implements InitializingBean {
    private EventLoopGroup boss;
    private EventLoopGroup worker;
    @Autowired
    private ServerHandler serverHandler;

    @Override
    public void afterPropertiesSet() throws Exception {
        // 这种方式启动会不会有问题啊，有可能还没有启动起来但是服务已经来了
        start();
    }

    private void start() {
        boss = new NioEventLoopGroup();
        worker = new NioEventLoopGroup();
        ServerBootstrap serverBootstrap = new ServerBootstrap();
        serverBootstrap.group(boss, worker)
                .channel(NioServerSocketChannel.class)
                .option(ChannelOption.SO_BACKLOG, 1024)
                .childHandler(new ChannelInitializer<SocketChannel>() {
                    @Override
                    protected void initChannel(SocketChannel ch) throws Exception {
                        ChannelPipeline pipeline = ch.pipeline();
                        pipeline.addLast(new LengthFieldBasedFrameDecoder(65535, 0, 4));
                        pipeline.addLast(new RpcEncoder(RpcResponse.class, new JSONSerializer()));
                        pipeline.addLast(new RpcDecoder(RpcRequest.class, new JSONSerializer()));
                        pipeline.addLast(serverHandler);

                    }
                });
        bind(serverBootstrap, 8888);
    }

    /**
     * 如果端口绑定失败，端口数+1,重新绑定
     */
    private void bind(final ServerBootstrap serverBootstrap, int port) {
        serverBootstrap.bind(port).addListener(future -> {
            if (future.isSuccess()) {
                log.info("端口[ {} ] 绑定成功", port);
            } else {
                log.error("端口[ {} ] 绑定失败", port);
                bind(serverBootstrap, port + 1);
            }
        });
    }

    @PreDestroy
    public void destory() throws InterruptedException {
        boss.shutdownGracefully().sync();
        worker.shutdownGracefully().sync();
        log.info("关闭Netty");
    }
}
```

```java
package xyz.dsvshx.server.netty;

import java.lang.reflect.InvocationTargetException;

import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.stereotype.Component;

import io.netty.channel.ChannelHandler;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.SimpleChannelInboundHandler;
import lombok.extern.slf4j.Slf4j;
import xyz.dsvshx.common.protocol.RpcRequest;
import xyz.dsvshx.common.protocol.RpcResponse;
import xyz.dsvshx.server.proxy.CglibProxy;

/**
 * @author dongzhonghua
 * Created on 2021-03-03
 */
@Component
@Slf4j
@ChannelHandler.Sharable
public class ServerHandler extends SimpleChannelInboundHandler<RpcRequest> implements ApplicationContextAware {
    private ApplicationContext applicationContext;

    @Override
    protected void channelRead0(ChannelHandlerContext ctx, RpcRequest rpcRequest) throws Exception {
        RpcResponse rpcResponse = new RpcResponse();
        rpcResponse.setRequestId(rpcRequest.getRequestId());
        try {
            Object handler = handler(rpcRequest);
            log.info("获取返回结果: {} ", handler);
            rpcResponse.setResult(handler);
        } catch (Throwable throwable) {
            rpcResponse.setError(throwable.toString());
            throwable.printStackTrace();
        }
        ctx.writeAndFlush(rpcResponse);
    }

    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        this.applicationContext = applicationContext;
    }

    /**
     * 服务端使用代理处理请求
     */
    // private Object handler(RpcRequest request) throws ClassNotFoundException, InvocationTargetException {
    //     //使用Class.forName进行加载Class文件
    //     Class<?> clazz = Class.forName(request.getClassName());
    //     Object serviceBean = applicationContext.getBean(clazz);
    //     log.info("serviceBean: {}", serviceBean);
    //     Class<?> serviceClass = serviceBean.getClass();
    //     log.info("serverClass:{}", serviceClass);
    //     String methodName = request.getMethodName();
    //
    //     Class<?>[] parameterTypes = request.getParameterTypes();
    //     Object[] parameters = request.getParameters();
    //
    //     //使用CGLIB Reflect
    //     FastClass fastClass = FastClass.create(serviceClass);
    //     FastMethod fastMethod = fastClass.getMethod(methodName, parameterTypes);
    //     log.info("开始调用CGLIB动态代理执行服务端方法...");
    //     return fastMethod.invoke(serviceBean, parameters);
    // }

    private Object handler(RpcRequest request) throws ClassNotFoundException, InvocationTargetException {
        Class<?> clazz = Class.forName(request.getClassName());
        Object serviceBean = applicationContext.getBean(clazz);
        log.info("调用的serviceBean:{}", serviceBean);
        Class<?> serviceClass = serviceBean.getClass();
        log.info("调用的serviceClass name:{}", serviceClass);
        String methodName = request.getMethodName();
        log.info("调用的方法 name:{}", methodName);
        Class<?>[] parameterTypes = request.getParameterTypes();
        Object[] parameters = request.getParameters();
        // 使用cglib
        log.info("开始调用CGLIB动态代理执行服务端方法...");
        return new CglibProxy().invoke(serviceClass, methodName, parameterTypes, parameters);
    }
}
```



值得一提的是服务器端在收到相应之后需要调用相应的函数，所以需要使用代理对象来调用，这里使用Cglib代理，客户端使用Jdk动态代理：

```java
package xyz.dsvshx.server.proxy;

import java.lang.reflect.Method;

import org.springframework.cglib.proxy.Enhancer;
import org.springframework.cglib.proxy.MethodInterceptor;
import org.springframework.cglib.proxy.MethodProxy;

import lombok.extern.slf4j.Slf4j;
import xyz.dsvshx.server.HelloServiceImpl;

/**
 * @author dongzhonghua
 * Created on 2021-03-03
 */

@Slf4j
public class CglibProxy implements MethodInterceptor {


    public Object invoke(Class<?> clazz, String methodName, Class<?>[] parameterTypes, Object[] parameters) {
        //使用cglib生成代理
        //1.创建核心类
        Enhancer enhancer = new Enhancer();
        //2.为哪个类生成代理
        enhancer.setSuperclass(clazz);
        //3.设置回调，相当于JDK动态代理中的invoke方法
        enhancer.setCallback(this);
        //4.创建代理对象并执行方法
        Method method;
        Object result = null;
        try {
            Object proxy = enhancer.create();
            method = proxy.getClass().getMethod(methodName, parameterTypes);
            method.setAccessible(true);
            result = method.invoke(proxy, parameters);
        } catch (Exception e) {
            log.info("方法调用失败");
            e.printStackTrace();
        }
        return result;
    }

    @Override
    public Object intercept(Object proxy, Method method, Object[] args,
            MethodProxy methodProxy) throws Throwable {
        log.info("调用代理对象方法：{}#{}", proxy, method);
        //调用代理对象的方法，相当也调用父类的方法
        return methodProxy.invokeSuper(proxy, args);
    }

    public static void main(String[] args) {
        Class<String> stringClass = String.class;
        Class<?>[] classes = new Class[1];
        classes[0] = stringClass;
        Object[] o = new Object[1];
        o[0] = "xxxx";
        Object sayHello = new CglibProxy().invoke(HelloServiceImpl.class, "sayHello", classes, o);
        System.out.println(sayHello);
    }
}
```

## 客户端

客户端的主要代码如下：

```java
package xyz.dsvshx.client.netty;

import java.util.Date;
import java.util.concurrent.TimeUnit;

import javax.annotation.PreDestroy;

import io.netty.bootstrap.Bootstrap;
import io.netty.channel.Channel;
import io.netty.channel.ChannelFuture;
import io.netty.channel.ChannelInitializer;
import io.netty.channel.ChannelOption;
import io.netty.channel.ChannelPipeline;
import io.netty.channel.EventLoopGroup;
import io.netty.channel.nio.NioEventLoopGroup;
import io.netty.channel.socket.SocketChannel;
import io.netty.channel.socket.nio.NioSocketChannel;
import lombok.extern.slf4j.Slf4j;
import xyz.dsvshx.common.protocol.RpcDecoder;
import xyz.dsvshx.common.protocol.RpcEncoder;
import xyz.dsvshx.common.protocol.RpcRequest;
import xyz.dsvshx.common.protocol.RpcResponse;
import xyz.dsvshx.common.protocol.serialize.JSONSerializer;

/**
 * @author dongzhonghua
 * Created on 2021-03-03
 */
@Slf4j
public class NettyClient {
    private EventLoopGroup eventLoopGroup;
    private Channel channel;
    private ClientHandler clientHandler;
    private String host;
    private Integer port;
    private static final int MAX_RETRY = 5;
    private static final int TIMEOUT = 5000;


    public NettyClient(String host, Integer port) {
        this.host = host;
        this.port = port;
    }

    public void connect() {
        clientHandler = new ClientHandler();
        eventLoopGroup = new NioEventLoopGroup();
        //启动类
        Bootstrap bootstrap = new Bootstrap();
        bootstrap.group(eventLoopGroup)
                //指定传输使用的Channel
                .channel(NioSocketChannel.class)
                .option(ChannelOption.SO_KEEPALIVE, true)
                .option(ChannelOption.TCP_NODELAY, true)
                .option(ChannelOption.CONNECT_TIMEOUT_MILLIS, TIMEOUT)
                .handler(new ChannelInitializer<SocketChannel>() {
                    @Override
                    protected void initChannel(SocketChannel ch) throws Exception {
                        ChannelPipeline pipeline = ch.pipeline();
                        //添加编码器
                        pipeline.addLast(new RpcEncoder(RpcRequest.class, new JSONSerializer()));
                        //添加解码器
                        pipeline.addLast(new RpcDecoder(RpcResponse.class, new JSONSerializer()));
                        //请求处理类
                        pipeline.addLast(clientHandler);
                    }
                });
        connect(bootstrap, host, port, MAX_RETRY);
    }

    /**
     * 失败重连机制，参考Netty入门实战掘金小册
     */
    private void connect(Bootstrap bootstrap, String host, int port, int retry) {
        ChannelFuture channelFuture = bootstrap.connect(host, port).addListener(future -> {
            if (future.isSuccess()) {
                log.info("连接服务端成功");
            } else if (retry == 0) {
                log.error("重试次数已用完，放弃连接");
            } else {
                //第几次重连：
                int order = (MAX_RETRY - retry) + 1;
                //本次重连的间隔
                int delay = 1 << order;
                log.error("{} : 连接失败，第 {} 重连....", new Date(), order);
                bootstrap.config().group()
                        .schedule(() -> connect(bootstrap, host, port, retry - 1), delay, TimeUnit.SECONDS);
            }
        });
        channel = channelFuture.channel();
    }

    /**
     * 发送消息
     */
    public RpcResponse send(final RpcRequest request) {
        try {
            channel.writeAndFlush(request).await();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        return clientHandler.getRpcResponse(request.getRequestId());
    }

    @PreDestroy
    public void close() {
        eventLoopGroup.shutdownGracefully();
        channel.closeFuture().syncUninterruptibly();
    }
}
```

```java
package xyz.dsvshx.client.netty;

import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

import io.netty.channel.ChannelDuplexHandler;
import io.netty.channel.ChannelHandler.Sharable;
import io.netty.channel.ChannelHandlerContext;
import io.netty.channel.ChannelPromise;
import lombok.extern.slf4j.Slf4j;
import xyz.dsvshx.client.future.DefaultFuture;
import xyz.dsvshx.common.protocol.RpcRequest;
import xyz.dsvshx.common.protocol.RpcResponse;

/**
 * @author dongzhonghua
 * Created on 2021-03-03
 */
@Sharable
@Slf4j
public class ClientHandler extends ChannelDuplexHandler {
    /**
     * 使用Map维护请求对象ID与响应结果Future的映射关系
     */
    private final Map<String, DefaultFuture> futureMap = new ConcurrentHashMap<>();

    @Override
    public void channelRead(ChannelHandlerContext ctx, Object msg) throws Exception {
        if (msg instanceof RpcResponse) {
            //获取响应对象
            RpcResponse response = (RpcResponse) msg;
            DefaultFuture defaultFuture = futureMap.get(response.getRequestId());
            defaultFuture.setResponse(response);
        }
        super.channelRead(ctx, msg);
    }
    //一开始写成read了，这两个方法有什么区别吗？
    // @Override
    // public void read(ChannelHandlerContext msg) throws Exception {
    //     if (msg instanceof RpcResponse) {
    //         //获取响应对象
    //         RpcResponse response = (RpcResponse) msg;
    //         log.info("client response:{}", response);
    //         DefaultFuture defaultFuture =
    //                 futureMap.get(response.getRequestId());
    //         //将结果写入DefaultFuture
    //         defaultFuture.setResponse(response);
    //     }
    //     super.read(msg);
    // }

    @Override
    public void write(ChannelHandlerContext ctx, Object msg, ChannelPromise promise) throws Exception {
        if (msg instanceof RpcRequest) {
            RpcRequest request = (RpcRequest) msg;
            //发送请求对象之前，先把请求ID保存下来，并构建一个与响应Future的映射关系
            futureMap.putIfAbsent(request.getRequestId(), new DefaultFuture());
        }
        super.write(ctx, msg, promise);
    }

    public RpcResponse getRpcResponse(String requestId) {
        try {
            DefaultFuture future = futureMap.get(requestId);
            return future.getRpcResponse(10);
        } finally {
            //获取成功以后，从map中移除
            futureMap.remove(requestId);
        }
    }
}
```

客户端的调用也是使用了代理，在代理对象里通过socket请求到结果返回：

```java
package xyz.dsvshx.client.proxy;

import java.lang.reflect.InvocationHandler;
import java.lang.reflect.Method;
import java.util.Date;
import java.util.UUID;

import lombok.extern.slf4j.Slf4j;
import xyz.dsvshx.client.netty.NettyClient;
import xyz.dsvshx.common.protocol.RpcRequest;
import xyz.dsvshx.common.protocol.RpcResponse;

/**
 * @author dongzhonghua
 * Created on 2021-03-03
 */
@Slf4j
public class RpcClientJdkDynamicProxy<T> implements InvocationHandler {
    private Class<T> clazz;

    public RpcClientJdkDynamicProxy(Class<T> clazz) throws Exception {
        this.clazz = clazz;
    }

    @Override
    public Object invoke(Object proxy, Method method, Object[] args) throws Throwable {
        RpcRequest request = new RpcRequest();
        String requestId = UUID.randomUUID().toString();

        String className = method.getDeclaringClass().getName();
        String methodName = method.getName();

        Class<?>[] parameterTypes = method.getParameterTypes();

        request.setRequestId(requestId);
        request.setClassName(className);
        request.setMethodName(methodName);
        request.setParameterTypes(parameterTypes);
        request.setParameters(args);
        log.info("请求内容: {}", request);
        //开启Netty 客户端，直连
        NettyClient nettyClient = new NettyClient("127.0.0.1", 8888);
        log.info("开始连接服务端：{}", new Date());
        nettyClient.connect();
        // TODO: 2021/3/3 有时候还没连接完就开始发送，导致失败，这种情况有没有解决方案？
        // while (!nettyClient.getIsConnected()) {
        //     log.info("获取连接状态:{}", nettyClient.getIsConnected());
        //     Thread.sleep(100);
        // }
        Thread.sleep(3000);
        RpcResponse send = nettyClient.send(request);
        log.info("请求调用返回结果：{}", send.getResult());
        return send.getResult();
    }
}
```

客户端的调用如下：

```java
package xyz.dsvshx.client;


import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.context.ApplicationContext;

import lombok.extern.slf4j.Slf4j;
import xyz.dsvshx.common.service.HelloService;

/**
 * @author dongzhonghua
 * Created on 2021-03-03
 */
@SpringBootApplication
@Slf4j
public class ClientApplication {
    public static void main(String[] args) throws Exception {
        ApplicationContext ctx = SpringApplication.run(ClientApplication.class, args);

        HelloService helloService = ctx.getBean(HelloService.class);
        System.out.println(helloService.sayHello("xxxxxxxxx"));
    }
}
```

## 注册中心

使用zk作为注册中心。

为什么要选用注册中心

假设没有注册中心，采用直连的方式，如果服务提供者发生变化，那么消费者也要立即更新，耦合度太高

zk作为服务注册的一个框架，消费者只需要向注册中心获取服务提供者的地址，无需自己做更新。达到了**解耦合**的作用，而且还能实现**服务的自动发现**。



XXL-RPC中每个服务在zookeeper中对应一个节点，如图"iface name"节点，该服务的每一个provider机器对应"iface name"节点下的一个子节点，如图中"192.168.0.1:9999"、"192.168.0.2:9999"和"192.168.0.3:9999"，子节点类型为zookeeper的**EPHMERAL（临时节点）**类型，该类型节点有个特点，当机器和zookeeper集群断掉连接后节点将会被移除。consumer底层可以从zookeeper获取到可提供服务的provider集群地址列表，从而可以向其中一个机器发起RPC调用。zk的注册中心类提供了一系列的方法，并通过定义的zkclient类来操作zk，创建和更新节点，这样就可以完成注册的功能

## 心跳机制

netty可以加入心跳机制避免长时间没有发消息二断开连接。这里没有实现，具体可以参考：

https://www.cnblogs.com/rickiyang/p/12792120.html

## 通过spi加载具体实现

有时候，一个接口可能对应多个实现，比如服务注册可能有zk和nacos。那么如何在运行的时候知道加载哪一个呢？可以通过spi机制，把实现类通过配置文件确定下来。这里也没有具体的实现，具体可以参考guide哥的实现。

## 参考

本文主要参考以下博客，并做了一些改进。

> 主要参考：https://juejin.cn/post/6844903957622423560 博客写得比较详细
> 
> https://www.w3cschool.cn/architectroad/architectroad-rpc-framework.html
> 
> https://github.com/pjmike/springboot-rpc-demo
> 
> 提供了非常好的解决思路：https://xilidou.com/2018/09/26/dourpc-remoting/
>
> guide哥写的rpc:https://github.com/Snailclimb/guide-rpc-framework
>
> 一起写个dubbo：https://blog.csdn.net/qq_40856284/category_10138756.html