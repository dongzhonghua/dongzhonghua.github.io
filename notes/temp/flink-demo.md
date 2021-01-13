## 你要搭建一个什么系统

在当今数字时代，信用卡欺诈行为越来越被重视。 罪犯可以通过诈骗或者入侵安全级别较低系统来盗窃信用卡卡号。 用盗得的信用卡进行很小额度的例如一美元或者更小额度的消费进行测试。 如果测试消费成功，那么他们就会用这个信用卡进行大笔消费，来购买一些他们希望得到的，或者可以倒卖的财物。

在这个教程中，你将会建立一个针对可疑信用卡交易行为的反欺诈检测系统。 通过使用一组简单的规则，你将了解到 Flink 如何为我们实现复杂业务逻辑并实时执行。

```bash
mvn archetype:generate \
    -DarchetypeGroupId=org.apache.flink \
    -DarchetypeArtifactId=flink-walkthrough-datastream-java \
    -DarchetypeVersion=1.10.2 \
    -DgroupId=xyz.dsvshx \
    -DartifactId=flink-demo \
    -Dversion=0.1 \
    -Dpackage=spendreport \
    -DinteractiveMode=false
```

