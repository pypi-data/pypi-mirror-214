


###### Sun Jun 18 17:10:46 CST 2023

#### get_weibo() 微博图片获取（v 0.1.0）

```shell
get_weibo(path,id,weibo_name)
```
参数说明：
path: 内容存放路径
id: 微博id
weibo_name: 内容存放路径下文件夹的名字


示例：获取梅西的微博id，获取其微博内容

```python
import pydatawork as dw 

path="/home/Desktop/pydatawork"
id="3543420821" # 梅西的微博id。在网页版上能获得链接，链接中u后面的内容即为id ,梅西微博的id为 3543420821  https://weibo.com/u/3543420821
weibo_name="mx"

dw.get_weibo(path,id,weibo_name)
```

#### pypi维护指令

```shell
cd 到pydatawork文件夹
python3 setup.py sdist bdist_wheel # 打包
twine check dist/* # 检查
twine upload dist/* # 上传，需要输入帐号密码

```


###### Sat Jun 17 18:23:38 CST 2023
要升级使用最新的安装包，比较稳定可靠的一种方式是，先卸载旧的，再重装。

#### pydatawork升级方法

卸载：
```shell
pip3 uninstall pydatawork
```

安装：
```shell
pip3 install pydatawork
```

###### Sat Jun 17 17:32:47 CST 2023
修改了导入方式，使用下面的导入方式：
```shell
import pydatawork
```

###### Thu Jun 15 13:23:43 CST 2023
数据工作相关的分享。

#### pydatawork安装

安装：
```shell
pip3 install pydatawork
```


