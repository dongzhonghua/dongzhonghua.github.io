[TOC]

# Spring相关的知识点

## InitializingBean的作用

spring初始化bean有两种方式：
 第一：实现InitializingBean接口，继而实现afterPropertiesSet的方法
 第二：反射原理，配置文件使用init-method标签直接注入bean



InitializingBean接口为bean提供了初始化方法的方式，它只包括afterPropertiesSet方法，凡是继承该接口的类，在初始化bean的时候会执行该方法。

### InitializingBean的原理

这方式在spring中是怎么实现的？
通过查看spring的加载bean的源码类(AbstractAutowireCapableBeanFactory)可看出其中奥妙
AbstractAutowireCapableBeanFactory类中的invokeInitMethods讲解的非常清楚，源码如下：

```java
protected void invokeInitMethods(String beanName, final Object bean, RootBeanDefinition mbd)
            throws Throwable {
//判断该bean是否实现了实现了InitializingBean接口，如果实现了InitializingBean接口，则只掉调用bean的afterPropertiesSet方法
        boolean isInitializingBean = (bean instanceof InitializingBean);
        if (isInitializingBean && (mbd == null || !mbd.isExternallyManagedInitMethod("afterPropertiesSet"))) {
            if (logger.isDebugEnabled()) {
                logger.debug("Invoking afterPropertiesSet() on bean with name '" + beanName + "'");
            }
            
            if (System.getSecurityManager() != null) {
                try {
                    AccessController.doPrivileged(new PrivilegedExceptionAction<Object>() {
                        public Object run() throws Exception {
                            //直接调用afterPropertiesSet
                            ((InitializingBean) bean).afterPropertiesSet();
                            return null;
                        }
                    },getAccessControlContext());
                } catch (PrivilegedActionException pae) {
                    throw pae.getException();
                }
            }                
            else {
                //直接调用afterPropertiesSet
                ((InitializingBean) bean).afterPropertiesSet();
            }
        }
        if (mbd != null) {
            String initMethodName = mbd.getInitMethodName();
            //判断是否指定了init-method方法，如果指定了init-method方法，则再调用制定的init-method
            if (initMethodName != null && !(isInitializingBean && "afterPropertiesSet".equals(initMethodName)) &&
                    !mbd.isExternallyManagedInitMethod(initMethodName)) {
                    //进一步查看该方法的源码，可以发现init-method方法中指定的方法是通过反射实现
                invokeCustomInitMethod(beanName, bean, mbd);
            }
        }
    }
```

总结：
1：spring为bean提供了两种初始化bean的方式，实现InitializingBean接口，实现afterPropertiesSet方法，或者在配置文件中同过init-method指定，两种方式可以同时使用
2：实现InitializingBean接口是直接调用afterPropertiesSet方法，比通过反射调用init-method指定的方法效率相对来说要高点。但是init-method方式消除了对spring的依赖
3：如果调用afterPropertiesSet方法时出错，则不调用init-method指定的方法。

## ApplicationContextAware

某一天我想在一个util里用Spring的一个bean，但是util里面又不能注入bean。那么还有没有别的办法呢，spring这么强大当然有办法。

首先，需要写一个类实现ApplicationContextAware接口：

```java
import org.springframework.beans.BeansException;
import org.springframework.context.ApplicationContext;
import org.springframework.context.ApplicationContextAware;
import org.springframework.stereotype.Component;

@Component
public class SpringJobBeanFactory implements ApplicationContextAware {

    
    private static ApplicationContext applicationContext;
    
    @Override
    public void setApplicationContext(ApplicationContext applicationContext) throws BeansException {
        SpringJobBeanFactory.applicationContext=applicationContext;
        
    }
     public static ApplicationContext getApplicationContext() {
            return applicationContext;
    }
    @SuppressWarnings("unchecked")
    public static <T> T getBean(String name) throws BeansException {
            if (applicationContext == null){
                return null;
            }
            return (T)applicationContext.getBean(name);
      }
}


// 使用：
HelloService helloServiceImpl = SpringJobBeanFactory.getBean("helloServiceImpl");
```

