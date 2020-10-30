[TOC]

## Instrument

Instrumentation是Java提供的一个来自JVM的接口，该接口提供了一系列查看和操作Java类定义的方法，例如修改类的字节码、向classLoader的classpath下加入jar文件等。使得开发者可以通过Java语言来操作和监控JVM内部的一些状态，进而实现Java程序的监控分析，甚至实现一些特殊功能（如AOP、热部署）。

基于 Instrumentation 来实现的有：

```
APM 产品: pinpoint、skywalking、newrelic、听云的 APM 产品等都基于 Instrumentation 实现

热部署工具：Intellij idea 的 HotSwap、Jrebel 等

Java 诊断工具：Arthas、Btrace 等
```

由于对字节码修改功能的巨大需求，JDK 从 JDK5 版本开始引入了`java.lang.instrument` 包。它可以通过 addTransformer 方法设置一个 ClassFileTransformer，可以在这个 ClassFileTransformer 实现类的转换。

JDK 1.5 支持静态 Instrumentation，基本的思路是在 JVM 启动的时候添加一个代理（javaagent），每个代理是一个 jar 包，其 MANIFEST.MF 文件里指定了代理类，这个代理类包含一个 premain 方法。JVM 在类加载时候会先执行代理类的 premain 方法，再执行 Java 程序本身的 main 方法，这就是 premain 名字的来源。在 premain 方法中可以对加载前的 class 文件进行修改。这种机制可以认为是虚拟机级别的 AOP，无需对原有应用做任何修改，就可以实现类的动态修改和增强。

从 JDK 1.6 开始支持更加强大的动态 Instrument，在JVM 启动后通过 Attach API 远程加载。

![instrumentation使用场景和流程.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/instrumentation使用场景和流程.png)

```java
public interface Instrumentation {
    /**
     * 注册一个Transformer，从此之后的类加载都会被Transformer拦截。
     * Transformer可以直接对类的字节码byte[]进行修改
     */
    void addTransformer(ClassFileTransformer transformer);
    
    /**
     * 对JVM已经加载的类重新触发类加载。使用的就是上面注册的Transformer。
     * retransformation可以修改方法体，但是不能变更方法签名、增加和删除方法/类的成员属性
     */
    void retransformClasses(Class<?>... classes) throws UnmodifiableClassException;
    
    /**
     * 获取一个对象的大小
     */
    long getObjectSize(Object objectToSize);
    
    /**
     * 将一个jar加入到bootstrap classloader的 classpath里
     */
    void appendToBootstrapClassLoaderSearch(JarFile jarfile);
    
    /**
     * 获取当前被JVM加载的所有类对象
     */
    Class[] getAllLoadedClasses();
}
```
其中最常用的方法就是addTransformer(ClassFileTransformer transformer)了，这个方法可以在类加载时做拦截，对输入的类的字节码进行修改，其参数是一个ClassFileTransformer接口，定义如下：

```java
/**
 * 传入参数表示一个即将被加载的类，包括了classloader，classname和字节码byte[]
 * 返回值为需要被修改后的字节码byte[]
 */
byte[] transform(ClassLoader loader,
            String className,
            Class<?> classBeingRedefined,
            ProtectionDomain protectionDomain,
            byte[] classfileBuffer)  
            throws IllegalClassFormatException;
```
addTransformer方法配置之后，后续的类加载都会被Transformer拦截。对于已经加载过的类，可以执行retransformClasses来重新触发这个Transformer的拦截。类加载的字节码被修改后，除非再次被retransform，否则不会恢复。

主流的JVM都提供了Instrumentation的实现，但是鉴于Instrumentation的特殊功能，并不适合直接提供在JDK的runtime里，而更适合出现在Java程序的外层，以上帝视角在合适的时机出现。因此如果想使用Instrumentation功能，拿到Instrumentation实例，我们必须通过Java agent。

## agent

Java agent是一种特殊的Java程序（Jar文件），它是Instrumentation的客户端。与普通Java程序通过main方法启动不同，agent并不是一个可以单独启动的程序，而必须依附在一个Java应用程序（JVM）上，与它运行在同一个进程中，通过Instrumentation API与虚拟机交互。

Java agent与Instrumentation密不可分，二者也需要在一起使用。因为Instrumentation的实例会作为参数注入到Java agent的启动方法中。

Java agent以jar包的形式部署在JVM中，jar文件的manifest需要指定agent的类名。根据不同的启动时机，agent类需要实现不同的方法（二选一）。
```java
/**
 * 以vm参数的形式载入，在程序main方法执行之前执行
 * 其jar包的manifest需要配置属性Premain-Class
 */
public static void premain(String agentArgs, Instrumentation inst);
/**
 * 以Attach的方式载入，在Java程序启动后执行
 * 其jar包的manifest需要配置属性Agent-Class
 */
public static void agentmain(String agentArgs, Instrumentation inst);
```



如果想自己写一个java agent程序，只需定义一个包含premain或者agentmain的类，在方法中实现你的逻辑，然后在打包jar时配置一下manifest即可。可以参考如下的maven plugin配置：

```xml
<plugin>
    <artifactId>maven-assembly-plugin</artifactId>
    <configuration>
        <archive>
            <manifestEntries>
                <Premain-Class>**.**.InstrumentTest</Premain-Class>
                <Agent-Class>**.**..InstrumentTest</Agent-Class>
                <Can-Redefine-Classes>true</Can-Redefine-Classes>
                <Can-Retransform-Classes>true</Can-Retransform-Classes>
            </manifestEntries>
        </archive>
    </configuration>
</plugin>
```

### agent加载

一个Java agent既可以在VM启动时加载，也可以在VM启动后加载：

- 启动时加载：通过vm的启动参数-javaagent:**.jar来启动
- 启动后加载：启动时加载是有一定的缺点的，因为项目在一开始运行的时候不知道到底要不要使用agent，所以jdk1.6之后可以在vm启动后的任何时间点，通过attach api，动态地启动agent

agent加载时，Java agent的jar包先会被加入到system class path中，然后agent的类会被system class loader加载。没错，这个system class loader就是所在的Java程序的class loader，这样agent就可以很容易的获取到想要的class。

对于VM启动时加载的Java agent，其premain方法会在程序main方法执行之前被调用，此时大部分Java类都没有被加载（“大部分”是因为，agent类本身和它依赖的类还是无法避免的会先加载的），是一个对类加载埋点做手脚（addTransformer）的好机会。如果此时premain方法执行失败或抛出异常，那么JVM的启动会被终止。

对于VM启动后加载的Java agent，其agentmain方法会在加载之时立即执行。如果agentmain执行失败或抛出异常，JVM会忽略掉错误，不会影响到正在running的Java程序。
![java的agent加载过程.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/java的agent加载过程.png)



### agent premain举例

举例，我想要监听某个类，并对这个类的每个方法都做一层AOP，打印出方法调用的耗时。那么使用Instrumentation的解决方式，就是修改这个类的字节码，对每个方法作如下改动：

```java
// 原方法
public void method1(){
    dosomething();
}
    ↓ ↓ ↓ ↓ ↓
// 修改后的方法
public void method1(){
    long stime = System.currentTimeMillis();
    dosomething();
    System.out.println("method1 cost:" + (System.currentTimeMillis() - stime) + " ms");
}
```

  要想实现这种效果，我们需要在transform方法的实现中，对指定的类，做指定的字节码增强。通常来说，做字节码增强都需要使用到框架，比如ASM,CGLIB,Byte Buddy,Javassist。不过如果你喜欢，你可以直接用位运算操作byte[]，不需要任何框架，例如JDK反射(method.invoke())的实现，就真的是用位操作拼装了一个类。
  言归正传，操作字节码的高手可能更喜欢ASM，因为它提供的方法更底层，功能更强大更直白。对于字节码不熟悉的开发者，更适合javassist，它可以直接以Java代码方式直接修改方法体。我们以javassist为例，看看怎么实现上述的功能。

```java
public class AgentTest {
    public static void premain(String agentOps, Instrumentation inst) {

        System.out.println("=========premain方法执行========");
        // 添加Transformer
        inst.addTransformer(new MyTransformer());
        System.out.println(agentOps);
    }

    public static void main(String[] args) throws InterruptedException {
        System.out.println("=======main方法执行=========");
    }

}
```

```java
public class MyTransformer implements ClassFileTransformer {

    final static String prefix = "\nlong startTime = System.currentTimeMillis();\n";
    final static String postfix = "\nlong endTime = System.currentTimeMillis();\n";

    // 被处理的方法列表
    final static Map<String, List<String>> methodMap = new HashMap<>();

    public MyTransformer() {
        add("dsvshx.agent.TimeTest.sayHello");
        add("dsvshx.agent.TimeTest.sayHello2");
    }

    private void add(String methodString) {
        String className = methodString.substring(0, methodString.lastIndexOf("."));
        String methodName = methodString.substring(methodString.lastIndexOf(".") + 1);
        List<String> list = methodMap.computeIfAbsent(className, k -> new ArrayList<>());
        list.add(methodName);
    }

    @Override
    public byte[] transform(ClassLoader loader, String className, Class<?> classBeingRedefined,
            ProtectionDomain protectionDomain, byte[] classfileBuffer) {
        className = className.replace("/", ".");
        if (methodMap.containsKey(className)) {// 判断加载的class的包路径是不是需要监控的类
            CtClass ctclass;
            try {
                ctclass = ClassPool.getDefault().get(className);// 使用全称,用于取得字节码类<使用javassist>
                for (String methodName : methodMap.get(className)) {
                    String outputStr = "\nSystem.out.println(\"this method " + methodName
                            + " cost:\" +(endTime - startTime) +\"ms.\");";

                    CtMethod ctmethod = ctclass.getDeclaredMethod(methodName);// 得到这方法实例
                    String newMethodName = methodName + "$old";// 新定义一个方法叫做比如sayHello$old
                    ctmethod.setName(newMethodName);// 将原来的方法名字修改

                    // 创建新的方法，复制原来的方法，名字为原来的名字
                    CtMethod newMethod = CtNewMethod.copy(ctmethod, methodName, ctclass, null);

                    // 构建新的方法体
                    String bodyStr = "{"
                            + prefix
                            + newMethodName + "($$);\n"// 调用原有代码，类似于method();($$)表示所有的参数
                            + postfix
                            + outputStr
                            + "}";
                    newMethod.setBody(bodyStr);// 替换新方法
                    ctclass.addMethod(newMethod);// 增加新方法
                }
                return ctclass.toBytecode();
            } catch (Exception e) {
                System.out.println(e.getMessage());
                e.printStackTrace();
            }
        }
        return null;
    }
}
```

测试类：

```Java
public class TimeTest {

    public static void main(String[] args) {
        sayHello();
        sayHello2("hello world222222222");
    }

    public static void sayHello() {
        try {
            Thread.sleep(2000);
            System.out.println("hello world!!");
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

    public static void sayHello2(String hello) {
        try {
            Thread.sleep(1000);
            System.out.println(hello);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }
}
```

使用方式，`<Main-Class>xxx.TimeTest</Main-Class>`，指定入口，然后打包成jar包，这几个文件可以放在一个项目里，命令以及结果

```shell
java -javaagent:xxx.jar=Hello1 -jar xxx.jar

=========premain方法执行========
Hello1
hello world!!
this method sayHello cost:2002ms.
hello world222222222
this method sayHello2 cost:1005ms.
```

## attach

上面提到，Java agent可以在JVM启动后再加载，就是通过Attach API实现的。当然，Attach API可不仅仅是为了实现动态加载agent，Attach API其实是跨JVM进程通讯的工具，能够将某种指令从一个JVM进程发送给另一个JVM进程。

加载agent只是Attach API发送的各种指令中的一种， 诸如jstack打印线程栈、jps列出Java进程、jmap做内存dump等功能，都属于Attach API可以发送的指令。

使用attach的方式，不需要实现premain函数，需要attachmain。

```Java
public void agentmain(String agentArgs, Instrumentation inst);
```

由于是进程间通讯，那代表着使用Attach API的程序需要是一个独立的Java程序，通过attach目标进程，与其进行通讯。下面的代码表示了向进程pid为1234的JVM发起通讯，加载一个名为agent.jar的Java agent。

```java
// VirtualMachine等相关Class位于JDK的tools.jar
VirtualMachine vm = VirtualMachine.attach("1234");  // 1234表示目标JVM进程pid
try {
    vm.loadAgent(".../agent.jar");    // 指定agent的jar包路径，发送给目标进程
} finally {
    vm.detach();
}
```

  vm.loadAgent之后，相应的agent就会被目标JVM进程加载，并执行agentmain方法。

### attach api原理

按惯例，以Hotspot虚拟机，Linux系统为例。当external process执行VirtualMachine.attach时，需要通过操作系统提供的进程通信方法，例如信号、socket，进行握手和通信。其具体内部实现流程如下所示：

| external process（attach发起的进程）                | target VM（目标JVM进程，假设pid为*XXX*）                     |
| --------------------------------------------------- | ------------------------------------------------------------ |
| 1. 创建文件：.attach_pid*XXX*                       |                                                              |
| 2. 检查.java_pid*XXX* 文件是否存在，如果存在则跳过4 |                                                              |
| 3. 向目标JVM发送SIGQUIT信号 →                       |                                                              |
| 4. 轮询等待.java_pid*XXX* 文件的创建（5秒超时）     | 1. JVM的Signal Dispatcher线程收到SIGQUIT信号                 |
| 4. 轮询等待 …………                                    | 2. 检查.attach_pid*XXX* 文件是否存在，若不存在则继续，否则忽略信号 |
| 4. 轮询等待 …………                                    | 2. 创建一个新线程Attach Listener，专门负责接收各种attach请求指令 |
| 4. 轮询等待 …………                                    | 3. 创建.java_pid*XXX*文件                                    |
| 4. 轮询等待 …………                                    | 4. 开始监听socket(. java_pid*XXX*)                           |
| 5. 尝试连接socket (.java_pid*XXX* )                 |                                                              |

上面提到了两个文件：

-   .attach_pid*XXX* 后面的XXX代表pid，例如pid为1234则文件名为.attach_pid1234。该文件目的是给目标JVM一个标记，表示触发SIGQUIT信号的是attach请求。这样目标JVM才可以把SIGQUIT信号当做attach连接请求，再来做初始化。其默认全路径为/proc/*XXX*/cwd/.attach_pid*XXX*，若创建失败则使用/tmp/attach_pid*XXX*
-   .java_pid*XXX* 后面的XXX代表pid，例如pid为1234则文件名为.java_pid1234。由于Unix domain socket通讯是基于文件的，该文件就是表示external process与target VM进行socket通信所使用的文件，如果存在说明目标JVM已经做好连接准备。其默认全路径为/proc/*XXX*/cwd/.java_pid*XXX*，若创建失败则使用/tmp/java_pid*XXX*

VirtualMachine.attach动作类似TCP创建连接的三次握手，目的就是搭建attach通信的连接。而后面执行的操作，例如vm.loadAgent，其实就是向这个socket写入数据流，接收方target VM会针对不同的传入数据来做不同的处理。

参考：
[谈谈Java Intrumentation和相关应用](http://www.fanyilun.me/2017/07/18/%E8%B0%88%E8%B0%88Java%20Intrumentation%E5%92%8C%E7%9B%B8%E5%85%B3%E5%BA%94%E7%94%A8/)

https://www.cnblogs.com/aspirant/p/8796974.html
