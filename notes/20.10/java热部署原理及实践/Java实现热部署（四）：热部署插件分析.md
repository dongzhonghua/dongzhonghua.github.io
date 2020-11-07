# 插件介绍

介绍一个插件，插件地址：https://github.com/liuzhengyang/lets-hotfix。这个插件可以实现热部署，插件的原理原理和前几篇文章中说的原理是一样的。这个插件的具体的使用方式在GitHub上面有详细的说明。插件可以在网页端使用也可以安装idea插件进行热部署。

# 代码分析

![letshotfix代码目录.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/letshotfix代码目录.png)

GitHub中的代项目目录大致分成了这几个部分，我们来一个一个分析。整体的结构和实现的功能图如下：

![lets-hotfix结构图.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/lets-hotfix结构图.png)

## agent

这部分原理很好懂，之前我们也讲到过。这里插件实现的主要功能就是通过后端传递过来的文件名找到对应的文件（文件已经被后端下载到指定的文件夹下）。如果是Java文件则编译成class文件在进行下一步操作。接下来需要看该类是不是已经被加载过了，如果被加载过的话则调用`instrumentation.redefineClasses()`，如果该类是个新的类则调用`defineClass(className, bytes, 0, bytes.length);`定义新的类。所以由于这里的限制，该插件可以添加一个新类或者修改方法体但是不能增加方法或者字段。



## boot

该部分的主要作用是在服务器部署服务，并且把agent文件保存到本地。起到初始化项目的作用。

## core

这部分主要是用到的一些工具类，比如编译工具。

## registry

就是一个eureka的注册中心。

## web

web这部分比较重要，大部分的逻辑集中在这个地方。首先有一个前端界面，可以选择上传一个文件，选择相应的进程，这样就可以实现热部署。
![letshotfix前端界面.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/letshotfix前端界面.png)后端收到文件之后，会保存到一个临时文件夹下，之后会通过attach调用agent，把文件路径传给agent，agent收到之后会读取文件并进行热部署的相关工作。

以上就是我对lets hotfix的一些理解，感谢大佬的开源，这个工具也确实能节省很多的时间和人力成本。我也添加了一些测试，以及前几篇文章里的一些测试用例我都上传到了我fork的仓库下了，欢迎大家提出建议：https://github.com/dongzhonghua/lets-hotfix。