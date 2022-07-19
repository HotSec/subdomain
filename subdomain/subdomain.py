#!/usr/bin/env python
# coding=utf-8

"""
Version: 0.1
Autor: zmf96
Email: zmf96@qq.com
Date: 2022-02-21 08:46:14
LastEditors: zmf96
LastEditTime: 2022-05-06 12:00:18
FilePath: /subdomain/subdomain.py
Description: 
"""
import asyncio
import os
import random
import sys

import aiodns
import IPy
from loguru import logger

Version = "0.1.4.11"

BASEDIR = os.path.dirname(os.path.abspath(__file__))


class SubDomain:
    def __init__(self, paras={}):
        self.basedir = os.path.dirname(os.path.abspath(__file__))
        self.deep = paras["deep"]
        self.check_analysis = True  # 通过cname 判断泛解析 这个方法极度损耗性能相当于查询两遍dns
        self.analysis_domain = []
        self.queue = asyncio.Queue(maxsize=3000000)
        self.check_bk = paras["check_bk"] if paras.get("check_bk") else True
        self.black_list = {}  # 黑名单ip  黑明单键值为10
        self.bk_domain = (
            paras["bk_domain"] if paras.get("bk_domain") else []
        )  # openvpn  world.taobao.com 这样的
        self.bk_limit = 10  # 黑名单次数
        self.bk_ipdata = ["127.0.0.0/8", "0.0.0.0/8"]
        self.domain_list = {}
        self.loop = asyncio.new_event_loop()
        self.resolver = aiodns.DNSResolver(loop=self.loop, rotate=True)
        self.resolver.nameservers = ["223.5.5.5", "223.6.6.6", "114.114.114.114"]
        self.domain = paras.get("domain")
        self.dictname = paras["dictname"]
        self.sec_dictname = "test.txt"  # "subdict.txt"  # 递归小字典
        self.semaphore = asyncio.Semaphore(100000)  # 协程并发量  40m带宽
        self.subdomain_list = set()
        self.deep_domain = []
        self.scan_total = 0
        self.find_total = 0
        self.results = {}

    def init_bk(self):
        """
        初始化 黑名单 随机不存在域名 判断泛解析
        :return:
        """
        for _ in range(200):
            self.loop.create_task(self.check_black())

    async def check_black(self):
        subd = "".join(
            random.sample("abcdefghijklmnopqrstuvwxyz", random.randint(6, 12))
        )
        res = await self.query(subd, self.semaphore, "A")
        if res:
            for ip in res:
                self.black_list[ip.host] = self.bk_limit

    async def query(self, sub_domain, sem, q_type, num=1):
        async with sem:
            try:
                sub_domain = sub_domain + "." + self.domain
                return await self.resolver.query(sub_domain, q_type)
            except aiodns.error.DNSError as e:
                err_code, err_msg = e.args[0], e.args[1]
                # 1:  DNS server returned answer with no data
                # 4:  Domain name not found
                # 11: Could not contact DNS servers
                # 12: Timeout while contacting DNS servers
                if err_code not in [1, 4, 11, 12]:
                    return
                if err_code in [11, 12]:
                    # 超时重试 处理
                    if num <= 2:
                        num += 1
                        await self.query(sub_domain, sem, q_type)
                    return
            except Exception as e:
                logger.error(e)
                return

    def is_black(self, ips):
        """
        黑名单相关操作
        :param subdomain:
        :return: true false
        """
        for ip in ips:
            ip_num = self.black_list.get(ip)
            if ip_num:
                if ip_num == self.bk_limit:
                    return False
                else:
                    self.black_list[ip] += 1
            else:
                self.black_list[ip] = 1
            for bkip in self.bk_ipdata:
                if ip in IPy.IP(bkip):
                    return False
        return True

    async def brute_domain(self):
        try:
            while True:
                size = self.queue.qsize()
                if size <= 1000000:
                    if self.deep_domain:
                        sub_text = self.deep_domain[0]
                        self.deep_domain.remove(sub_text)
                        with open(
                            os.path.join(
                                BASEDIR,
                                "dict/" + self.sec_dictname,
                            ),
                            "r",
                        ) as f:
                            for line in f:
                                self.queue.put_nowait(
                                    line.strip().lower() + "." + sub_text
                                )
                sub = await self.queue.get()
                self.scan_total += 1
                # logger.debug("remain " + str(self.scan_total) + "  | Found" +
                #             str(self.find_total) + '\r')
                if self.check_analysis:
                    cname = await self.query(sub, self.semaphore, "CNAME")
                    if cname:
                        cname = cname.cname
                        if cname in self.analysis_domain:
                            continue
                res = await self.query(sub, self.semaphore, "A")
                if res:
                    subdomain = sub + "." + self.domain
                    sub_ips = [r.host for r in res]
                    if self.is_black(sub_ips):
                        self.find_total += 1
                        # logger.info(f'{subdomain} {sub_ips}')
                        self.results[subdomain] = sub_ips
                        logger.info(
                            "remain "
                            + str(self.scan_total)
                            + "  | Found "
                            + str(self.find_total)
                            + " subdomain:"
                            + subdomain
                        )
                        # self.save_and_next(subdomain, sub_ips)
                self.queue.task_done()
        except Exception as e:
            logger.warning(e)

    async def start_brute(self):
        """
        开始爆破
        """
        with open(os.path.join(BASEDIR, "dict/" + self.dictname), "r") as f:
            for line in f:
                domain = line.strip().lower()
                self.queue.put_nowait(domain)
        brute_tasks = [
            self.loop.create_task(self.brute_domain()) for _ in range(10000)
        ]  # 启动10000个协程
        await self.queue.join()
        for task in brute_tasks:
            task.cancel()

    def check_bk_domain(self, domain):
        """
        检查黑名单
        return: True False
        """
        if not self.bk_domain:
            return False
        for bk_domain in self.bk_domain:
            if bk_domain in domain:
                return True
        return False

    def run(self):
        try:
            self.init_bk()
        except Exception as e:
            logger.warning(e)
        try:
            logger.info("启动")
            self.loop.run_until_complete(self.start_brute())
        except Exception as e:
            logger.warning(e)
