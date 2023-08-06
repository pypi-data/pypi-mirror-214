# 部署包说明

注意以下pip，python均表示的是3.x以上的python

## 本地源码安装部署包

```bash
pip install log4py
python {pack}_setup.py install
```

## 生成部署包

```bash
# 构建一个二进制的分发包（zip)
python {pack}_setup.py bdist
# 构建一个 egg 分发包，经常用来替代基于 bdist 生成的模式(.egg)
python {pack}_setup.py bdist_egg
# 构建一个 wheel 分发包，egg 包是过时的，whl 包是新的标准
python {pack}__setup.py bdist_wheel
```
