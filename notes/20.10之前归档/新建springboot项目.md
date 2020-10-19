

# springboot热部署

热部署依赖：https://blog.csdn.net/liu_shi_jun/article/details/79985575

        <dependency> <!--添加热部署依赖 -->
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-devtools</artifactId>
        </dependenc>
        <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
                <configuration>
                    <fork>true</fork>
                </configuration>
            </plugin>
        </plugins>
    </build>
```
debug: true
spring:
  devtools:
    restart:
      enabled: true  #设置开启热部署
  freemarker:
    cache: false    #页面不加载缓存，修改即时生效
```

但我觉得用处不太大，不知道什么时候他会更新，大多数不需要的时候刷新还会报错。

### 真正的热部署

因为要编辑前端用到thymleaf， 每次都要重启项目非常麻烦。开启idea的热部署会非常方便。更改html文件reload一下，大概两三秒就可以了。更改java代码还是会重启但是比自己重启会快一些。

在设置Compiler里勾选Build project automatically。->之后按住Ctrl+shift+alt+/进入Redistry，勾选compiler.automake.allow.when.app.running。就可以了，然后在工具栏run->里Reload changed class可以手动热部署。

# swagger

参考https://www.jianshu.com/p/05be40b9a7a3

```maven
        <dependency><!--添加Swagger依赖 -->
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger2</artifactId>
            <version>2.9.2</version>
        </dependency>
        <dependency><!--添加Swagger-UI依赖 -->
            <groupId>io.springfox</groupId>
            <artifactId>springfox-swagger-ui</artifactId>
            <version>2.9.2</version>
        </dependency>

```

```java
package xyz.dsvshx.blog.config;

import io.swagger.annotations.Api;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import springfox.documentation.builders.ApiInfoBuilder;
import springfox.documentation.builders.PathSelectors;
import springfox.documentation.builders.RequestHandlerSelectors;
import springfox.documentation.service.ApiInfo;
import springfox.documentation.spi.DocumentationType;
import springfox.documentation.spring.web.plugins.Docket;
import springfox.documentation.swagger2.annotations.EnableSwagger2;

@Configuration
@EnableSwagger2
public class Swagger2Configuration {

    @Bean
    public Docket createRestApi() {
        return new Docket(DocumentationType.SWAGGER_2)
                .apiInfo(apiInfo())
                .select()
                .apis(RequestHandlerSelectors.withClassAnnotation(Api.class))//这是注意的代码
                .paths(PathSelectors.any())
                .build();
    }

    private ApiInfo apiInfo() {
        return new ApiInfoBuilder()
                .title("Blog接口文档")
                .description("Blog相关接口的文档")
                .termsOfServiceUrl("http://www.dsvshx.xyz")
                .version("1.0")
                .build();
    }

}
```

注意的这行代码：apis(RequestHandlerSelectors.withClassAnnotation(Api.class)),这个代码说明的我们扫描的哪些接口，我这行意思是扫描带@Api注解的接口类，这里selector有5个方法来应对扫描需求，其中basePackage()方法是按照接口类所在的包的位置(在我的代码中这里就应该填“ cn.zh.demo.controller”）,需多的人说这个配置类应该与Application类在同一级目录，但是我实际测试是不需要的，放在自己想要的放的位置即可。

```java
@Api： 描述 Controller
@ApiIgnore： 忽略该 Controller，指不对当前类做扫描
@ApiOperation： 描述 Controller类中的 method接口
@ApiParam： 单个参数描述，与 @ApiImplicitParam不同的是，他是写在参数左侧的。如（ @ApiParam(name="username",value="用户名")Stringusername）
@ApiModel： 描述 POJO对象
@ApiProperty： 描述 POJO对象中的属性值
@ApiImplicitParam： 描述单个入参信息
@ApiImplicitParams： 描述多个入参信息
@ApiResponse： 描述单个出参信息
@ApiResponses： 描述多个出参信息
@ApiError： 接口错误所返回的信息



@Api(value = "AdminUserController ")
@RestController
@RequestMapping("/admin/user")
public class AdminUserController extends BaseController {
    /**
     * 用户登录
     */
    @ApiOperation(value = "登录")
    @ApiImplicitParams({@ApiImplicitParam(name = "userName", value = "用户名", required = true, dataType = "String"),
            @ApiImplicitParam(name = "password", value = "密码", required = true, dataType = "String")})
    @PostMapping("/login")
    @SystemControllerLog(description = "/admin/user/login")
    public ResultVO login(String userName, String password){}
```

https://blog.csdn.net/xtj332/article/details/80595768

配置了fastjson出现了访问不到的情况，上面是解决方案。

# 阿里云OSS





# 自己作图床。

**一、原理分析**

浏览器提供了 copy 命令 ，可以复制选中的内容

```
document.execCommand("copy")
```

如果是输入框，可以通过 **select()** 方法，选中输入框的文本，然后调用 copy 命令，将文本复制到剪切板

但是 select() 方法只对 <input> 和 <textarea> 有效，对于 <p> 就不好使

 

最后我的解决方案是，在页面中添加一个 <textarea>，然后把它隐藏掉

**点击按钮的时候，先把  的 value 改为 <p> 的 innerText，然后复制 <textarea> 中的内容**

 

**二、代码实现**

 https://www.cnblogs.com/wisewrong/p/7473978.html 

HTML 部分

```
<style type="text/css">
   .wrapper {position: relative;}
   #input {position: absolute;top: 0;left: 0;opacity: 0;z-index: -10;}
</style>

<div class="wrapper">
   <p id="text">我把你当兄弟你却想着复制我？</p>
   <textarea id="input">这是幕后黑手</textarea>
   <button onclick="copyText()">copy</button>
</div>
```

[![复制代码](https://common.cnblogs.com/images/copycode.gif)](javascript:void(0);)

 

JS 部分

```
  <script type="text/javascript">
    function copyText() {
      var text = document.getElementById("text").innerText;
      var input = document.getElementById("input");
      input.value = text; // 修改文本框的内容
      input.select(); // 选中文本
      document.execCommand("copy"); // 执行浏览器复制命令
      alert("复制成功");
    }
  </script>
```

我觉得可以自己做一个图床啊，实现原理很简单就是后台就一两个接口，前端就是显示图片加上链接，可以有一个复制功能。这就很简单了。有时间可以试一试。

