## maven 命令的格式

 mvn [plugin-name]:[goal-name]，可以接受的参数如下。

> -D 指定参数，如 -Dmaven.test.skip=true 跳过单元测试；
> -P 指定 Profile 配置，可以用于区分环境；
> -e 显示maven运行出错的信息；
> -o 离线执行命令,即不去远程仓库更新包；
> -X 显示maven允许的debug信息；
> -U 强制去远程更新snapshot的插件或依赖，默认每天只更新一次。

## 开发中常用命令

1.  mvn compile 编译源代码
2.  mvn test-compile 编译测试代码
3.  mvn test 运行测试
4.  mvn -Dtest package 打包但不测试。完整命令为：mvn -D maven.test.skip=true package
5.  mvn verify 验证软件包是否有效
6.  mvn install 在本地Repository中安装jar
7.  mvn clean 清除产生的项目
8.  mvn dependency:sources 下载源码
9.  mvn validate 检查项目是否正确，需要的信息是否完善
10. mvn deploy 将最终的构件上传到远程存储库
11. mvn package 打包，根据pom.xml打成war或jar。也会先执行validate、compile以及test。
>   如果pom.xml中设置 war，则此命令相当于mvn war:war
>    如果pom.xml中设置 jar，则此命令相当于mvn jar:jar