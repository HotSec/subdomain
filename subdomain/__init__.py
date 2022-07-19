#!/usr/bin/env python
# coding=utf-8

"""
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-02-21 08:45:43
LastEditors: zmf96
LastEditTime: 2022-05-06 12:17:52
FilePath: /subdomain/__init__.py
Description:
"""

from cp_common.base import Plugin

from .subdomain import SubDomain,Version

__all__ = ["PluginClass", "SubDomain","Version"]


class PluginClass(Plugin):
    usage = [
    ]
    plugin_name = "pysubdomain"
    author = "example"
    version = "0.1.4.11"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self):
        self.logger.info(self.kwargs)
        domain_list = self.kwargs.get("hosts")
        if isinstance(domain_list,str):
            domain_list = domain_list.split(",")
        self.logger.info(domain_list)
        for domain in domain_list:
            sd = SubDomain({"deep": 1, "domain": domain, "dictname": "default.txt"})
            sd.run()
            for dom, ips in sd.results.items():
                self.results.append({"domain": {"domain": dom, "ips": ips}})
            sd.loop.close()
