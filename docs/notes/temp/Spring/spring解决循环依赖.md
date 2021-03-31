[TOC]

# 循环依赖

## 简单的解决循环依赖的方法

用两个map来解决

## spring为什么要用三个缓存来解决循环依赖

众所周知，spring是用了三个map来解决了循环依赖问题如下所示：

```java
//DefaultSingletonBeanRegistry类的三个成员变量命名如下：

/** 一级缓存 单例缓存池 缓存的是一个完整可用的bean实例*/
private final Map<String, Object> singletonObjects = new ConcurrentHashMap<>(256);

/** 三级缓存 该map用户缓存 key为 beanName  value 为ObjectFactory 可以通过ObjectFactory中的getObject()
	 方法来生成bean并包装bean，这级缓存用来处理生成需要被包装代理的类，如AOP的功能实现，个人自定义的一些
	 bean包装生成策略。
*/
private final Map<String, ObjectFactory<?>> singletonFactories = new HashMap<>(16);

/** 二级缓存 ，用来缓存未创建完全的bean，即此时的bean还不可用，属性还没入完成全部注入*/
private final Map<String, Object> earlySingletonObjects = new HashMap<>(16);    

@FunctionalInterface
public interface ObjectFactory<T> {

	/**
	 * Return an instance (possibly shared or independent)
	 * of the object managed by this factory.
	 * @return the resulting instance
	 * @throws BeansException in case of creation errors
	 */
	T getObject() throws BeansException;
}
```

那么为什么要用三级呢？刚才我们用的两级不是也解决了吗？

那么更进一步，为什么要用两级，一级行不行呢？我们一步步分析：

### 只使用一级缓存

只用一级缓存有两种情况：

**缓存类型为Map<String, Object>**
		那么所有的bean都会被缓存在这个map中，有创建完成可使用的，也有未创建完整属性注入未完成的，如果这个时候程序中有获取bean的需求，拿到没有创建好完整的bean，那么在使用的过程中，就会出现问题了，如果要用某个属性，但是还未注入，就会报空指针NullPointException异常了，所以这种缓存方式肯定是不行的。

**缓存类型为Map<String, ObjectFactory<?>>**

这种情况下并不能保证bean的单例，也不能很好的解决代理的问题



### 使用两级缓存

**singletonObjects 和 earlySingletonObjects 组合**

​		现在有A的field或者setter依赖B的实例对象，同时B的field或者setter依赖了A的实例，A首先开始创建，并将自己暴露到 earlySingletonObjects 中，开始填充属性，此时发现自己依赖B的属性，尝试去get(B)，发现B还没有被创建，所以开始创建B，在进行属性填充时初始化A，就从earlySingletonObjects 中获取到了实例化但没有任何属性的A，B拿到A后完成了初始化阶段，将自己放到singletonObjects中,此时返回A，A拿到B的对象继续完成初始化，完成后将自己放到singletonObjects中，由A与B中所表示的A的属性地址是一样的，所以A的属性填充完后，B也获取了A的属性，这样就解决了循环的问题。

  似乎完美解决，如果就这么使用的话也没什么问题，但是再加上AOP情况就不同了，被AOP增强的Bean会在初始化后代理成为一个新的对象，也就是说：
  如果有AOP，A依赖于B，B依赖于A，A实例化完成暴露出去，开始注入属性，发现引用B，B开始实例化，使用A暴露的对象，初始化完成后封装成代理对象，A再将代理后的B注入，再做代理，那么代理A中的B就是代理后的B，但是代理后的B中的A是没用代理的A。

​		而且spring加载流程是：实例化，设置属性，初始化（即执行initializeBean方法），增强。在有循环引用的时候，之前的bean并不会增强后放入到二级缓存。

**singletonObjects 和 singletonFactories 组合**

A实例化，放入singletonFactories 缓存，设置B，B实例化，设置属性，拿到A,此时从singletonFactories 缓存中拿到代理后的A。由于A没加载完毕，不会放入singletonObjects 缓存。这个时候B开始设置C,C实例化，设置属性A,又去singletonFactories 缓存中拿对象A,。这个时候通过ObjectFactory的getObject()方法生成的A和B中生成的A就不是同一个对象了，出现问题。但是我想到一点就是这里能用单例模式吗？



### 使用三级缓存

A实例化，放入三级singletonFactories缓存，设置属性B，B实例化放入三级singletonFactories缓存。B设置属性A，从三级singletonFactories 缓存中获取代理后的对象A，同时，代理后的A放入二级earlySingletonObjects 缓存，然后设置属性C，C实例化放入三级singletonFactories 缓存，设置属性A，此时从二级earlySingletonObjects 缓存中获取到的代理后的A跟B中的A是一个对象，属性A设置成功。然后执行后置处理器，进行aop的增强。增强后将代理的C放入到一级singletonObjects 缓存，同时删除三级singletonFactories缓存中的C。C加载完成，B得到C，B设置C成功，然后执行后置处理器，进行aop增强，将增强后的代理对象B放入到一级singletonObjects 缓存。删除三级singletonFactories缓存中的B。此时A拿到B，设置属性B成功，初始化后执行后置处理器，进行aop的增强生成最终代理，完成整个bean的创建。


一级缓存`singletonObjects`是完整的bean，它可以被外界任意使用，并且不会有歧义。

二级缓存`earlySingletonObjects`是不完整的bean，没有完成初始化，它与`singletonObjects`的分离主要是职责的分离以及边界划分，可以试想一个Map缓存里既有完整可使用的bean，也有不完整的，只能持有引用的bean，在复杂度很高的架构中，很容易出现歧义，并带来一些不可预知的错误。

三级缓存`singletonFactories`，其职责就是包装一个bean，有回调逻辑，所以它的作用非常清晰，并且只能处于第三层。

在实际使用中，要获取一个bean，先从一级缓存一直查找到三级缓存，缓存bean的时候是从三级到一级的顺序保存，并且缓存bean的过程中，三个缓存都是互斥的，只会保持bean在一个缓存中，而且，最终都会在一级缓存中。

## 参考

> https://www.cnblogs.com/semi-sub/p/13548479.html
>
> https://blog.csdn.net/qq_35457078/article/details/112409302
>
> https://www.cnblogs.com/asker009/p/14376955.html
>
> https://segmentfault.com/a/1190000023647227



















