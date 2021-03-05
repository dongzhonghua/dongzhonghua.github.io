[TOC]

# 类加载机制以及热部署的实现
回顾一下Java类加载相关的知识点，主要是类加载器，加载模型等。并且实现一个小的Java热部署的demo

## 类加载器

###  类加载时机与过程

类从被加载到虚拟机内存中开始，到卸载出内存为止，它的整个生命周期包括：加载（Loading）、验证（Verification）、准备(Preparation)、解析(Resolution)、初始化(Initialization)、使用(Using)和卸载(Unloading)7个阶段。其中准备、验证、解析3个部分统称为连接（Linking）。如图所示

![类加载的过程.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/类加载的过程.png)

加载过程中的一些概念详见：https://juejin.im/post/6844903887866953735

###  类加载器种类

1.  Bootstrap ClassLoader/启动类加载器 
    主要负责jdk_home/lib目录下的核心 api 或 -Xbootclasspath 选项指定的jar包装入工作。
2.  Extension ClassLoader/扩展类加载器 
    主要负责jdk_home/lib/ext目录下的jar包或 -Djava.ext.dirs 指定目录下的jar包装入工作。
3.  Application ClassLoader/应用程序类加载器 
    负责加载用户类路径（classpath）上的指定类库，我们可以直接使用这个类加载器。一般情况，如果我们没有自定义类加载器默认就是用这个加载器。
4.  User Custom ClassLoader/用户自定义类加载器(java.lang.ClassLoader的子类) 
    在程序运行期间, 通过java.lang.ClassLoader的子类动态加载class文件, 体现java动态实时类装入特性。

![java类加载流程.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/java类加载流程.png)

-   一个class文件发送请求加载,会先找到自定义的类加载器,当然这里没画出来
-   APPClassLoader得到加载器请求后,向上委托交给ExtClassLoader,ExtClassLoader同理会交给BoostrapClassLoader,这是向上委托方向
-   最终到达BoostrapClassLoader,会先在缓存中找,没有就尝试在自己能加载的路径去加载,找不到就交给ExtClassLoader,同理一直到用户自定义的ClassLoader,这就是向下查找方向
-   前面说的类的唯一性由类和类加载器共同决定, 这样保证了确保了类的唯一性



### 类加载器特性

1. 每个ClassLoader都维护了一份自己的名称空间， 同一个名称空间里不能出现两个同名的类。
2. 为了实现java安全沙箱模型顶层的类加载器安全机制， java默认采用了 " 双亲委派的加载链 " 结构。

https://mp.weixin.qq.com/s/6nJ-6cDLW6TfysWV5ZB3Iw 一篇讲双亲委派的公众号文章

## 双亲委派模型

> 什么是双亲委派模型？
双亲委派模型工作过程是：如果一个类加载器收到类加载的请求，它首先不会自己去尝试加载这个类，而是把这个请求委派给父类加载器完成。每个类加载器都是如此，只有当父加载器在自己的搜索范围内找不到指定的类时（即ClassNotFoundException），子加载器才会尝试自己去加载。

> 为什么需要双亲委派模型？
假设没有双亲委派模型，试想一个场景：
黑客自定义一个java.lang.String类，该String类具有系统的String类一样的功能，只是在某个函数稍作修改。比如equals函数，这个函数经常使用，如果在这这个函数中，黑客加入一些“病毒代码”。并且通过自定义类加载器加入到JVM中。此时，如果没有双亲委派模型，那么JVM就可能误以为黑客自定义的java.lang.String类是系统的String类，导致“病毒代码”被执行。
而有了双亲委派模型，黑客自定义的java.lang.String类永远都不会被加载进内存。因为首先是最顶端的类加载器加载系统的java.lang.String类，最终自定义的类加载器无法加载java.lang.String类。
或许你会想，我在自定义的类加载器里面强制加载自定义的java.lang.String类，不去通过调用父加载器不就好了吗?确实，这样是可行。但是，在JVM中，判断一个对象是否是某个类型时，如果该对象的实际类型与待比较的类型的类加载器不同，那么会返回false。
举个简单例子：
ClassLoader1、ClassLoader2都加载java.lang.String类，对应Class1、Class2对象。那么Class1对象不属于ClassLoad2对象加载的java.lang.String类型。

> 线程上下文类加载器?

> 如何打破双亲委派模型？
自定义一个classLoader重写loadClass()

## 自定义类加载器

### MyClassLoader
下面我们定义一个ClassLoader，我这里是重写的findClass()方法。使用commons.io.monitor来监听文件夹，如果class文件变动则动态的加载到JVM中。
ClassLoader的相关代码在这篇文章：https://blog.csdn.net/it_zhonghua/article/details/109243855
```java
public class MyClassLoader extends ClassLoader {
    public String rootPath;
    public String[] classPaths;
    public List<String> clazzs;

    public MyClassLoader(String rootPath, String... classPaths) throws Exception {
        this.rootPath = rootPath;
        clazzs = new ArrayList<>();
        this.classPaths = classPaths;
        for (String classPath : classPaths) {
            this.findClass(classPath);
        }
    }

    @Override
    protected Class<?> findClass(String name) throws ClassNotFoundException {
        Class<?> clazz = findLoadedClass(name);
        if (clazz == null) {
            File file = new File(name);
            if (file.isDirectory()) {
                for (File f : Objects.requireNonNull(file.listFiles())) {
                    this.findClass(f.getPath());
                }
            } else {
                try {
                    String fileName = file.getName();
                    String filePath = file.getPath();
                    String endName = fileName.substring(fileName.lastIndexOf(".") + 1);
                    if (endName.equals("class")) {
                        FileInputStream fileInputStream = new FileInputStream(file);
                        byte[] bytes = new byte[(int) file.length()];
                        fileInputStream.read(bytes);
                        String className = filePath.replace(rootPath, "").replaceAll("/", ".");
                        className = className.substring(1, className.lastIndexOf("."));
                        clazzs.add(className);
                        // class文件已经到了虚拟机了
                        return defineClass(className, bytes, 0, bytes.length);
                    }
                } catch (Exception e) {
                    return super.findClass(name);
                }
            }
        }
        return clazz;
    }
}
```
### 测试类
```java
public class Test {
    public Test() {
    }

    public void hello() {
        System.out.println("test 1.0");
        System.out.println("当前使用的类加载器是：" + getClass().getClassLoader());
    }
}
```

### 通过main方法调用

```java
public static void main(String[] args) throws Exception {
    // 模拟一个web项目，一直运行。如果是一个web项目，可以提供一个接口，调用接口就reload。
    while (true) {
        // 同一个classloader只会存在同一个类的一份class，所以如果需要替换之前的class需要new一个classloader。
        String path = MyClassLoader.class.getResource("/").getPath().replaceAll("%20", " ");
        String rootPath = new File(path).getPath();
        MyClassLoader myClassLoader = new MyClassLoader(rootPath, rootPath + "/dsvshx");
        Class<?> aClass = myClassLoader.loadClass("dsvshx.Test");
        Object o = aClass.newInstance();
        aClass.getMethod("hello").invoke(o);
        // 这种方式的话new一个对象的方式还是不能使用热加载的类。如何改变new的对象的classloader？
        new Test().hello();
        Thread.sleep(2000);
    }
    // 全盘委托 该方法所述的类是由哪个类加载器加载的，那么这个方法中new出来的对象也都是由改类加载器加载的。
}
```
下面查看hello()方法打印出来的日志：
```
test 1.0
当前使用的类加载器是：dsvshx.loader.MyClassLoader@60e53b93
test 1.0
当前使用的类加载器是：sun.misc.Launcher$AppClassLoader@18b4aac2
```
现在修改一下1.0变成2.0然后编译一下。

```
test 2.0
当前使用的类加载器是：dsvshx.loader.MyClassLoader@4ccabbaa
test 1.0
当前使用的类加载器是：sun.misc.Launcher$AppClassLoader@18b4aac2
```
下面我们来分析一下。前两行是通过自己的类加载器加载之后反射出来的。后两行new出来的对象还是用应用类加载器。这里就涉及到了jvm类加载的另一个特性：全盘委派。
> “全盘委派”是指当一个ClassLoader装载一个类时，除非显示地使用另一个ClassLoader，则该类所依赖及引用的类也由这个CladdLoader载入。
> 例如，系统类加载器AppClassLoader加载入口类（含有main方法的类）时，会把main方法所依赖的类及引用的类也载入，依此类推。“全盘负责”机制也可称为当前类加载器负责机制。显然，入口类所依赖的类及引用的类的当前类加载器就是入口类的类加载器。

所以第二个new的对象并没有实现热加载。使用的还是之前的class文件。那么怎么打破全盘委派的影响呢。其实可以参考springboot这种框架的启动方式。具体思路就是不使用main方法来启动应用，而是通过自定义的加载器加载入口类，在通过反射的方式来启动应用入口。这样启动入口就是通过自定义加载器加载，过程中用到的类也会通过自定义的加载器来加载。


### 类似springboot启动的方式

```java
public class Application {
    public static String rootPath;

    public static void run(Class<?> clazz) throws Exception {
        String path = clazz.getResource("/").getPath().replaceAll("%20", " ");
        String rootPath = new File(path).getPath();
        Application.rootPath = rootPath;
        FileLisener.startFileMino(rootPath);
        MyClassLoader myClassLoader = new MyClassLoader(rootPath, rootPath + "/dsvshx");
        start0(myClassLoader);
    }

    public void start() {
        System.out.println("启动。。。。。。。。。");
        Test test = new Test();
        test.hello();
        System.out.println(Test.class.getClassLoader());
    }

    public static void start0(MyClassLoader myClassLoader) throws Exception {
        Class<?> aClass = myClassLoader.loadClass("dsvshx.Application");
        Object o = aClass.newInstance();
        aClass.getMethod("start").invoke(o);
    }

    public static void main(String[] args) throws Exception {
        Application.run(MyClassLoader.class);
    }
}
```

```java
public class FileLisener extends FileAlterationListenerAdaptor {

    @Override
    public void onFileChange(File file) {
        if (file.getPath().contains(".class")) {
            try {
                MyClassLoader myClassLoader = new MyClassLoader(Application.rootPath, Application.rootPath + "/dsvshx");
                Application.start0(myClassLoader);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

    public static void startFileMino(String rootPath) throws Exception{
        FileAlterationObserver fileAlterationObserver = new FileAlterationObserver(rootPath);
        fileAlterationObserver.addListener(new FileLisener());
        FileAlterationMonitor fileAlterationMonitor = new FileAlterationMonitor(5000);
        fileAlterationMonitor.addObserver(fileAlterationObserver);
        fileAlterationMonitor.start();
    }
}
```
以上模拟了一个简单的demo，使用filelisener来监听文件夹，如果变动了则使用自定义的加载器来重新加载该class文件。