[TOC]

# Java SPI机制详解

## 什么是SPI？

SPI 全称为 (Service Provider Interface) ，是JDK内置的一种服务提供发现机制。SPI是一种动态替换发现的机制， 比如有个接口，想运行时动态的给它添加实现，你只需要添加一个实现。我们经常遇到的就是java.sql.Driver接口，其他不同厂商可以针对同一接口做出不同的实现，mysql和postgresql都有不同的实现提供给用户，而Java的SPI机制可以为某个接口寻找服务实现。



## Java SPI 应用实例

当服务的提供者提供了一种接口的实现之后，需要在classpath下的META-INF/services/目录里创建一个以服务接口命名的文件，这个文件里的内容就是这个接口的具体的实现类。当其他的程序需要这个服务的时候，就可以通过查找这个jar包（一般都是以jar包做依赖）的META-INF/services/中的配置文件，配置文件中有接口的具体实现类名，可以根据这个类名进行加载实例化，就可以使用该服务了。JDK中查找服务实现的工具类是：java.util.ServiceLoader。

## SPI的用途

数据库DriverManager、Spring、ConfigurableBeanFactory等都用到了SPI机制，这里以数据库DriverManager为例，看一下其实现的内幕。

DriverManager是jdbc里管理和注册不同数据库driver的工具类。针对一个数据库，可能会存在着不同的数据库驱动实现。我们在使用特定的驱动实现时，不希望修改现有的代码，而希望通过一个简单的配置就可以达到效果。 在使用mysql驱动的时候，会有一个疑问，DriverManager是怎么获得某确定驱动类的？我们在运用Class.forName("com.mysql.jdbc.Driver")加载mysql驱动后，就会执行其中的静态代码把driver注册到DriverManager中，以便后续的使用。

在JDBC4.0之前，连接数据库的时候，通常会用`Class.forName("com.mysql.jdbc.Driver")`这句先加载数据库相关的驱动，然后再进行获取连接等的操作。而JDBC4.0之后不需要`Class.forName`来加载驱动，直接获取连接即可，这里使用了Java的SPI扩展机制来实现。

在java中定义了接口java.sql.Driver，并没有具体的实现，具体的实现都是由不同厂商来提供的。

### mysql

在mysql-connector-java-5.1.45.jar中，META-INF/services目录下会有一个名字为java.sql.Driver的文件：

```
com.mysql.jdbc.Driver
com.mysql.fabric.jdbc.FabricMySQLDriver
```

## SPI例子

首先定义一个接口：

```java
package xyz.dsvshx.spi;

/**
 * @author dongzhonghua
 * Created on 2021-03-05
 */
public interface Log {
    void log(String msg);
}
```

定义两个实现类：

```java
package xyz.dsvshx.spi;

/**
 * @author dongzhonghua
 * Created on 2021-03-05
 */
public class Log4j implements Log {
    @Override
    public void log(String msg) {
        System.out.printf("Log4j: %s%n", msg);
    }
}

package xyz.dsvshx.spi;

/**
 * @author dongzhonghua
 * Created on 2021-03-05
 */
public class LogBack implements Log {
    @Override
    public void log(String msg) {
        System.out.printf("LogBack: %s%n", msg);
    }
}

```

![](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/resource%E6%96%87%E4%BB%B6%E5%A4%B9spi.png)

新建一个文件夹，内容如下：

```
xyz.dsvshx.spi.Log4j
xyz.dsvshx.spi.LogBack
```

测试类：

```java
package xyz.dsvshx.spi;

import java.util.Iterator;
import java.util.ServiceLoader;

/**
 * @author dongzhonghua
 * Created on 2021-03-05
 */

public class LogTest {
    public static void main(String[] args) {
        ServiceLoader<Log> serviceLoader = ServiceLoader.load(Log.class);
        Iterator<Log> iterator = serviceLoader.iterator();
        while (iterator.hasNext()) {
            Log log = iterator.next();
            log.log("JDK SPI");
        }
    }
}
```

输出：

Log4j: JDK SPI
LogBack: JDK SPI

![img](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/spi%E5%8E%9F%E7%90%86%E6%80%BB%E7%BB%93.png)





### Spring中spi思想的应用

Spring中运用到spi思想的地方也有很多，下面随便列举几个

#### scan

我们在spring中可以通过component-scan标签来对指定包路径进行扫描，只要扫到spring制定的@service、@controller等注解，spring自动会把它注入容器。

这就相当于spring制定了注解规范，我们按照这个注解规范开发相应的实现类或controller，spring并不需要感知我们是怎么实现的，他只需要根据注解规范和scan标签注入相应的bean，这正是spi理念的体现。

### Scope

spring中有作用域scope的概念。
除了singleton、prototype、request、session等spring为我们提供的域，我们还可以自定义scope。

像是自定义一个 ThreadScope实现Scope接口
再把它注册到beanFactory中

```text
Scope threadScope = new ThreadScope();
beanFactory.registerScope("thread", threadScope);
```

接着就能在xml中使用了

```text
<bean id=".." class=".." scope="thread"/>
```

spring作为使用方提供了自定义scope的规则，提供方根据规则进行编码和配置，这样在spring中就能运用我们自定义的scope了，并不需要spring感知我们scope里的实现，这也是平台使用方制定规则，提供方负责实现的思想。

### 自定义标签

扩展Spring自定义标签配置大致需要以下几个步骤

1. 创建一个需要扩展的组件，也就是一个bean
2. 定义一个XSD文件描述组件内容，也可以给bean的属性赋值啥的
3. 创建一个文件，实现BeanDefinitionParser接口，用来解析XSD文件中的定义和对组件进行初始化，像是为组件bean赋上xsd里设置的值
4. 创建一个Handler文件，扩展自NamespaceHandlerSupport，目的是将组件注册到Spring容器，重写其中的的init方法

这样我们就边写出了一个自定义的标签，spring只是为我们定义好了创建标签的流程，不用感知我们是如何实现的，我们通过register就把自定义标签加载到了spring中，实现了spi的思想。



### ConfigurableBeanFactory

spring里为我们提供了许多属性编辑器，这时我们如果想把spring配置文件中的字符串转换成相应的对象进行注入，就要自定义属性编辑器，这时我们可以按照spring为我们提供的规则来自定义我们的编辑器

自定义好了属性编辑器后，ConfigurableBeanFactory里面有一个registerCustomEditor方法，此方法的作用就是注册自定义的编辑器，也是spi思想的体现



## JDK SPI 源代码

首先获取类加载器：

```java
public static <S> ServiceLoader<S> load(Class<S> service) {
    ClassLoader cl = Thread.currentThread().getContextClassLoader();
    return ServiceLoader.load(service, cl);
}
```

首先，会检查传入的接口类是否存在。

其次，当前线程的 ClassLoader 不存在时，默认使用 SystemClassLoader。

```java

public static <S> ServiceLoader<S> load(Class<S> service, ClassLoader loader) {
    return new ServiceLoader<>(service, loader);
}

private ServiceLoader(Class<S> svc, ClassLoader cl) {
    service = Objects.requireNonNull(svc, "Service interface cannot be null");
    loader = (cl == null) ? ClassLoader.getSystemClassLoader() : cl;
    acc = (System.getSecurityManager() != null) ? AccessController.getContext() : null;
    reload();
}
```



首先，清理 LinkedHashMap 缓存。

其次，初始化新的 LazyIterator 对象，实现完全延迟的查找。

```java

private LinkedHashMap<String,S> providers = new LinkedHashMap<>();
public void reload() {
    providers.clear();
    lookupIterator = new LazyIterator(service, loader);
}
```



LazyIterator 是私有的内部类，实现完全延迟的提供程序查找。

- hasNextService 会读取固定前缀 PREFIX 服务接口文件数据，并将读到的数据赋值给 pending 对象。
- nextService 会将 hasNextService 方法读取到的信息，转换成实现类 Class，赋值给 providers 对象。

```java
private class LazyIterator implements Iterator<S> {
  Class<S> service;
  ClassLoader loader;
  Enumeration<URL> configs = null;
  Iterator<String> pending = null;
  String nextName = null;

  private LazyIterator(Class<S> service, ClassLoader loader) {
      this.service = service;
      this.loader = loader;
  }

  private boolean hasNextService() {
      if (nextName != null) {
          return true;
      }
      if (configs == null) {
          try {
              String fullName = PREFIX + service.getName();
              if (loader == null)
                  configs = ClassLoader.getSystemResources(fullName);
              else
                  configs = loader.getResources(fullName);
          } catch (IOException x) {
              fail(service, "Error locating configuration files", x);
          }
      }
      while ((pending == null) || !pending.hasNext()) {
          if (!configs.hasMoreElements()) {
              return false;
          }
          pending = parse(service, configs.nextElement());
      }
      nextName = pending.next();
      return true;
  }

  private S nextService() {
      if (!hasNextService())
          throw new NoSuchElementException();
      String cn = nextName;
      nextName = null;
      Class<?> c = null;
      try {
          c = Class.forName(cn, false, loader);
      } catch (ClassNotFoundException x) {
          fail(service,
               "Provider " + cn + " not found");
      }
      if (!service.isAssignableFrom(c)) {
          fail(service,
               "Provider " + cn  + " not a subtype");
      }
      try {
          S p = service.cast(c.newInstance());
          providers.put(cn, p);
          return p;
      } catch (Throwable x) {
          fail(service,
               "Provider " + cn + " could not be instantiated",
               x);
      }
      throw new Error();          // This cannot happen
  }

  public boolean hasNext() {
      if (acc == null) {
          return hasNextService();
      } else {
          PrivilegedAction<Boolean> action = new PrivilegedAction<Boolean>() {
              public Boolean run() { return hasNextService(); }
          };
          return AccessController.doPrivileged(action, acc);
      }
  }

  public S next() {
      if (acc == null) {
          return nextService();
      } else {
          PrivilegedAction<S> action = new PrivilegedAction<S>() {
              public S run() { return nextService(); }
          };
          return AccessController.doPrivileged(action, acc);
      }
  }

  public void remove() {
      throw new UnsupportedOperationException();
  }

}
```



## Dubbo实现spi

https://cloud.tencent.com/developer/article/1727394



## 参考：

https://zhuanlan.zhihu.com/p/28909673

https://juejin.cn/post/6844903605695152142
