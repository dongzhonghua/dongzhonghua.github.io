## 加命令

https://ningyu1.github.io/site/post/93-maven-depenpency-analyze/



```
mvn -DincludeScope=runtime \
    clean package dependency:copy-dependencies \
    -Dcheckstyle.skip=true -U -Dmaven.compile.fork=true -Dmaven.test.skip=true \
    -Denforcer.skip=true || exit 1
```

## 减依赖

分析没有用到的依赖

```
mvn dependency:analyze -DignoreNonCompile
```





