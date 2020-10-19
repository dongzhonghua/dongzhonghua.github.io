



[gitee上传文件api](https://gitee.com/api/v5/swagger#/postV5ReposOwnerRepoContentsPath)

[github上传文件api](https://developer.github.com/v3/repos/contents/#create-or-update-file-contents)

这个[网址]([https://stong-chen.github.io/2018/11/06/%E4%BD%BF%E7%94%A8github%E7%9A%84api%E4%B8%8A%E4%BC%A0%E6%96%87%E4%BB%B6%E5%88%B0%E9%A1%B9%E7%9B%AE22/](https://stong-chen.github.io/2018/11/06/使用github的api上传文件到项目22/))讲了怎么申请token和使用这个api。

结合typora可以非常方便的利用GitHub搭建一个私人图床。

之前有很多教程是讲的怎么上传到七牛云阿里云等，但是还是不如这个方便而且也非常稳定。

>   所有xxx的地方都需要替换成你的

```python
import argparse
import base64
import random
import string
import sys
import requests
import json
from urllib.parse import unquote


url = 'https://api.github.com/repos/xxx_username_xxx/xxx_仓库名——xxx/contents/img/blog/'
headers = {'content-type': 'application/json', 'Authorization': 'Bearer xxx_your_token_xxx'}
data = {
    "message": "",
    "committer": {
        "name": "xxx",
        "email": "xxx"
    },
    "content": ""
}
image_name = ''
if len(sys.argv) == 1:
    sys.argv.append('--help')
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--source', type=str, nargs='+', help="必须传入文件名参数", required=True)
args = parser.parse_args()
image_list = args.source


def get_data(img):
    with open(img, "rb") as f:
        file = f.read()
        encode_f = base64.b64encode(file)
    data['content'] = str(encode_f, encoding="utf-8")
    data['message'] = image_name
    return data


if __name__ == '__main__':
    for img in image_list:
        image_name = img.split("/")[-1]
        if len(image_name) > 50:
            image_name = ''.join(random.sample(string.ascii_letters + string.digits, 20)) \
                         + '.' + image_name.split(".")[-1]
        data = get_data(img)
        req = requests.put(url=url + image_name, data=json.dumps(data), headers=headers)
        print(unquote(req.json()['content']['download_url'], 'utf-8'))

```

![image-20200627144920370](https://raw.githubusercontent.com/dongzhonghua/dongzhonghua.github.io/master/img/blog/image-20200627144920370.png)

>   自定义命令填入 python3 xxx/upload.py -s
>
>   -s后面typora会帮你自动填入本地图片路径，使用时直接拖拽图片到typora就自动上传了。





| asdf | asdf |
| ---- | ---- |
|      |      |







autoindex on;

location /video/ {
								alias /Volumes/新加卷/video/;
						}
						
						
						
						
						
						
						
			