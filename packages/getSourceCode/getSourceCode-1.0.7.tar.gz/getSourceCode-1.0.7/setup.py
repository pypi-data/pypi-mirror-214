# -*- coding: utf-8 -*-

from setuptools import setup


setup(
    name='getSourceCode',
    version='1.0.7',
    author='hxzy',
    author_email='hxzy0220@gmail.com',
    url='https://hxzy.me',
    description=u'Simple way to get contract source code.',
    long_description=open('README.rst', encoding='utf-8').read(),
    packages=['getSourceCode'],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'getCode=getSourceCode:main',
        ]
    }
)