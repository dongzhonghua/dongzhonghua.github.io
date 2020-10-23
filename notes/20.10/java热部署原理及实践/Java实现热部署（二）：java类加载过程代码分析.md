从Launcher看起

ExtClassLoader 和 AppClassLoader不是继承关系，而是通过指定 parent 属性来形成的组合模型


```java
public Launcher() {
    Launcher.ExtClassLoader var1;
    try {
        // 获取扩展类加载器，getExtClassLoader()是用了double check的单例模式，和之前背过的东西相遇了。
        var1 = Launcher.ExtClassLoader.getExtClassLoader();
    } catch (IOException var10) {
        throw new InternalError("Could not create extension class loader", var10);
    }

    try {
        // 获取应用类加载器，并且吧拓展类加载器设置成parent
        this.loader = Launcher.AppClassLoader.getAppClassLoader(var1);
    } catch (IOException var9) {
        throw new InternalError("Could not create application class loader", var9);
    }
    // 指定APPClassloader为线程上下文加载器
    Thread.currentThread().setContextClassLoader(this.loader);
    String var2 = System.getProperty("java.security.manager");
    if (var2 != null) {
        SecurityManager var3 = null;
        if (!"".equals(var2) && !"default".equals(var2)) {
            try {
                // 调用loadClass
                var3 = (SecurityManager)this.loader.loadClass(var2).newInstance();
            } catch (IllegalAccessException var5) {
            } catch (InstantiationException var6) {
            } catch (ClassNotFoundException var7) {
            } catch (ClassCastException var8) {
            }
        } else {
            var3 = new SecurityManager();
        }

        if (var3 == null) {
            throw new InternalError("Could not create SecurityManager: " + var2);
        }

        System.setSecurityManager(var3);
    }

}
```

```java
private static volatile Launcher.ExtClassLoader instance;

public static Launcher.ExtClassLoader getExtClassLoader() throws IOException {
    if (instance == null) {
        Class var0 = Launcher.ExtClassLoader.class;
        synchronized(Launcher.ExtClassLoader.class) {
            if (instance == null) {
                instance = createExtClassLoader();
            }
        }
    }

    return instance;
}
```



```java
protected Class<?> loadClass(String name, boolean resolve)
        throws ClassNotFoundException
    {
        // 方法有同步块（synchronized）,多线程情况不会出现重复加载的情况。
        synchronized (getClassLoadingLock(name)) {
            // First, check if the class has already been loaded
            Class<?> c = findLoadedClass(name);
            if (c == null) {
                long t0 = System.nanoTime();
                try {
                    // 如果父类加载器不为空则使用父类加载器来加载。
                    if (parent != null) {
                        c = parent.loadClass(name, false);
                    } else {
                        // parent为空，交给BootstrapClassLoader
                        c = findBootstrapClassOrNull(name);
                    }
                } catch (ClassNotFoundException e) {
                    // ClassNotFoundException thrown if class not found
                    // from the non-null parent class loader
                }

                if (c == null) {
                    // If still not found, then invoke findClass in order
                    // to find the class.
                    long t1 = System.nanoTime();
                    c = findClass(name);

                    // this is the defining class loader; record the stats
                    sun.misc.PerfCounter.getParentDelegationTime().addTime(t1 - t0);
                    sun.misc.PerfCounter.getFindClassTime().addElapsedTimeFrom(t1);
                    sun.misc.PerfCounter.getFindClasses().increment();
                }
            }
            if (resolve) {
                resolveClass(c);
            }
            return c;
        }
    }
```