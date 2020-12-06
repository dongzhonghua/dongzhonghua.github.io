[TOC]

## lambda表达式

Java *Lambda表达式*的一个重要用法是简化某些*匿名内部类*（`Anonymous Classes`）的写法。实际上Lambda表达式并不仅仅是匿名内部类的语法糖，JVM内部是通过*invokedynamic*指令来实现Lambda表达式的。

### Lambda and Anonymous Classes(I)

本节将介绍如何使用Lambda表达式简化匿名内部类的书写，但Lambda表达式并不能取代所有的匿名内部类，只能用来取代**函数接口（Functional Interface）**的简写。



### 自定义函数接口

自定义函数接口很容易，只需要编写一个只有一个抽象方法的接口即可。

```java
// 自定义函数接口
@FunctionalInterface
public interface ConsumerInterface<T>{
	void accept(T t);
}
```

上面代码中的@FunctionalInterface是可选的，但加上该标注编译器会帮你检查接口是否符合函数接口规范。就像加入@Override标注会检查是否重载了函数一样。

有了上述接口定义，就可以写出类似如下的代码：

```java
ConsumerInterface<String> consumer = str -> System.out.println(str);
```

进一步的，还可以这样使用：

```java
class MyStream<T>{
	private List<T> list;
    ...
	public void myForEach(ConsumerInterface<T> consumer){// 1
		for(T t : list){
			consumer.accept(t);
		}
	}
}
MyStream<String> stream = new MyStream<String>();
stream.(str -> System.out.println(str));// 使用自定义函数接口书写Lambda表达式
```

