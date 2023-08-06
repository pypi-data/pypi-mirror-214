


###### Sun Jun 18 17:10:46 CST 2023
v0.0.7：添加了get_weibo()

get_weibo(path,id,weibo_name)
path:输入存放路径；
id:微博id；
weibi_name:存放文件夹的名字。


pypi维护指令：

```shell
cd 到pydatawork文件夹
python3 setup.py sdist bdist_wheel # 打包
twine check dist/* # 检查
twine upload dist/* # 上传，需要输入帐号密码

```


###### Sat Jun 17 18:23:38 CST 2023
要升级使用最新的安装包，比较稳定可靠的一种方式是，先卸载旧的，再重装。

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

安装：
```shell
pip3 install pydatawork
```


