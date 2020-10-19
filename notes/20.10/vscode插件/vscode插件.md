[TOC]

# 如何写一个vscode插件
先说说为什么会萌生了这个开发vscode插件的想法。我在写markdown的时候需要插入图片。本地写的话只能是本地的URI。如果放到别的平台上对于图片的处理是比较麻烦的。目前的解决方案是存到七牛云或者使用pic等等。但是比较不靠谱而且还要配置比较麻烦。所以我的这个插件就是把图片上传到码云的仓库，返回一个URL直接插入到markdown中。

首先要感谢大神的一系列博客https://www.cnblogs.com/liuxianan/p/vscode-plugin-overview.html。写一个简单的vscode插件看这系列文章就够了。我在这里只是简单记录一下我的开发过程。
vscode支持通过脚手架来初始化一个vscode插件目录。首先安装脚手架。

```
npm install -g yo generator-code
```
然后进入你的目运行 `yo code`。
![vscode插件初始化.jpg](https://gitee.com/dongzhonghua/zhonghua/raw/master/img/blog/vscode插件初始化.jpg)
# 编写
vscode支持TypeScript和JavaScript。我用的是JS。进入目录之后大部分的改动都在extension.js和package.json两个文件。
我下面直接把代码贴过来再加一些注释。

vscode的主要配置如下，main表明了入口文件。这里是extention.js。
## package.json
**contributes**：这里定义了如何来触发自己的插件。我定义的是command。也就是通过Ctrl+shift+p然后输入命令。这些命令需要在activationEvents里面注册一下。
configuration：这里定义了一些配置，一些个性化的信息不适合写死在代码里。
输入命令对应的代码会写在extension.js里面。

```json
// package.json
"activationEvents": [
    "onCommand:extention.upload",
    "onCommand:extention.upload_remote",
    "onCommand:extention.upload_local",
    "*"
	],
"main": "./extension.js",
"contributes": {
    "commands": [
        {
            "command": "extention.upload",
            "title": "upload"
        },
        {
            "command": "extention.upload_remote",
            "title": "uploadRemote"
        },
        {
            "command": "extention.upload_local",
            "title": "uploadLocal"
        }
    ],
    "configuration": {
        "type": "object",
        "title": "mdPic配置",
        "properties": {
            "pic.git": {
                "type": "string",
                "default": "null",
                "description": "git仓库"
            },
            "pic.access_token": {
                "type": "string",
                "default": "null",
                "description": "access_token"
            }
        }
    }
},
```
## extenion.js

### 注册命令
首先vscode有一个声明周期函数。插件激活之后会自动进入activate函数。在这个函数里面我们需要把配置的commands注册一下。
`sub.push(vscode.commands.registerCommand('extention.upload_remote', disposeRemotePic));`这行代码标识如果输入upload_remote命令，它对应的回调函数是disposeRemotePic。vscode为我们提供了很多API，比如`vscode.window.showInformationMessage("active!");`就是弹出一个显示active的窗口。

```javascript
// extension.js
/**
 * @param {vscode.ExtensionContext} context
 */
function activate(context) {
	console.log('"md-pic" is now active!');
	const dispos = vscode.commands.registerCommand("extention.upload", function () {
		vscode.window.showInformationMessage("active!");
	});
	context.subscriptions.push(dispos);

	let sub = context.subscriptions;
	sub.push(vscode.commands.registerCommand('extention.upload_remote', disposeRemotePic));
	sub.push(vscode.commands.registerCommand('extention.upload_local', disposeLocalPic));
}
```

### 编写具体的功能实现。

这段代码实现了获取当前行的图片链接，并且下载该图片并转成base64格式编码。下载图片是用的axios。后面上传图片也是是用了这个模块。

```js
function disposeRemotePic() {
	let editor = vscode.window.activeTextEditor;
	let document = editor.document;
	console.log(editor);
	console.log(document);
	const line = editor.selection.active.line;
	let url = document.lineAt(line);
	console.log(url.text);
	const text = '上传第' + line + '行链接图片：' + url.text + ' 至GitHub, 请输入图片名称';
	vscode.window.showInputBox(
		{
			password: false, // 输入内容是否是密码
			ignoreFocusOut: true, // 默认false，设置为true时鼠标点击别的地方输入框不会消失
			placeHolder: 'name', // 在输入框内的提示信息
			prompt: text, // 在输入框下方的提示信息
		}).then(res => {
			const pic_name = res + ".png";
			const pic_url = url.text;
			// upload(res + ".png", url.text);
			console.log('name: ' + pic_name + ', url: ' + pic_url);
			axios.get(encodeURI(pic_url),
				{
					responseType: 'arraybuffer'
				})
				.then(res => uploadGitee(pic_name, Buffer.from(res.data).toString('base64')))
				.catch(function (error) {
					console.log(error);
					vscode.window.showInformationMessage("download image failed, please try again!");
				});
		});
}
```
这段代码是选择一个本地文件并把这个文件转成base64编码。
```js
function disposeLocalPic() {
	vscode.window.showOpenDialog(
		{ // 可选对象
			canSelectFiles: true, // 是否可选文件
			canSelectFolders: false, // 是否可选文件夹
			canSelectMany: true, // 是否可以选择多个
			defaultUri: vscode.Uri.file("./"), // 默认打开本地路径
			openLabel: '上传'
		}).then(function (msg) {
			const path = msg[0].path;
			console.log(path);
			// var data = fs.readFileSync(path.substring(1));
			var data = fs.readFileSync(path);
			const base64Data = Buffer.from(data).toString('base64');
			const paths = path.split("/");
			const pic_name = paths[paths.length - 1];
			uploadGitee(pic_name, base64Data);
		});
}
```
这段代码是吧文件上传到gitee然后返回一个URL。并且调用API插入到文本编辑框里。
```js
function uploadGitee(pic_name, base64_data) {
	const url = vscode.workspace.getConfiguration().get('pic.git');
	const auth = vscode.workspace.getConfiguration().get('pic.access_token');
	const headers = { 'Content-Type': 'application/json', 'charset': 'UTF-8' };
	const jdata = JSON.stringify({
		"access_token": auth,
		"message": pic_name,
		"content": base64_data
	});
	console.log(headers)
	console.log(jdata);

	axios.post(encodeURI(url + pic_name), jdata, {
		headers: headers
	}
	).then(res => {
		console.log(res);
		if (res.status = 200) {
			const git_url = res.data["content"]["download_url"]
			console.log(git_url);
			vscode.window.activeTextEditor.edit(editBuilder => {
				const md_img = "![" + pic_name + "](" + git_url + ")";
				const end = new vscode.Position(vscode.window.activeTextEditor.selection.active.line + 1, 0);
				editBuilder.replace(new vscode.Range(new vscode.Position(vscode.window.activeTextEditor.selection.active.line, 0), end), md_img);
			});
		} else {
			console.error("upload url failed!")
			vscode.window.showInformationMessage("upload url failed, please try again!");
		}
	}).catch(function (error) {
		console.log(error);
		vscode.window.showInformationMessage("upload url failed, please try again!");
	});

}
```
整体的功能比较简单。vscode提供的API相当丰富。这个只是一个比较简单的尝试。

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