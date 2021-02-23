[TOC]

# 通过maven命令来运行Java程序main方法

## 一、从命令行运行

1.  运行前先编译代码，exec：java不会自动编译代码，你需要手动执行mvn compile来完成编译。

```properties
mvn compile
```

2.  编译完成后，执行exec运行main方法。

不需要传递参数：

```bash
mvn exec:java -Dexec.mainClass="com.vineetmanohar.module.Main"
```

需要传递参数：

```bash
mvn exec:java -Dexec.mainClass="com.vineetmanohar.module.Main" -Dexec.args="arg0 arg1 arg2"
```

指定对classpath的运行时依赖：

```bash
mvn exec:java -Dexec.mainClass="com.vineetmanohar.module.Main" -Dexec.classpathScope=runtime
```

## 二、 在pom.xml中指定某个阶段执行

```html
<build>
    <plugins>
        <plugin>
            <groupId>org.codehaus.mojo</groupId>
            <artifactId>exec-maven-plugin</artifactId>
            <version>1.1.1</version>
            <executions>
                <execution>
                    <phase>test</phase>
                    <goals>
                        <goal>java</goal>
                    </goals>
                    <configuration>
                        <mainClass>com.vineetmanohar.module.CodeGenerator</mainClass>
                        <arguments>
                            <argument>arg0</argument>
                            <argument>arg1</argument>
                        </arguments>
                    </configuration>
                </execution>
            </executions>
        </plugin>
    </plugins>
</build>
```

将CodeGenerator.main()方法的执行绑定到maven的 test 阶段，通过下面的命令可以执行main方法：

```bash
mvn test
```

## 三、 在pom.xml中指定某个配置来执行

```html
<profiles>
    <profile>
        <id>code-generator</id>
        <build>
            <plugins>
                <plugin>
                    <groupId>org.codehaus.mojo</groupId>
                    <artifactId>exec-maven-plugin</artifactId>
                    <version>1.1.1</version>
                    <executions>
                        <execution>
                            <phase>test</phase>
                            <goals>
                                <goal>java</goal>
                            </goals>
                            <configuration>
                                <mainClass>com.vineetmanohar.module.CodeGenerator</mainClass>
                                <arguments>
                                    <argument>arg0</argument>
                                    <argument>arg1</argument>
                                </arguments>
                            </configuration>
                        </execution>
                    </executions>
                </plugin>
            </plugins>
        </build>
    </profile>
</profiles>
```

将2中的配置用<profile>标签包裹后就能通过指定该配置文件来执行main方法，如下：

```bash
mvn test -Pcode-generator
```


注：通过以下命令可以获取mvn exec的其他配置参数说明。

```sql
mvn exec:help -Ddetail=true -Dgoal=java
```



参考：https://blog.csdn.net/qbg19881206/article/details/19850857

