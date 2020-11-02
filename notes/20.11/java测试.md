[TOC]

测试其实是衡量一个程序员编程素养的一个比较重要的维度。做测试其实是对自己写过代码的一个再思考的过程，而不仅仅是发现程序中的bug。之前工作中很少写测试，虽然短期看代码产出量变多了但是长久来看的话其实是一个非常不好的习惯，中间还是吃过几次亏的。



## Junit

Junit是idea自带的测试框架，可以用快捷键`shift+command+T`快速的创建测试类。需要添加一下pom依赖：

```xml
  <groupId>org.junit.jupiter</groupId>
  <artifactId>junit-jupiter</artifactId>
  <version>${latest-version}</version>
  <scope>test</scope>
</dependency>
```

在方法中加入@Test方注解可以开始测试。



JUnit5 提供了4个生命周期注解 @BeforeAll @AfterAll @BeforeEach @AfterEach

-   @BeforeAll：在所有的 @Test @RepeatedTest @ParameterizedTest @TestFactory 之前执行
-   @BeforeEach：在每个测试用例前执行
-   @AfterAll @AfterEach：与before类似，在测试用例之后执行

@RepeatedTest() 执行多次测试

@ParameterizedTest参数化测试

```java
@ParameterizedTest
@ValueSource(strings = { "racecar", "radar", "able was I ere I saw elba" })
void palindromes(String candidate) {
    log.error(candidate);
}
```



@CsvSource csv源支持

```
@ParameterizedTest
@CsvSource({
        "apple,         1",
        "banana,        2",
        "'lemon, lime', 0xF1"
})
void testWithCsvSource(String fruit, int rank) {
    log.error(fruit + rank);
}
```

它也支持从文件导入，例如`@CsvFileSource(resources = "/two-column.csv", numLinesToSkip = 1)`



## spring的测试

@SpringTest

@MockBean

@SpyBean



等等

## mock

Mockito

```xml
<!-- https://mvnrepository.com/artifact/org.mockito/mockito-all -->
<dependency>
    <groupId>org.mockito</groupId>
    <artifactId>mockito-all</artifactId>
    <version>1.10.19</version>
    <scope>test</scope>
</dependency>

```



https://juejin.im/post/6844903631137800206



参考文章：https://dnocm.com/articles/cherry/junit-5-info/(非常详细)