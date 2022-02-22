#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-02-21 11:06:17
LastEditors: zmf96
LastEditTime: 2022-02-22 03:49:02
FilePath: /tests/test_subdomain.py
Description: 
'''
from subdomain.subdomain import SubDomain, __version__


def test_version():
    assert __version__ == '0.1.1'


def test_subdomain():
    sd = SubDomain({'deep': 1, 'domain': 'www.baidu.com',
                   'dictname': 'default.txt'})
    sd.run()
    print(sd.results)
