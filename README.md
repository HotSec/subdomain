<!--
 * @Version: 0.1
 * @Autor: zmf96
 * @Email: zmf96@qq.com
 * @Date: 2022-02-21 08:41:27
 * @LastEditors: zmf96
 * @LastEditTime: 2022-02-22 03:49:57
 * @FilePath: /README.md
 * @Description: 
-->
# subdomain
使用异步协程的子域名爆破工具

采用cname与黑名单ip的方式来处理泛解析.

## 安装

python3.8.10 

```bash
git clone https://github.com/HotSec/subdomain
cd subdomain
pip3 install poetry
poetry install
poetry shell

python subdomain/subdomain.py -h
```
## usage

```bash
usage: subdomain.py [-h] [-v] [-f FILE] -d DOMAIN [-s DEEP]

使用aiodns爆破子域名

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f FILE, --file FILE  指定字典文件
  -d DOMAIN, --domain DOMAIN
                        目标域名
  -s DEEP, --deep DEEP  域名深度,默认 1
```

## Thanks

subdomain在[subdns](https://github.com/ldbfpiaoran/subdns.git)的基础上进行开发的.