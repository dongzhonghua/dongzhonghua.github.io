[TOC]



jvisualvm和jconsole都是JVM自带的强大的JVM分析工具。在命令行输入相应的命令就可以打开用户界面。

# jvisualvm

## 堆内存溢出
直接使用jvisualvm来分析一个堆内存溢出异常。
设置堆栈信息，设得小一点：`-Xms5m   -Xmx5m   -XX:+HeapDumpOnOutOfMemoryError`。这样很快就会有内存溢出了。
```java
import java.util.ArrayList;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        List<Main> list = new ArrayList<>();
        for( ; ; ) {
            list.add(new Main());

        }
    }
}
```
<img src="https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/oom界面.png" alt="oom界面.png" style="zoom:50%;" />
使用idea运行之后可以发现堆栈信息已经生成了，现在可以到jvisualvm里面导入。

导入之后的界面是这样的。
<img src="https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/jvvm界面.png" alt="jvvm界面.png" style="zoom:50%;" />
还可以看到类的信息。
<img src="https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/jvvm类信息.png" alt="jvvm类信息.png" style="zoom: 50%;" />


在这里我们就可以清晰的看出，因为该类实例太多占据97%，
通过分析每一个实例对象可以看到详细信息，比如该类是由Appclassloader加载的，其父是扩展类加载器，在往上是启动类加载器

![jvvm类具体信息.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/jvvm类具体信息.png)

他也可以进行监控，可以手动执行垃圾回收和dump。
![jvvm监控.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/jvvm监控.png)

## 栈内存溢出
设置栈内存为最小值160k方便快速看到效果 `-Xss160k`

```java
 public class Main {
    private int time;

    public int gettime() {
        return time;
    }

    public void goon() {
        this.time++;
        try {
            Thread.sleep(40);   //防止主线程结束太快，不好监测
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        goon();
    }

    public static void main(String[] args) {
        Main jtext2 = new Main();
        try {
            jtext2.goon();
        } catch (Throwable e) {
            System.out.println(jtext2.gettime());
            e.printStackTrace();
        }
    }
}
```
可以看到，函数循环调用了七百多次之后发生了栈内存溢出。
![栈溢出报错.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/栈溢出报错.png)

使用jvisualvm查看线程dump

![栈溢出报错dump.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/栈溢出报错dump.png)

可以看到main线程的调用堆栈和状态。这样可以初步排查到问题。

## 死锁检测
```java
public class Main {
    public static void main(String[] args) {
        new Thread(new A(), "Thread-A").start();
        new Thread(new B(), "Thread-B").start();

        try {
            Thread.sleep(50000);//不让main线程快速结束，以便进行线程dunmp
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
    }

}

class A implements Runnable {
    private static final Object lock1 = new Object();
    public static void amethod() {
        synchronized (lock1) {
            System.out.println("进入A");
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            B.bmethod();
        }
    }

    @Override
    public void run() {
        amethod();
    }
}

class B implements Runnable {
    private static final Object lock2 = new Object();

    public static void bmethod() {
        synchronized (lock2) {
            System.out.println("进入B");
            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            A.amethod();
        }
    }

    @Override
    public void run() {
        bmethod();
    }
}
```

![jvvm死锁检测.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/jvvm死锁检测.png)


![死锁dump信息.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/死锁dump信息.png)


# jconsole
jconsole和jvisualvm类似。我们用jconsole分析一下元空间（方法区）的内存溢出。

> 在 Java 虚拟机（以下简称JVM）中，类包含其对应的元数据，比如类的层级信息，方法数据和方法信息（如字节码，栈和变量大小），运行时常量池，已确定的符号引用和虚方法表。在过去（当自定义类加载器使用不普遍的时候），类几乎是“静态的”并且很少被卸载和回收，因此类也可以被看成“永久的”。另外由于类作为 JVM 实现的一部分，它们不由程序来创建，因为它们也被认为是“非堆”的内存。在 JDK8 之前的 HotSpot虚拟机中，类的这些“永久的”数据存放在一个叫做永久代的区域。永久代一段连续的内存空间，永久代的垃圾回收和老年代的垃圾回收是绑定的，一旦其中一个区域被占满，这两个区都要进行垃圾回收。
> Java8之后，永久代和堆内存已经不连在一起了，元数据被移动到一个在本地内存区域中，该区域称为元空间，J7之前的的hotspot虚拟机中，纳入字符串常量池的字符串被储存在永久代中，因此会导致一系列性能问题和内存溢出问题，而J8中由于改为在本地内存中，所以元空间的内存管理由元空间虚拟机来完成元空间的最大可分配空间就是系统可用内存空间

元空间的内存管理由元空间虚拟机来完成，其采用的形式为组块分配。元空间会被分配给其他类加载器，我们可以这样理解，每个类加载器加载完一个类后，他的命名空间中就多了这个类的信息，对应的元空间虚拟机便会分给该加载器一块区域来保存这个类的元数据，当一个类加载器消亡，他的命名空间不复存在，他对应拥有元空间的组块也全部清除并归还，一旦某个虚拟内存映射区域清空，这部分内存就会返回给操作系统。由于元空间按照组块分配，元空间虚拟机还未支持压缩功能，所以会产生碎片化问题。

接下来通过循环动态生成类，使得新类一直被加载并在元空间中分配区域直到元空间溢出;
```java
import org.springframework.cglib.proxy.Enhancer;
import org.springframework.cglib.proxy.MethodInterceptor;

public class Main {

    public static void main(String[] args) {
        for(;;){
            Enhancer enhancer = new Enhancer( ) ;
            enhancer.setSuperclass (Main.class);
            enhancer.setUseCache(false) ;//是否使用缓存
            enhancer.setCallback((MethodInterceptor) (obj, method, args1, proxy) ->
                    proxy. invokeSuper(obj, args1));

            System.out.println("RUN");
            enhancer.create();
        }

    }

}
```
设置元空间最大内存：`-XX:MaxMetaspaceSize=200m`
![元空间内存溢出.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/元空间内存溢出.png)

可以看到元空间到达200M之后，程序异常退出。

