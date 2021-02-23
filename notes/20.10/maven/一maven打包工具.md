[TOC]

# mvn系列文章

有很多习以为常的东西本来觉得自己会了，但是其实很多细节上的东西都没理解好。写mvn是因为我对于maven的插件有不知道的地方，结果在查这个的时候又发现了其他很多自己不太理解的东西，也结合之前搜过的不会的东西，整理一个集合。后续其他学过的东西还是得整理一下，不然时间长了没有积累的东西很快就会忘了。

## maven打包插件

##  maven-assembly-plugin，maven-shade-plugin与maven-assembly-plugin

### 一、介绍

maven提供的打包插件有如下三种：

| plugin                | function                                       |
| --------------------- | ---------------------------------------------- |
| maven-jar-plugin      | maven 默认打包插件，用来创建 project jar       |
| maven-shade-plugin    | 用来打可执行包，executable(fat) jar            |
| maven-assembly-plugin | 支持定制化打包方式，例如 apache 项目的打包方式 |

### 二、 打包准备

1.  需要设定文件的编码格式（如果不设定，将会以系统的默认编码进行处理）与JDK版本版本变量，代码如下：

```xml
<properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
    <java.version>1.8</java.version>
</properties>
```

2.  需要确定依赖的scope：默认的scope包括如下

    

    | scope    | 说明                                                         |
    | ------------- | ------------------------------------------------------------ |
    | compile  | 默认的范围；如果没有提供一个范围，那该依赖的范围就是编译范围。编译范围依赖在所有的classpath 中可用，同时它们也会被打包 |
    | provided | 依赖只有在当JDK 或者一个容器已提供该依赖之后才使用。例如， 如果你开发了一个web 应用，你可能在编译 classpath 中需要可用的Servlet API 来编译一个servlet，但是你不会想要在打包好的WAR 中包含这个Servlet API；这个Servlet API JAR 由你的应用服务器或者servlet 容器提供。已提供范围的依赖在编译classpath （不是运行时）可用。它们不是传递性的，也不会被打包。 |
    | runtime  | 依赖在运行和测试系统的时候需要，但在编译的时候不需要。比如，你可能在编译的时候只需要JDBC API JAR，而只有在运行的时候才需要JDBC驱动实现。 |
    | test     | test范围依赖 在一般的编译和运行时都不需要，它们只有在测试编译和测试运行阶段可用 |
    | system   | system范围依赖与provided 类似，但是你必须显式的提供一个对于本地系统中JAR 文件的路径。这么做是为了允许基于本地对象编译，而这些对象是系统类库的一部分。这样的构件应该是一直可用的，Maven 也不会在仓库中去寻找它。如果你将一个依赖范围设置成系统范围，你必须同时提供一个 systemPath 元素。注意该范围是不推荐使用的（你应该一直尽量去从公共或定制的 Maven 仓库中引用依赖） |

3.  maven的build:

  build分为两种：

  a. base build（既为project的子元素）

```xml
<build>  
    <defaultGoal>install</defaultGoal>  
    <directory>${basedir}/target</directory>  
    <finalName>${artifactId}-${version}</finalName>  
    <filters>  
        <filter>filters/filter1.properties</filter>  
    </filters>  
    ...  
</build> 
```

上述例子中：

defaultGoal:执行build任务时，如果没有指定目标，将使用的默认值,上述例子犹如 mvn install.

directory：build目标文件的存放目录，默认在${basedir}/target目录；

finalName：build目标文件的文件名，默认情况下为${artifactId}-${version}；

  b. 指定一个特定的resource位置。例如

```xml
<build>  
    ...  
    <resources>  
         <resource>  
            <targetPath>META-INF/plexus</targetPath>  
            <filtering>false</filtering>  
            <directory>${basedir}/src/main/plexus</directory>  
            <includes>  
                <include>configuration.xml</include>  
            </includes>  
            <excludes>  
                <exclude>**/*.properties</exclude>  
            </excludes>  
         </resource>  
    </resources>  
    <testResources>  
        ...  
    </testResources>  
    ...  
</build>  
```

1、resources：一个resource元素的列表，每一个都描述与项目关联的文件是什么和在哪里；
2、targetPath：指定build后的resource存放的文件夹。该路径默认是basedir。通常被打包在JAR中的resources的目标路径为META-INF；
3、filtering：true/false，表示为这个resource，filter是否激活。
4、directory：定义resource所在的文件夹，默认为${basedir}/src/main/resources；
5、includes：指定作为resource的文件的匹配模式，用*作为通配符；
6、excludes：指定哪些文件被忽略，如果一个文件同时符合includes和excludes，则excludes生效；
7、testResources：定义和resource类似，但只在test时使用，默认的test resource文件夹路径是${basedir}/src/test/resources，test resource不被部署。

c. plugins,如下代码所示：

```xml
<build>  
    ...  
    <plugins>  
        <plugin>  
            <groupId>org.apache.maven.plugins</groupId>  
            <artifactId>maven-jar-plugin</artifactId>  
            <version>2.0</version>  
            <extensions>false</extensions>  
            <inherited>true</inherited>  
            <configuration>  
                <classifier>test</classifier>  
            </configuration>  
            <dependencies>...</dependencies>  
            <executions>...</executions>  
        </plugin>  
    </plugins>  
</build>  
```

除了groupId:artifactId:version标准坐标，plugin还需要如下属性：
1、extensions：true/false，是否加载plugin的extensions，默认为false；
2、inherited：true/false，这个plugin是否应用到该POM的孩子POM，默认true；
3、configuration：配置该plugin期望得到的properies，如上面的例子，我们为maven-jar-plugin的Mojo设置了classifier属性；如果你的POM有一个parent，它可以从parent的build/plugins或者pluginManagement集成plugin配置。

### 三、 maven-jar-plugin插件（maven默认打包插件）

使用 Maven 构建一个 JAR 文件比较容易：只要定义项目包装为 “jar”，然后执行包装生命周期阶段即可。但是定义一个可执行 JAR 文件却比较麻烦。

可行的方案是创建一个MANIFEST.MF 文件中定义一个 `main` 类。或者可以使用两个 Maven 插件帮助您完成：`maven-jar-plugin` 和 `maven-dependency-plugin`。

1.指定manfestFile位置：具体配置如下：

```xml
<project>
  ...
  <build>
    <plugins>
      <plugin>
        <groupId>org.apache.maven.plugins</groupId>
        <artifactId>maven-jar-plugin</artifactId>
        <version>3.0.2</version>
        <configuration>
          <archive>
            <manifestFile>${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
          </archive>
        </configuration>
        ...
      </plugin>
    </plugins>
  </build>
  ...
</project>
```

2.  使用maven-jar-plugin 修改 MANIFEST.MF文件，具体代码如下：

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-jar-plugin</artifactId>
    <configuration>
        <archive>
            <manifest>
                <addClasspath>true</addClasspath>
                <classpathPrefix>lib/</classpathPrefix>
                <mainClass>com.mypackage.MyClass</mainClass>
            </manifest>
        </archive>
    </configuration>
</plugin>
```

所有 Maven 插件通过一个 `<configuration>` 元素公布了其配置，在本例中，`maven-jar-plugin` 修改它的 `archive` 属性，特别是存档文件的 `manifest` 属性，它控制 MANIFEST.MF 文件的内容。包括 3 个元素：

-   `addClassPath`：将该元素设置为 *true* 告知 `maven-jar-plugin` 添加一个 `Class-Path` 元素到 MANIFEST.MF 文件，以及在 `Class-Path` 元素中包括所有依赖项。
-   `classpathPrefix`：如果您计划在同一目录下包含有您的所有依赖项，作为您将构建的 JAR，那么您可以忽略它；否则使用 `classpathPrefix` 来指定所有依赖 JAR 文件的前缀。在清单 1 中，`classpathPrefix` 指出，相对存档文件，所有的依赖项应该位于 “`lib`” 文件夹。
-   `mainClass`：当用户使用 `lib` 命令执行 JAR 文件时，使用该元素定义将要执行的类名。上述可以通过是用maven-dependency-plugin将依赖包添加进去

### 四、 maven-shade-plugin

### 五、 maven-assembly-plugin

日常使用的以maven-assembly-plugin为最多，因为大数据项目中往往有很多shell脚本、SQL脚本、.properties及.xml配置项等，采用assembly插件可以让输出的结构清晰而标准化。

要使用该插件，就在项目pom文件中加入以下内容。

```xml
    <build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-assembly-plugin</artifactId>
                <version>${maven-assembly-plugin.version}<version>
                <executions>
                    <execution>
                        <id>make-assembly</id>
                        <!-- 绑定到package生命周期 -->
                        <phase>package</phase>
                        <goals>
                            <!-- 只运行一次 -->
                            <goal>single</goal>
                        </goals>
                    </execution>
                </executions>
                <configuration>
                    <!-- 配置描述符文件 -->
                    <descriptor>src/main/assembly/assembly.xml</descriptor>
                    <!-- 也可以使用Maven预配置的描述符
                    <descriptorRefs>
                        <descriptorRef>jar-with-dependencies</descriptorRef>
                    </descriptorRefs> -->
                </configuration>
            </plugin>
        </plugins>
    </build>
```

assembly插件的打包方式是通过descriptor（描述符）来定义的。
 Maven预先定义好的描述符有bin，src，project，jar-with-dependencies等。比较常用的是jar-with-dependencies，它是将所有外部依赖JAR都加入生成的JAR包中，比较傻瓜化。
 但要真正达到自定义打包的效果，就需要自己写描述符文件，格式为XML。下面是我们的项目中常用的一种配置。

```xml
<assembly>
    <id>assembly</id>

    <formats>
        <format>tar.gz</format>
    </formats>

    <includeBaseDirectory>true</includeBaseDirectory>

    <fileSets>
        <fileSet>
            <directory>src/main/bin</directory>
            <includes>
                <include>*.sh</include>
            </includes>
            <outputDirectory>bin</outputDirectory>
            <fileMode>0755</fileMode>
        </fileSet>
        <fileSet>
            <directory>src/main/conf</directory>
            <outputDirectory>conf</outputDirectory>
        </fileSet>
        <fileSet>
            <directory>src/main/sql</directory>
            <includes>
                <include>*.sql</include>
            </includes>
            <outputDirectory>sql</outputDirectory>
        </fileSet>
        <fileSet>
            <directory>target/classes/</directory>
            <includes>
                <include>*.properties</include>
                <include>*.xml</include>
                <include>*.txt</include>
            </includes>
            <outputDirectory>conf</outputDirectory>
        </fileSet>
    </fileSets>

    <files>
        <file>
            <source>target/${project.artifactId}-${project.version}.jar</source>
            <outputDirectory>.</outputDirectory>
        </file>
    </files>

    <dependencySets>
        <dependencySet>
            <unpack>false</unpack>
            <scope>runtime</scope>
            <outputDirectory>lib</outputDirectory>
        </dependencySet>
    </dependencySets>
</assembly>
```

##### id与formats

-   formats是assembly插件支持的打包文件格式，有zip、tar、tar.gz、tar.bz2、jar、war。可以同时定义多个format。
-   id则是添加到打包文件名的标识符，用来做后缀。
-   也就是说，如果按上面的配置，生成的文件就是${artifactId}-${version}-assembly.tar.gz。

##### fileSets/fileSet

用来设置一组文件在打包时的属性。

-   directory：源目录的路径。
-   includes/excludes：设定包含或排除哪些文件，支持通配符。
-   fileMode：指定该目录下的文件属性，采用Unix八进制描述法，默认值是0644。
-   outputDirectory：生成目录的路径。

##### files/file

与fileSets大致相同，不过是指定单个文件，并且还可以通过destName属性来设置与源文件不同的名称。

##### dependencySets/dependencySet

用来设置工程依赖文件在打包时的属性。也与fileSets大致相同，不过还有两个特殊的配置：

-   unpack：布尔值，false表示将依赖以原来的JAR形式打包，true则表示将依赖解成*.class文件的目录结构打包。
-   scope：表示符合哪个作用范围的依赖会被打包进去。compile与provided都不用管，一般是写runtime。

按照以上配置打包好后，将.tar.gz文件上传到服务器，解压之后就会得到bin、conf、lib等规范化的目录结构，十分方便。




参考：https://www.jianshu.com/p/e581fff1cf87
