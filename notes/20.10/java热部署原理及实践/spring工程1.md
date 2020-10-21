[TOC]

### 1. jdbc（Java数据库连接）工程

#### (1)配置pom.xml文件/mysql

```java  
    <dependencies>
        <dependency>
            <groupId>mysql</groupId>
            <artifactId>mysql-connector-java</artifactId>
            <version>8.0.21</version>
        </dependency>
    </dependencies>
```

####  (2)实例

详细解析推荐：[https://blog.csdn.net/qq_22172133/article/details/81266048](https://blog.csdn.net/qq_22172133/article/details/81266048)

```java
package com.day01.jdbc;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
/**
 * 程序的耦合
 * 耦合：程序间的依赖关系
 * 包括：类之间的依赖关系
 * 方法间的依赖关系
 * 解耦：降低程序间的依赖关系
 * 实际开发中应该做到编译起不依赖，运行期才依赖
 */
public class JdbcDemo1 {
    public static void main(String[] args) throws Exception {
        //注册驱动
//        DriverManager.registerDriver(new com.mysql.cj.jdbc.Driver());
        Class.forName("com.mysql.jdbc.Driver");
        //获取连接
        Connection conn = DriverManager.getConnection("jdbc:mysql://localhost:3306/eesy?useUnicode=true&useSSL=false&characterEncoding=utf8&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true","root","ZZDXYX19971125");
        //获取操作数据库的预处理对象
        PreparedStatement pstm = conn.prepareStatement("select * from account");
        //执行SQL语句，得到结果集
        ResultSet rs = pstm.executeQuery();
        //遍历结果集
        while(rs.next()){
            System.out.println(rs.getString("name"));
        }
        //释放资源
        rs.close();
        pstm.close();
        conn.close();
    }
}

```

### 2.spring项目

#### （1）基础知识：

1）项目的三层架构：持久层dao--业务层service（调用持久层）--表现层ui(调用持久层)

2）ioc(inversion of control):把创建对象的权利交给框架，是框架的重要特征，并非面向对象编程的专用术语。它包括依赖注入DI和依赖查找。

3）ioc的作用：削减计算程序的耦合（解除我们代码中的依赖关系）。

#### （2）配置pom.xml文件/spring-context：

```java
<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>

    <groupId>org.example</groupId>
    <artifactId>day01_eesy_04bean</artifactId>
    <version>1.0-SNAPSHOT</version>
    <packaging>jar</packaging>

    <dependencies>
        <dependency>
            <groupId>org.springframework</groupId>
            <artifactId>spring-context</artifactId>
            <version>4.1.6.RELEASE</version>
        </dependency>
    </dependencies>
</project>
```

#### (3)项目实例--此处只有表现层和业务层

业务层：

```java
package com.day02.service.impl;
import com.day02.service.IAccountService;
import java.util.Date;

public class AccountServiceImpl implements IAccountService {
    private String name;
    private Integer age;
    private Date birthday;

    public AccountServiceImpl(String name,Integer age,Date birthday){
        this.name = name;
        this.age = age;
        this.birthday = birthday;
    }
    public void saveAccount(){
        System.out.println("方法执行了哦耶耶" + name + " " + birthday + " " + age);
    }
}
```

业务层接口：

```java
package com.day02.service;
//业务层接口，操作账户
public interface IAccountService {
    //模拟保存账户
    void saveAccount();
}
```

表现层：

```java
package com.day02.ui;
import com.day02.service.IAccountService;
import org.springframework.context.ApplicationContext;
import org.springframework.context.support.ClassPathXmlApplicationContext;
import javax.annotation.Resource;
//模拟一个表现层
public class Client {
    /*
    获取spring容器的ioc核心容器，并根据id获取对象
    classPathXmlAppplicationContext:可以加载类路径中的配置文件，要求配置文件必须在类文件下，不在的话加载不了
    FileSystemXmlApplicationContext：可以加载磁盘下任意路径下的配置文件（由访问权限）
    AnnotationConfigApplicationContext：用于读取注解创建容器的
    核心容器的两个接口：
    ApplicationContext:(单例模式适合）
    后见核心容器时创建对象的策略采用的是立即加载的方式，也就是说一读完配置文件马上就创建配置文件中的对象
    BeanFactory:（多例模式适合）
    策略采用的是延迟加载的方式，什么时候根据id获取对象了，什么时候才是真正的创建对象
     */
    public static void main(String[] args) {
        //1.获取核心容器对象
        ClassPathXmlApplicationContext ac = new              ClassPathXmlApplicationContext("applicationContext.xml");
        //2.根据id获取bean对象
        IAccountService as1 =(IAccountService)ac.getBean("accountService3");
  //      IAccountService as2 =(IAccountService)ac.getBean("accountService");
        as1.saveAccount();
      // System.out.println(as);
       //手动关闭容器
        ac.close();
    }
}
```

#### （4）配置ApplicationContext.xml：

```java
<?xml version="1.0" encoding="UTF-8"?>
<beans xmlns="http://www.springframework.org/schema/beans"
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
       xsi:schemaLocation="
    http://www.springframework.org/schema/beans
    http://www.springframework.org/schema/beans/spring-beans.xsd">
</beans>
```

#### （5）创建ioc核心容器：

##### (1)ApplicationContext的三个常用实现类(适用于单例模式）：

在构建核心容器时，创建对象采用的是立即加载的方式，也就是说，只要一读取完配置文件马上就创建配置文件中配置的对象。

1）ClassPathXmlApplicationContext:可以加载类路径下的配置文件，要求配置文件必须在类路径下，不在的话，加载不了。

```java
ApplicationContext ac = new ClassPathXmlApplicationContext("applicationContext.xml");`
```

2）FileSystemXmlApplicationContext:可以加载磁盘任意路径下的配置文件，必须有访问权限。

```java
ApplicationContext ac = new FileSystemXmlApplicationContext("E:\JAVA_MAVEN\day01_eesy_05DI\src\main\resources\applicationContext.xml");`
```

3）AnnotationConfigApplicationContext:可以读取注解创建容器。

##### (2)BeanFactory(适用于多例模式)

在创建核心容器时，创建对象的策略采用的是延迟加载的方式，也就是说什么时候根据ID获取对象了，什么时候才真正的创建对象。

```java
Resource resource = (Resource) new ClassPathResource("applicationContext.xml");
BeanFactory factory = new XmlBeanFactory((org.springframework.core.io.Resource) resource);
```

#### （6）创建Bean对象：

1）创建bean三种方式

```java
1.使用默认构造函数创建。
      在spring的配置文件中使用bean标签，配以id和class属性之后，且没有其他的属性和标签时，
      采用的就是默认构造函数创建bean对象，此时如果类中如果没有默认构造函数，则对象无法创建.
      <bean id = "accountService" class = "com.day02.service.impl.AccountServiceImpl"></bean>
2.使用普通工厂中的方法创建对象（使用某个类中的方法创建对象，并存入spring容器）--让spring创建对象然后调用工厂对象的方法获取目标对象。
      解释：：现在有一个对象叫做"instanceFactory"，它是一个工厂，里面有方法可以为我们创建一个service。service对象"accountService"怎么来的，是由"instanceFactory"这个id指向的"getAccountService"这个对象。
          
      <bean id = "instanceFactory" class = "com.day02.factory.InstanceFactory"></bean>
      <bean id = "accountService" factory-bean="instanceFactory" factory-method="getAccountService"></bean>
          
public class InstanceFactory {
    public AccountServiceImpl getAccountService(){
        return new AccountServiceImpl();
    }
}

3.使用静态工厂中的静态方法创建对象（使用某个类中的静态方法创建对象，并存入spring容器）
     <bean id = "accountService" class="com.day02.factory.StaticFactory" factory-method="getAccountService"></bean>
   
public class StaticFactory {
    public static AccountServiceImpl getAccountService(){
        return new AccountServiceImpl();
    }
}
```

2）bean的作用范围

```java
1.bean标签的scope属性（默认单例）
    作用：用于指定bean的作用范围
    取值：
    singleton：单例模式
    prototyoe:多例模式
    request:用于web应用的请求范围
    session：用于web应用的会话范围
    global-session：作用于集群环境的会话范围（全局会话范围），当不是集群环境，他等同于上一个。
```

3）bean的生命周期

```java
1.单例对象
         出生：当容器创建时对象出生
         活着：只要容器在
         死亡：容器销毁
         总结：单例对象的生命周期和容器相同
2.多例对象
         出生：当我们使用对象是spring框架为我们创建
         活着：对象只要是使用过程中就一直活着
         死亡：当对象长时间不用，或者没有别的对象引用时，由java的垃圾回收机制回收
         -->
<bean id = "accountService" class = "com.day02.service.impl.AccountServiceImpl" scope="singleton" init-method="init" destroy-method="destorys"></bean>
    
    public AccountServiceImpl(){
        System.out.println("对象创建了");
    }
    public void init(){
        System.out.println("对象初始化了");
    }
    public void destorys(){
        System.out.println("对象销毁了");
    }
```

#### (7)spring的依赖注入

当前类中需要其他类的对象，由spring为我们提供，我们只需要在配置文件中说明。依赖关系的维护：就称为依赖注入。

能注入的数据有三类：基本类型和string；其他bean类型；复杂类型 集合类型。

注入方式有三种：使用构造函数提供；使用set方法提供；使用注解提供。

##### 1）构造函数注入：

```java
使用的标签：constructor-arg
标签出现的位置：bean标签的内部
标签中的属性：
     type:用于指定要注入的数据的数据类型，该数据类型也是构造函数中某个或某些参数的类型
     index:用于指定要注入的数据给构造函数中的指定索引位置的参数赋值，索引的位置是从0开始
     name:用于指定给定构造函数中的指定名称的参数赋值
     =========以上三个用于指定给构造函数中的哪个参数赋值===================================
     value:用于给基本类型/String类型提供数据
     ref:用于给其他的bean数据的类型，spring ioc核心容器中配置过的额bean对象
优势：获取bean对象时，注入数据是必要的操作，否则对象无法创建成功
弊端：改变了bean对象的实例化方式，使我们在创建对象时，即使用不到哦这些数据时，也必须注入
    <bean id = "accountService" class = "com.day02.service.impl.AccountServiceImpl">
        <constructor-arg name="name" value="test"></constructor-arg>
        <constructor-arg name="age" value="18"></constructor-arg>
        <constructor-arg name="birthday" ref="now"></constructor-arg>
    </bean>
    <bean id="now" class="java.util.Date"></bean>
```

2）set方法注入：

```java
使用的标签：property
标签出现的位置：bean标签的内部
标签中的属性：
     type:用于指定要注入的数据的数据类型，该数据类型也是构造函数中某个或某些参数的类型
     index:用于指定要注入的数据给构造函数中的指定索引位置的参数赋值，索引的位置是从0开始
     name:用于注入指定的set方法名称
     =========以上三个用于指定给构造函数中的哪个参数赋值===================================
     value:用于给基本类型/String类型提供数据
     ref:用于给其他的bean数据的类型，spring ioc核心容器中配置过的额bean对象
优势：创建对象时没有明确的限制
弊端：如果由某个成员必须有值，则获取对象是有可能set方法没有执行-->
    <bean id = "accountService2" class = "com.day02.service.impl.AccountServiceImpl2">
        <property name="name" value="test" ></property>
        <property name="age"  value="24"></property>
        <property name="birthday" ref="now"></property>
    </bean>

public class AccountServiceImpl2 implements IAccountService {
    private String name;
    private Integer age;
    private Date birthday;
    public void setName(String name) {
        this.name = name;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public void setBirthday(Date birthday) {
        this.birthday = birthday;
    }


    public void saveAccount(){
        System.out.println("方法执行了哦耶耶" + name + " " + birthday + " " + age);
    }
}

set方法注入:复杂类型注入
用于给list结构注入的：list set
用于给map结构注入的：map,props-->
    <bean id = "accountService3" class = "com.day02.service.impl.AccountServiceImpl3">
        <property name="myStrs">
            <array>
                <value>AAAA</value>
                <value>BBBBB</value>
                <value>CCCCCCCCC</value>
            </array>
        </property>
        <property name="myList">
            <list>
                <value>AAAA</value>
                <value>BBBBB</value>
                <value>CCCCCCCCC</value>
            </list>
        </property>
        <property name="mySet">
            <list>
                <value>AAAA</value>
                <value>BBBBB</value>
                <value>CCCCCCCCC</value>
            </list>
        </property>
        <property name="myMap">
            <map>
                <entry key="1111" value="vvvvvv"></entry>
                <entry key="1111">
                    <value>5555555</value>
                </entry>
            </map>
        </property>
        <property name="myProps">
            <props>
                <prop key="testc">mmmmmm</prop>
            </props>
        </property>
    </bean>
</beans>
        
public class AccountServiceImpl3 implements IAccountService {
   private String[] myStrs;
   private List<String> myList;
   private Set<String> mySet;
   private Map<String,String> myMap;
   private Properties myProps;

    public void setMyStrs(String[] myStrs) {
        this.myStrs = myStrs;
    }

    public void setMyList(List<String> myList) {
        this.myList = myList;
    }

    public void setMySet(Set<String> mySet) {
        this.mySet = mySet;
    }

    public void setMyMap(Map<String, String> myMap) {
        this.myMap = myMap;
    }

    public void setMyProps(Properties myProps) {
        this.myProps = myProps;
    }

    public void saveAccount(){
        System.out.println(Arrays.toString(myStrs));
        System.out.println(myList);
        System.out.println(mySet);
        System.out.println(myMap);
        System.out.println(myProps);
    }
}
```