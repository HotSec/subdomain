#!/usr/bin/env python
# coding=utf-8

'''
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-03-29 23:40:23
LastEditors: zmf96
LastEditTime: 2022-03-29 23:40:23
FilePath: /subdomain/__main__.py
Description: 
'''
from loguru import logger
import sys
import argparse
from subdomain import __version__,SubDomain

def main():
    logger.debug("subdomain  version 0.1")
    parser = argparse.ArgumentParser(description='使用aiodns爆破子域名')
    parser.add_argument("-v", "--version",
                        action='version', version=__version__)
    parser.add_argument("-f", "--file", type=str,
                        help='指定字典文件', default='default.txt')
    parser.add_argument("-d", "--domain", type=str,
                        help='目标域名', required=True)
    parser.add_argument("-s", "--deep", type=int, help='域名深度,默认 1', default=1)
    args = parser.parse_args()
    params = {}
    if args.domain is None:
        logger.error(
            "Please input domain  such as python subdns.py -u baidu.com")
        sys.exit()
    params['domain'] = args.domain
    params['deep'] = args.deep
    params['dictname'] = args.file
    sd = SubDomain(paras=params)
    sd.run()
    print(sd.results)


if __name__ == '__main__':
    main()
