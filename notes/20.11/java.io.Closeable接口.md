说到java.io.Closeable接口就避不开java.lang.AutoCloseable接口，因为在java版本7.0时引入了java.lang.AutoCloseable接口，同时java.io.Closeable接口便继承自java.lang.AutoCloseable接口了。

### java.io.Closeable

先说一下Closeable接口，这个接口从java 5.0版本开始引入，其中中仅声明了一个方法close，用于关闭一个资源。一直一来我都很困惑，就算不实现这个接口，我给我的类实现一个close方法（或者别的方法）来完成“关闭”的功能不也是一样的么。直到我看到下面的两段代码。



```csharp
//第一段代码
static void copy(String src, String dest)throws IOException {
  InputStream in = null;
  OutputStream out = null; 
  try {
    in = new FileInputStream(src);
    out = new FileOutputStream(dest);
    byte[] buf = new byte[1024];
    int n;
    while ((n = in.read(buf)) >= 0) {
      out.write(buf, 0, n);
    }
  } finally {
    if (in != null) in.close();
    if (out != null) out.close();
  }
}
```

上面这段代码的问题在于，finally语句中的close方法也可能会抛出IOException异常。如果这正好发现在in.close被调用之时，那么这个异常就会阻止out.close被调用，从而使输出流保持在打开状态。所以这个程序使得finally可能被意外结束。解决方式是将每一个close都包装在一个try语句块中。从java 5.0版本开始，可以利用Closeable接口。



```csharp
//第二段代码
// 对第一段代码中的finally语句改造如下
finally {
  closeIgnoringIOException(in);
  closeIgnoringIOException(out);
}
private static void closeIgnoringIOException(Closeable c) {
  if (c != null) {
    try {
      c.close();
    } catch (IOException ex) { }
  }
}
```

基于以上两段代码我知道了java.io.Closeable接口的用处。

### java.lang.AutoCloseable

在java 7.0j时引入了java.lang.AutoCloseable，并且java.io.Closeable接口继承自 java.lang.AutoCloseable。很多资源类都直接或间接的实现了此接口。其实这个接口与try-with-resources语法是密切相关的。

从AutoCloseable的注释可知它的出现是为了更好的管理资源，准确说是资源的释放，当一个资源类实现了该接口close方法，在使用try-with-resources语法创建的资源抛出异常后，JVM会自动调用close 方法进行资源释放，当没有抛出异常正常退出try-block时候也会调用close方法。



```csharp
//第三段代码
static void copy(String src, String dest)throws IOException {
  try (InputStream in=new FileInputStream(src);OutputStream out=new FileOutputStream(dest)){
    byte[] buf = new byte[1024];
    int n;
    while ((n = in.read(buf)) >= 0) {
      out.write(buf, 0, n);
    }
  }catch(Exception e) {
    System.out.println("catch block:"+e.getLocalizedMessage());
  }finally{
    System.out.println("finally block");
  }
}
```

因为InputStream和OutputStream都实现了java.io.Closeable接口（间接实现了java.lang.AutoCloseable接口）所以上面的【第三段代码】与【第二段代码的】一样“安全”。

### try-with-resources

try-with-resources 是在java 7.0 版本时引入的新语法特性。使用它配合java.lang.AutoCloseable接口可以更好的对资源进行释放，减少繁琐的异常处理。

1.  使用try-with-resources结构无论是否抛出异常在try-block执行完毕后都会调用资源的close方法；
2.  使用try-with-resources结构创建多个资源，try-block执行完毕后调用的close方法的顺序与创建资源顺序相反；
3.  使用try-with-resources结构，try-block块抛出异常后先执行所有资源（try的（）中声明的）的close方法然后在执行catch里面的代码然后才是finally；
4.  只用在try的()中声明的资源的close方法才会被调用，并且当对象销毁的时候close不会被再次调用；
5.  使用try-with-resources结构无须显式调用资源释放，编程效率高，代码更简洁。