# xml2epub

## Update

### 介绍

原项目已经较为成熟 [Html2Epub](https://github.com/zzZ5/Html2Epub) ，此次更改是为了满足自身需求，主要是取消 html string 的清洗：

* 关于页面清洗：html string 通过 `create_chapter_from_string` 的参数 `strict` 控制，`False` 表示不清洗
* 关于封面：xml string 中如果包含`<title>封面</title>`或者`<title>cover</title>`等，则应该自动生成 epub 文件的封面
* 关于替换静态资源，做的改进是：
  * 图片的名称由`uuid`改为`md5(url)` 作为名称(128位 16个字符)，图片文件夹为 img
  * 提取页面中的 css 并保存在 css 文件夹中

### 使用示例

```python
import xml2epub

epub = xml2epub.Epub('My First Epub')
chapter = xml2epub.create_chapter_from_url('https://en.wikipedia.org/wiki/EPUB')
epub.add_chapter(chapter)
epub.create_epub('OUTPUT_DIRECTORY')
```

### 源码推送到pipy

参考：https://zhuanlan.zhihu.com/p/37987613

```bash
pip3 install setuptools
pip3 install wheel
# 打包
python3 setup.py sdist bdist_wheel

pip3 install twine
# 上传
twine upload dist/*
```

### 参考文献

1. *[wcember/pypub: Python library to programatically create epub files](https://github.com/wcember/pypub).*
2. *[EPUB - Wikipedia](https://en.wikipedia.org/wiki/EPUB).*
