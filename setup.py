from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='xml2epub',
    version='1.9',
    author='dfface',
    author_email='dfface@sina.com',
    description='将 html链接, html文件 或 html文本 转换成 epub文件，并自动添加封面.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dfface/xml2epub',
    packages=['xml2epub'],
    package_data={'xml2epub': ['epub_templates/*', ]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4',
        'jinja2',
        'requests',
    ]
)
