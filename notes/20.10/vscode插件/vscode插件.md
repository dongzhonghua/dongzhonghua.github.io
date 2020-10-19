[TOC]

# 如何写一个vscode插件
vscode支持通过脚手架来初始化一个vscode插件目录。首先安装脚手架。

```
npm install -g yo generator-code
```
然后进入你的目运行 `yo code`。


# 编写

# [上线](https://www.cnblogs.com/liuxianan/p/vscode-plugin-publish.html)

- 方法一：直接把文件夹发给别人，让别人找到vscode的插件存放目录并放进去，然后重启vscode，一般不推荐；
- 方法二：打包成vsix插件，然后发送给别人安装，如果你的插件涉及机密不方便发布到应用市场，可以尝试采用这种方式；
- 方法三：注册开发者账号，发布到官网应用市场，这个发布和npm一样是不需要审核的。


## 本地打包

无论是本地打包还是发布到应用市场都需要借助vsce这个工具。

安装：`npm i vsce -g`
打包成vsix文件：`vsce package`

生成好的vsix文件不能直接拖入安装，只能从扩展的右上角选择Install from VSIX安装。

## 发布到应用市场

### 注册账号
访问 https://login.live.com/ 登录你的Microsoft账号，然后访问： https://aka.ms/SignupAzureDevOps， 进入组织的主页后，点击右上角的Security。点击创建新的个人访问令牌，这里特别要注意Organization要选择all accessible organizations，Scopes要选择Full access，否则后面发布会失败。

### 创建发布账号
获得个人访问令牌后，使用vsce以下命令创建新的发布者：`vsce create-publisher your-publisher-name`

### 发布

```
vsce publish // 发布
vsce publish patch // 增量发布
vsce unpublish (publisher name).(extension name) // 取消发布
```