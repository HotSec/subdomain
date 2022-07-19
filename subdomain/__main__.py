#!/usr/bin/env python
# coding=utf-8

"""
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-03-29 23:40:23
LastEditors: zmf96
LastEditTime: 2022-05-06 12:19:24
FilePath: /subdomain/__main__.py
Description:
"""
import argparse
import json
import sys

from loguru import logger

from subdomain import SubDomain,Version


def main():
    logger.debug("subdomain  version {}".format(Version))
    parser = argparse.ArgumentParser(description="使用aiodns爆破子域名")
    parser.add_argument("-v", "--version", action="version", version=Version)
    parser.add_argument("-f", "--file", type=str, help="指定字典文件", default="default.txt")
    parser.add_argument("-d", "--domain", type=str, help="目标域名")
    parser.add_argument("-s", "--deep", type=int, help="域名深度,默认 1", default=1)
    parser.add_argument("-l", "--listfile", type=str, help="目标文件，一个目标一行")
    args = parser.parse_args()

    params = {}
    if args.domain is None and args.listfile is None:
        logger.error("Please input domain  such as python subdomain -d baidu.com")
        sys.exit()
    params["domain"] = args.domain
    params["deep"] = args.deep
    params["dictname"] = args.file
    logger.error(args)
    if args.domain:
        print(params)
        sd = SubDomain(paras=params)
        sd.run()
        sd.loop.close()
        print(sd.results)

    if args.listfile:
        with open(args.listfile, "r") as fp:
            for target in fp:
                params["domain"] = target.strip()
                print(params)
                sd = SubDomain(paras=params)
                sd.run()
                print(sd.results)
                with open(target.strip() + "_subdomain_result.json", "w") as fp:
                    json.dump(sd.results, fp, ensure_ascii=False)


if __name__ == "__main__":
    main()
