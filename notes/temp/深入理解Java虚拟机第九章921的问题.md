问题： 
> 如果有10个WEB应用程序都是用Spring来进行组织和管理的话，可以把Spring放到Common或Shared目录下（Tomcat5.0）让这些程序共享。Spring要对用户程序的类进行管理，自然要能访问到用户程序的类，而用户的程序显然是放在/WebApp/WEB-INF目录下的，那么被CommonClassLoader或SharedClassLoader加载的Spring如何访问并不在其加载范围内的用户程序呢？如果读过本书第7章的相关内容，相信读者可以很同意的回答这个问题。

回答：

书中第7章7.4.3说的，破坏双亲委派模型中的线程上下文类加载器就是答案。

spring加载类所用的classloader都是通过Thread.currentThread().getContextClassLoader()来获取的，而当线程创建时会默认 setContextClassLoader(AppClassLoader)，即spring中始终可以获取到这个AppClassLoader(在tomcat里就是WebAppClassLoader)子类加载器来加载bean，以后任何一个线程都可以通过getContextClassLoader()获取到WebAppClassLoader来getbean


