[TOC]

# java代理



## JDK动态代理



## CGLib





## 区别

CGLib创建代理的速度比较慢，但是创建代理后运行的速度却非常快，而JDK动态代理正好相反。如果在运行的时候不断地用CGLib去创建代理，系统的性能会大打折扣，所以建议一般在系统的初始化的时候用CGLib创建代理，并放入spring的ApplicationContext中以备后用。