[TOC]

## 机器A 向 机器B 进行免密码登陆

### step1生成公私钥：

 在机器A中生成 私钥和公钥：

ssh-keygen -t rsa

此时在 ~/.ssh/ 目录下生成了公钥（id_rsa.pub）和私钥(id_rsa)

### step2复制公钥：

把机器A的公钥（id_rsa.pub）复制到机器B ~/.ssh/authorized_keys 文件里，两种常用方法

#### 方法1：

scp ~/.ssh/id_rsa.pub username@host:/home/B/id_rsa.pub

//此时scp需要输入 登录机器B username用户的密码

//然后进入机器B内把 /home/B/id_rsa.pub 文件内容加写进 ~/.ssh/authorized_keys 文件：

cat /home/B/id_rsa.pub /home/B/.ssh/authorized_keys

#### 方法2：

//在机器A中使用 ssh-copy-id 把公钥加写到机器B的 ~/.ssh/authorized_keys 文件

ssh-copy-id username@host

//执行后输入机器B username用户的密码，效果和方法1一样

### step3修改权限：

修改机器B ~/.ssh/authorized_keys 文件的权限：

chmod 600 ~/.ssh/authorized_keys

 此时如果机器B没有~/.ssh 目录需要手动创建

### step4免密登录：

此时机器A可以进行免验证登录 机器B

ssh username@host

### 小结

登录的机子要有私钥，被登录的机子要有登录机子的公钥。这个公钥/私钥对一般在私钥宿主机产生。上面是用rsa算法的公钥/私钥对，当然也可以用dsa(对应的文件是id_dsa，id_dsa.pub)想让A，B机无密码互登录，那B机以上面同样的方式配置即可。

SSH 为建立在应用层和传输层基础上的安全协议。SSH 是目前较可靠，专为远程登录会话和其他网络服务提供安全性的协议。利用SSH 协议可以有效防止远程管理过程中的信息泄露问题。

 从客户端来看，SSH提供两种级别的安全验证：

 

1、基于口令的验证

   只要知道帐号和口令，就可以登录到远程主机。所有传输的数据都会被加密，但缺点是：不能保证你正在连接的服务器就是你想连接的服务器。以下是我画了的登录验证流程：

![ssh登录验证流程.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/ssh登录验证流程.png)
 当第一次链接远程主机时，会提示您当前主机的”公钥指纹”，询问您是否继续，如果选择继续后就可以输入密码进行登录了，当远程的主机接受以后，该台服务器的公钥就会保存到~/.ssh/known_hosts文件中。

2、基于密钥的验证 

  这种验证的前提是客户端需要生成一对密钥，将公钥放到需访问的远程服务器。这种验证比上一种的好处是，不能仿冒真正的服务器，因为要仿冒必须拿到客户端生成的公钥。缺点就是验证等待过程稍长些。

![ssh.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/ssh.png)
![ssh工作过程.png](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/ssh工作过程.png)
1. 在A上生成公钥私钥。
2. 将公钥拷贝给server B，要重命名成authorized_keys(从英文名就知道含义了)
3. Server A向Server B发送一个连接请求。
4. Server B得到Server A的信息后，在authorized_key中查找，如果有相应的用户名和IP，则随机生成一个字符串，并用Server A的公钥加密，发送给Server A。
5. Server A得到Server B发来的消息后，使用私钥进行解密，然后将解密后的字符串发送给Server B。Server B进行和生成的对比，如果一致，则允许免登录。

总之：A要免密码登录到B，B首先要拥有A的公钥，然后B要做一次加密验证。对于非对称加密，公钥加密的密文不能公钥解开，只能私钥解开。

## 解决多个ssh public key的问题


### 第一步
```shell
ssh-keygen -t rsa -C "dongzhonghua03@kuaishou.com" -f ~/.ssh/id_rsa_dongzhonghua03
```

### 第二步 添加公钥到gitlab

### 第三步 添加密钥到ssh-agent中

```shell
exec ssh-agent bash
ssh-add ~/.ssh/id_rsa_dongzhonghua03
ssh-add ~/.ssh/id_rsa
```

### 第四步添加config配置文件分别映射不同的GitHub和码云的账户下

 进入~/.ssh目录，新建config文件，并添加下面的内容
```
# 个人的GitHub公钥
Host github.com
HostName github.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa_github # 指定特定的ssh私钥文件
# 公司的's gitee.com
Host gitee.com
HostName gitee.com
PreferredAuthentications publickey
IdentityFile ~/.ssh/id_rsa # 指定特定的ssh私钥文件
```
### 第五步 检查配置是否成功执行下面命令

```shell
ssh -T git@github.com
```

