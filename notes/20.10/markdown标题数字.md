# title

## a

### b

#### c

### b

#### d

## a

### b

![md标题序号.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/md标题序号.png)
这种方式通过修改css的方式来完成，但是主流的博客网站都不支持，所以这种方式只能在本地来做。
```
<style type="text/css">
h1 {

    counter-reset: h2counter;

}

h2 {

    counter-reset: h3counter;

}

h3 {

    counter-reset: h4counter;

}

h4 {

    counter-reset: h5counter;

}

h5 {

    counter-reset: h6counter;

}

h1 {

    text-align: center;

}

h2:before {

    counter-increment: h2counter;
    content: counter(h2counter) ".\0000a0\0000a0";

}

h3:before {

    counter-increment: h3counter;
    content: counter(h2counter) "." counter(h3counter) ".\0000a0\0000a0";

}

h4:before {

    counter-increment: h4counter;
    content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) ".\0000a0\0000a0";

}

h5:before {

    counter-increment: h5counter;
    content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) "." counter(h5counter) ".\0000a0\0000a0";

}

h6:before {

    counter-increment: h6counter;
    content: counter(h2counter) "." counter(h3counter) "." counter(h4counter) "." counter(h5counter) "." counter(h6counter) ".\0000a0\0000a0";

}
</style>
```