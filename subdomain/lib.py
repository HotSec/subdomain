#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-03-29 23:56:22
LastEditors: zmf96
LastEditTime: 2022-03-30 01:03:58
FilePath: /subdomain/lib.py
Description: 
'''

from cp_common.base import Plugin
from subdomain import SubDomain


class PluginClass(Plugin):
    usage = [
        {
            "name": "host_list",
            "type": "List[str]",
            "usage": '域名列表，eg: ["baidu.com","bing.com"]',
        }
    ]
    plugin_name = "pysubdomain"
    author = "example"
    version = "0.1.0"

    def __init__(self, **kwargs):
        super().__init__(kwargs)

    def run(self):
        self.logger.info(self.kwargs)
        for host in self.kwargs['host_list']:
            sd = SubDomain({'deep': 1, 'domain': host,
                            'dictname': 'test.txt'})
            sd.run()
            for dom, ips in sd.results.keys():
                self.results.append({
                    "domain": {
                        "domain": dom,
                        "ips": dom
                    }
                })