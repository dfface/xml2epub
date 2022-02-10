# xml2epub

## Update

**中文文档不再更新**.

### FAQ 

1. 想直接将html字符串生成epub而不需要清理内容？ 
   1. 设置`create_chapter_from_string`的参数`strict`为`False`即可，这表示不会经过内部的清理。
2. 我如何自行清理html字符串然后生成epub？ 
   1. 如果你选择自行获取html字符串并自行清理，那么可以遵循以下步骤： 
      1. 利用爬虫技术获取html字符串，例如`requests.get(url).text`。 
      2. 利用我们暴露的`html_clean`方法清理字符串，例如`html_clean(html_string, tag_clean_list=['sidebar'])`。或者你也可以自己编写
         * 方法来清理字符串，一切都只是为了得到纯净的字符串，你想怎么做的都可以。
         * tag_dictionary 定义了需要保存的所有tag及其class，你可以看看默认值都有什么。 
         * tag_clean_list 定义了需要删除的所有tag，注意这里会直接删除整个tag及其子tag。 
         * class_list 定义了需要删除的所有包含该class内容的tag，也即只要任何一个tag的class属性包含这个列表中的内容，那么这整个tag都会被删除包括其子tag。
      3. 利用`create_chapter_from_string(html_string, strict=False)`方法，特别注意其中的参数``要设置为False，表示会略过我们内部的清理策略。
   2. 一个自定义的例子如 [vuepress2epub.py](./examples/vuepress2epub.py) 所示。

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
