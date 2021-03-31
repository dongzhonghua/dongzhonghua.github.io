[TOC]

# 问题分析

1.  对于任何系统来说，日志功能是必不可少的。那么作为一个主流的中间件，MyBatis 是要自己实现一套日志功能呢，还是集成第三方的日志框架呢？MyBatis 选择了后者。
2.  第三方的日志框架种类繁多，常用的包括 Slf4j、Logback、Log4j 等等，这些日志框架的接口定义和内部实现都不尽相同。而且，每个使用 MyBatis 的业务系统都可能引入了不同的日志组件，那么 MyBatis 如何进行兼容呢？如果业务方引入了多个日志框架，MyBatis 按照什么优先级进行选择呢？
3.  MyBatis 的核心流程，包括 SQL 生成、SQL 执行、结果集映射等关键步骤，都是需要打印日志的，那在核心流程中显式调用log.info("xxx") 就显得有点 low了，那么如何将日志打印优雅地嵌入到核心流程中呢？

# 适配器模式

**如果你需要接入多个第三方的 SDK 来满足自己的业务需求，但是 SDK 的接口定义与你的业务不兼容，你又不能修改第三方的代码，这个时候你肯定会想到一个设计模式。对，适配器。**

https://static.yximgs.com/udata/pkg/EE-KSTACK/407db99340f8e504dd7ca0e70bf41ab4.png

**适配器模式的作用：将一个接口转换成满足客户端期望的另一个接口，使得接口不兼容的那些类可以一起工作。**
适配器模式中的角色：

1.  Target：目标接口，定义了客户端所需要的接口。
2.  Adaptee：被适配者，它自身有满足客户端需求的功能，但是接口定义与 Target 并不兼容，需要进行适配。
3.  Adapter：适配器，对 Adaptee 进行适配，使其满足 Target 的定义，供客户端使用。



# 日志框架的集成

下面我们一起研究下 MyBatis 日志适配器的玩法。
首先，MyBatis 定义了自己的 Log 接口，并给出了debug、trace、error、warn 四种日志级别。**这其实是所有主流日志框架所支持的级别的交集。**

```java
/**
 * MyBatis日志接口定义
 * 支持debug、trace、error、warn 四种日志级别
 * 这其实是所有主流日志框架所支持的级别的交集
 */
public interface Log {
  // 省略相关代码...

  void error(String s, Throwable e);

  void error(String s);

  void debug(String s);

  void trace(String s);

  void warn(String s);
}
```

然后，MyBatis 为大部分主流的日志框架都实现了 Adapter。以 Log4j 为例：

```java
/**
 * MyBatis为Log4j实现的Adapter
 * Log4jImpl实现了MyBatis自定义的Log接口,内部实现代理给Log4j的实例完成
 */
public class Log4jImpl implements Log {
  private static final String FQCN = Log4jImpl.class.getName();

  //内部维护log4j的Logger实例
  private final Logger log;

  public Log4jImpl(String clazz) {
    log = Logger.getLogger(clazz);
  }

    // 省略相关代码...

  @Override
  public void error(String s, Throwable e) {
    log.log(FQCN, Level.ERROR, s, e);
  }

  @Override
  public void error(String s) {
    log.log(FQCN, Level.ERROR, s, null);
  }

  @Override
  public void debug(String s) {
    log.log(FQCN, Level.DEBUG, s, null);
  }

  @Override
  public void trace(String s) {
    log.log(FQCN, Level.TRACE, s, null);
  }

  @Override
  public void warn(String s) {
    log.log(FQCN, Level.WARN, s, null);
  }
}
```

Log4jImpl 实现了 MyBatis 自定义的 Log 接口，然后内部实现都代理给 Log4j 的实例完成。其他的 Slf4jImpl、JakartaCommonsLoggingImpl 等等实现类也都是同样的逻辑。
这里适配器模式的应用就很明显了：

https://static.yximgs.com/udata/pkg/EE-KSTACK/492b0d791709efa792d290690993ff30.png

Log = Target
Logger(log4j) = Adaptee
Log4jImpl = Adapter

接下来的问题就是，业务方可能会引入多个日志框架，那么 MyBatis 该如何选择呢？有什么优先级策略吗？
MyBatis 也定义了一个 LogFactory 类，跟其他框架一样，日志的实例都是通过 LogFactory 获取的。我们来看下 LogFactory 的实现：

```java
/**
 * 日志工厂,通过getLog()方法获取日志实现类
 */
public final class LogFactory {

  /**
   * Marker to be used by logging implementations that support markers.
   */
  public static final String MARKER = "MYBATIS";

  private static Constructor<? extends Log> logConstructor;

  static {
    //按照顺序,依次尝试加载Log实现类
    //优先级为:slf4j -> commons-logging -> log4j2 -> log4j -> jdk-logging -> no-logging
    tryImplementation(LogFactory::useSlf4jLogging);
    tryImplementation(LogFactory::useCommonsLogging);
    tryImplementation(LogFactory::useLog4J2Logging);
    tryImplementation(LogFactory::useLog4JLogging);
    tryImplementation(LogFactory::useJdkLogging);
    tryImplementation(LogFactory::useNoLogging);
  }

  private LogFactory() {
    // disable construction
  }

  public static Log getLog(Class<?> clazz) {
    return getLog(clazz.getName());
  }

  public static Log getLog(String logger) {
    try {
      return logConstructor.newInstance(logger);
    } catch (Throwable t) {
      throw new LogException("Error creating logger for logger " + logger + ".  Cause: " + t, t);
    }
  }

  public static synchronized void useCustomLogging(Class<? extends Log> clazz) {
    setImplementation(clazz);
  }

  public static synchronized void useSlf4jLogging() {
    setImplementation(org.apache.ibatis.logging.slf4j.Slf4jImpl.class);
  }

  public static synchronized void useCommonsLogging() {
    setImplementation(org.apache.ibatis.logging.commons.JakartaCommonsLoggingImpl.class);
  }

  public static synchronized void useLog4JLogging() {
    setImplementation(org.apache.ibatis.logging.log4j.Log4jImpl.class);
  }

  public static synchronized void useLog4J2Logging() {
    setImplementation(org.apache.ibatis.logging.log4j2.Log4j2Impl.class);
  }

  public static synchronized void useJdkLogging() {
    setImplementation(org.apache.ibatis.logging.jdk14.Jdk14LoggingImpl.class);
  }

  public static synchronized void useStdOutLogging() {
    setImplementation(org.apache.ibatis.logging.stdout.StdOutImpl.class);
  }

  public static synchronized void useNoLogging() {
    setImplementation(org.apache.ibatis.logging.nologging.NoLoggingImpl.class);
  }

  private static void tryImplementation(Runnable runnable) {
    if (logConstructor == null) {
      try {
        runnable.run();
      } catch (Throwable t) {
        // ignore
        // 找不到构造器,异常直接忽略了
      }
    }
  }

  private static void setImplementation(Class<? extends Log> implClass) {
    try {
      //查找指定实现类的构造器
      Constructor<? extends Log> candidate = implClass.getConstructor(String.class);
      Log log = candidate.newInstance(LogFactory.class.getName());
      if (log.isDebugEnabled()) {
        log.debug("Logging initialized using '" + implClass + "' adapter.");
      }
      logConstructor = candidate;
    } catch (Throwable t) {
      throw new LogException("Error setting Log implementation.  Cause: " + t, t);
    }
  }

}
```

这样一来，我们就清楚了，MyBatis 是按照 slf4j -> commons-logging -> log4j2 -> log4j -> jdk-logging -> no-logging 的优先级选择日志组件的。从 MyBatis 的选择中我们也可以看出，Slf4j 应该还是目前使用比较广泛的日志组件。

最后，这里还有一个点，no-logging 是什么鬼？
no-logging 对应的实现类是 NoLoggingImpl，这其实是 **Null Object Pattern 空对象模式**，它也实现了目标接口，内部实现就是 Do Nothing，这样对客户端来说，可以用一致的方式调用不同的实现类，而无需关心不同实现类的差异，更不用去做任何判空处理。我们也经常在一些枚举的定义里使用这种模式。

```java
/**
 * 空Log实现, Null Object Pattern
 */
public class NoLoggingImpl implements Log {

  public NoLoggingImpl(String clazz) {
    // Do Nothing
  }

  // 省略相关代码...

  @Override
  public void error(String s, Throwable e) {
    // Do Nothing
  }

  @Override
  public void error(String s) {
    // Do Nothing
  }

  @Override
  public void debug(String s) {
    // Do Nothing
  }

  @Override
  public void trace(String s) {
    // Do Nothing
  }

  @Override
  public void warn(String s) {
    // Do Nothing
  }
}
```

