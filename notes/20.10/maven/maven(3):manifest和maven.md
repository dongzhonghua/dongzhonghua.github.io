[TOC]

# jar文件

提到 JAR，最先可能想到的就是依赖，比如 fastjson.jar ，它可以作为依赖在项目中来引用，但是不能通过 java -jar 来执行，这种就是非可执行的 JAR。另外一种，比如我们项目打包之后生成的 JAR （当然也可能是 war），我们可以通过 java -jar 来运行程序，我们把它称之为可执行的 JAR。

JAR 作用大体可以分为以下几种：

-   用于发布和使用类库
-   作为应用程序和扩展的构建单元
-   作为组件、applet 或者插件程序的部署单位
-   用于打包与组件相关联的辅助资源

JAR 文件格式提供了许多优势和功能，其中很多是传统的压缩格式如 ZIP 或者 TAR 所没有提供的。它们包括：

-   安全性：可以对 JAR 文件内容加上数字化签名。这样，能够识别签名的工具就可以有选择地为您授予软件安全特权，这是其他文件做不到的，它还可以检测代码是否被篡改过。
-   减少下载时间：如果一个 applet 捆绑到一个 JAR 文件中，那么浏览器就可以在一个 HTTP 事务中下载这个 applet 的类文件和相关的资源，而不是对每一个文件打开一个新连接。
-   压缩：JAR 格式允许您压缩文件以提高存储效率。
-   传输平台扩展。Java 扩展框架 (Java Extensions Framework) 提供了向 Java 核心平台添加功能的方法，这些扩展是用 JAR 文件打包的 (Java 3D 和 JavaMail 就是由 Sun 开发的扩展例子 )。
-   包密封：存储在 JAR 文件中的包可以选择进行 密封，以增强版本一致性和安全性。密封一个包意味着包中的所有类都必须在同一 JAR 文件中找到。
-   包版本控制：一个 JAR 文件可以包含有关它所包含的文件的数据，如厂商和版本信息。
-   可移植性：处理 JAR 文件的机制是 Java 平台核心 API 的标准部分。

## 常见的 jar工具用法

| 功能                                    | 命令                             |
| :-------------------------------------- | :------------------------------- |
| 用一个单独的文件创建一个 JAR 文件       | jar cf jar-file input-file...    |
| 用一个目录创建一个 JAR 文件             | jar cf jar-file dir-name         |
| 创建一个未压缩的 JAR 文件               | jar cf0 jar-file dir-name        |
| 更新一个 JAR 文件                       | jar uf jar-file input-file...    |
| 查看一个 JAR 文件的内容                 | jar tf jar-file                  |
| 提取一个 JAR 文件的内容                 | jar xf jar-file                  |
| 从一个 JAR 文件中提取特定的文件         | jar xf jar-file archived-file... |
| 运行一个打包为可执行 JAR 文件的应用程序 | java -jar app.jar                |




# META-INF

大多数 JAR 文件包含一个 META-INF 目录，它用于存储包和扩展的配置数据，如安全性和版本信息。Java 2 平台（标准版【J2SE】）识别并解释 META-INF 目录中的下述文件和目录，以便配置应用程序、扩展和类装载器：

-   MANIFEST.MF：这个 manifest 文件定义了与扩展和包相关的数据。
-   通过 MAVEN 插件打包进来的文件比如：
    -   maven
    -   services ： 存储所有服务提供程序配置文件
-   其他的还有一些不常看到的：
    -   INDEX.LIST ：这个文件由 jar工具的新选项 -i生成，它包含在应用程序或者扩展中定义的包的位置信息。它是 JarIndex 实现的一部分，并由类装载器用于加速类装载过程。
    -   .SF：这是 JAR 文件的签名文件
    -   .DSA：与签名文件相关联的签名程序块文件，它存储了用于签名 JAR 文件的公共签名。
    -   LICENSE.txt ：证书信息
    -   NOTICE.txt ： 公告信息



# maven和MANIFEST.MF

可以通过在pom文件里增加配置来自动生成MANIFEST.MF

```xml
<archive>
    <manifestEntries>
        <Specification-Title>${project.name}</Specification-Title>
        <Specification-Version>${project.version}</Specification-Version>
        <Implementation-Title>${project.name}</Implementation-Title>
        <Implementation-Version>${project.version}</Implementation-Version>
        <Main-Class>dsvshx.agent.AgentTest</Main-Class>
    </manifestEntries>
</archive>
```

这样生成的内容如下：

![manifest.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/manifest.png)