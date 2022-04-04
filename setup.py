from setuptools import setup

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='xml2epub',
    version='2.6',
    author='dfface',
    author_email='dfface@sina.com',
    keywords="convert html url export epub",
    description='Batch convert multiple web pages into one e-book by URL, xml string, etc.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/dfface/xml2epub',
    packages=['xml2epub'],
    package_data={'xml2epub': ['epub_templates/*', 'epub_cover/*', 'epub_cover/animals/*']},
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'beautifulsoup4',
        'jinja2',
        'requests',
        'lxml',
        'pillow'
    ]
)
