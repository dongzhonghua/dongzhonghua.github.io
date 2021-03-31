## 一。基本概念

-   Channel：是个     facade，主要成员变量：java.nio.channels.Channel、Pipeline、Unsafe     及 EventLoop。
-   EventLoop：IO 操作执行线程，主要成员变量：java.nio.channels.Selector     和 Task-Queue。EventLoop 与     Channel 的数量关系是 1:N。
-   Pipeline &     ChannelHandler：类似 j2ee 中 filter 机制，负责处理编解码及业务逻辑。Netty 把     ChannelHandler 封装为 ChannelHandlerContext 放在     Pipeline 的 head、tail 链表(正序链表、逆序链表)中;其中，IO 触发(eg:accept/read     等等)从 head 开始执行，用户发起     IO(eg:bind/connect/write 等)从 tail 开始执行。
-   Unsafe：非字面不安全意思，实际是指 Netty     的内部接口，不应该被外部直接调用。代理 Channel 中 IO 相关的操作。
-   Promise：相当于可设置结果的     Future。
-   ByteBuf：加强版的     ByteBuffer，支持自动扩容、Buffer 缓冲池等功能。

## 二。Netty 线程模型：EventLoop

### 1.Server&Client 工作流程图

-   Server



![netty监听流程](https://raw.githubusercontent.com/dongzhonghua/dongzhonghua.github.io/master/img/blog/netty监听流程.png)