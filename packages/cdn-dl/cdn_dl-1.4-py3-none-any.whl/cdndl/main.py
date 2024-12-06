#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import json
from os import path
import os
import random
import re
import signal
from typing import List
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import urllib3
import ipaddress
from urllib.parse import urlparse
from collections import defaultdict
from urllib3.exceptions import ConnectTimeoutError, MaxRetryError

DEBUG = False

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0'
]


urllib3.disable_warnings()

# 注册全局退出监听
def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    os._exit(0)

signal.signal(signal.SIGINT, signal_handler)


def is_ip_address(ip_str: str):
    try:
        ip = ipaddress.ip_address(ip_str)
        return ip is not None
    except ValueError:
        return False

HOSTNAME_PATTERN = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
def is_domain_name(string: str):
    if re.match(HOSTNAME_PATTERN, string):
        return True
    else:
        return False

def is_valid_port(port: int):
    return port > 0 and port < 65535

def parse_cdn_config(hostname: str, cdn_configs: str):
    def parse_str_config(config_str: str, hostname: str):
        def method1(hostname):
            parts = config_str.split()
            ip = parts[0]
            hostname = parts[1] if len(parts) == 2 else hostname
            port = 443
            return hostname, ip, port

        def method2(hostname):
            parts = config_str.split(':')
            ip = parts[0]
            port = 443
            if len(parts) >= 2:
                if is_domain_name(parts[1]):
                    hostname = parts[1]
                else:
                    try:
                        port = int(parts[1])
                    except:
                        port =  -1
            if len(parts) >= 3:
                try:
                    port = int(parts[1])
                except:
                    port = -1
                hostname = parts[2]
            return hostname, ip, port

        for fn in method1, method2:
            hostname, ip, port = fn(hostname)
            if is_domain_name(hostname) and is_ip_address(ip) and is_valid_port(port):
                return hostname, ip, port
        return None, None, None

    hostname_ip_map = defaultdict(list)
    config_lines = []
    for cdn_config in cdn_configs:
        file_path = path.join(cdn_config)
        if path.exists(file_path) and path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    config_lines.append(line)
        else:
            config_lines.append(cdn_config)

    for config_str in config_lines:
        hostname, ip, port = parse_str_config(config_str, hostname)
        if hostname:
            hostname_ip_map[hostname].append((ip, port))
    for k, v in hostname_ip_map.items():
        hostname_ip_map[k] = list(dict.fromkeys(v))
    if DEBUG and hostname_ip_map:
        print()
        print('CDN 配置如下:')
        for k, v in hostname_ip_map.items():
            print('    ',k, v)
        print()
    return hostname_ip_map


def parse_url(url: str):
    parsed_url = urlparse(url)
    return parsed_url.hostname, parsed_url.path

def download_file(url: str, save_path: str, cdn_configs: List[str], ua: bool, ts: int, timeout: int, retry: int):
    def init_cdn_map():
        hostname, _ = parse_url(url)
        cdn_map = parse_cdn_config(hostname, cdn_configs)
        if not cdn_map:
            raise RuntimeError('无法检测到可用CDN, 请检查配置!')
        return cdn_map

    def get_ip_port(hostname: str):
        choices = cdn_map.get(hostname)
        if not choices:
            choices = []
            for _, v in cdn_map.items():
                choices.extend(v)
        used_choices = bad_cdn_map.get(hostname, [])
        available_choices = [choice for choice in choices if choice not in used_choices]
        if available_choices:
            return random.choice(available_choices)
        else:
            return None, None

    res = False
    cdn_map = init_cdn_map()
    headers = {}
    if ua:
        headers.update({'User-Agent': random.choice(USER_AGENTS)})
    bad_cdn_map = defaultdict(list)
    while True:
        def handle_error():
            print('请求{} 异常\n'.format(url))
            bad_cdn_map[hostname].append((ip, port))

        hostname, _ = parse_url(url)
        ip, port = get_ip_port(hostname)
        if not ip:
            print('所有CDN 都无法下载, 退出中... ...')
            break
        print('cdn 配置为: {}:{}:{}'.format(hostname, ip, port))
        pool = urllib3.HTTPSConnectionPool(
            ip,
            assert_hostname=hostname,
            server_hostname=hostname,
            port=port,
            cert_reqs='CERT_NONE',
        )
        headers.update({'Host': hostname})
        try:
            with pool.urlopen('GET', url,
                             redirect=False,
                             headers=headers,
                             assert_same_host=False,
                             timeout=timeout,
                             preload_content=False,
                             retries=urllib3.Retry(retry, backoff_factor=1)) as response:
                # 检查是否为重定向
                print('请求{} 返回 {}\n'.format(url, response.status))
                if response.status in (301, 302, 303, 307, 308) and 'Location' in response.headers:
                    # 获取重定向的 URL
                    url = response.headers['Location']
                    # headers = response.headers
                    continue
                if response.status == 200:
                    total_size = int(response.headers.get('content-length', 0))
                    with open(save_path, 'wb') as file, tqdm(
                        desc=save_path,
                        total=total_size,
                        unit='K',
                        unit_scale=True,
                        unit_divisor=1024,
                    ) as bar:
                        for data in response.stream(ts):
                            file.write(data)
                            bar.update(len(data))
                        response.release_conn()
                        res = True
                        break
                else:
                    handle_error()
                    continue
        except (ConnectTimeoutError, MaxRetryError):
            handle_error()
            continue
        except Exception as e:
            print('下载文件异常:', e)
            break
    return res

def get_cdn():
    def parse_domains():
        domains = []
        for domain in domain_arg:
            if path.exists(domain) and path.isfile(domain):
                with open(domain, 'r', encoding='utf-8') as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if is_domain_name(line):
                            domains.append(line)
            else:
                if is_domain_name(domain):
                    domains.append(domain)
        if not domains:
            raise RuntimeError('未能读取到有效域名, 请检查参数!')
        domains = list(dict.fromkeys(domains))
        return domains

    def init_cdn_map():
        hostname, _ = parse_url(url)
        cdn_map = parse_cdn_config(hostname, cdn_configs)
        return cdn_map

    def get_ip_port(hostname: str, used_choices: list):
        if not cdn_map:
            return None, None
        choices = cdn_map.get(hostname)
        if not choices:
            choices = []
            for _, v in cdn_map.items():
                choices.extend(v)
        available_choices = [choice for choice in choices if choice not in used_choices]
        if available_choices:
            return random.choice(available_choices)
        else:
            return None, None

    def get_dns(domains: List[str]):
        def dns_lookup(domain):
            def dns_lookup_internal():
                dns = []
                used_choices = []
                headers = {'accept': 'application/dns-json'}
                url = api.format(domain)
                hostname, _ = parse_url(url)
                headers.update({'Host': hostname})
                while True:
                    if not cdn_map:
                        print('CDN 为空, 跳过使用CDN 解析')
                        pool = urllib3.HTTPSConnectionPool(
                            hostname,
                            assert_hostname=hostname,
                            server_hostname=hostname,
                            cert_reqs='CERT_NONE',
                        )
                    else:
                        ip, port = get_ip_port(hostname, used_choices)
                        if not ip:
                            print('所有CDN 都无法解析, 退出中... ...')
                            break
                        used_choices.append((ip, port))
                        print('使用CDN: {}:{}:{} 解析 {}'.format(hostname, ip, port, domain))
                        pool = urllib3.HTTPSConnectionPool(
                            ip,
                            assert_hostname=hostname,
                            server_hostname=hostname,
                            cert_reqs='CERT_NONE',
                            port=port
                        )
                    try:
                        with pool.urlopen('GET', url,
                                         redirect=False,
                                         headers=headers,
                                         assert_same_host=False,
                                         timeout=timeout,
                                         preload_content=False,
                                         retries=urllib3.Retry(retry, backoff_factor=1)) as response:
                            json_data = json.loads(response.data.decode('utf-8'))
                            if 'Answer' in json_data:
                                records = json_data['Answer']
                                for record in records:
                                    if record['type'] == 1:
                                        dns.append(record['data'])
                            if response.status == 200:
                                break
                    except Exception as e:
                        if not cdn_map:
                            break
                        continue
                return dns

            print(f"Performing DNS lookup for {domain}...")
            dns = dns_lookup_internal()
            return domain, dns

        dns_map = defaultdict(list)
        with ThreadPoolExecutor(max_workers=threads) as executor:
            future_to_domain = {executor.submit(dns_lookup, domain) for domain in domains}
            for future in as_completed(future_to_domain):
                domain, dns = future.result()
                dns_map[domain] = dns
            executor.shutdown(wait=True)
        for k, v in dns_map.items():
            dns_map[k] = list(dict.fromkeys(v))
        return dns_map

    def save_or_print_hosts():
        if not dns_map:
            print('DNS 记录为空, 请检查域名是否正确!')
            return
        print('DNS 解析记录如下:')
        for k, v in dns_map.items():
            for ip in v:
                line = '{} {}'.format(ip, k)
                print(line)
        if path_arg:
            save_path = path.join(path_arg)
            with open(save_path, 'w', encoding='utf-8') as f:
                for k, v in dns_map.items():
                    for ip in v:
                        line = '{} {}'.format(ip, k)
                        f.write(line)
                        f.write('\n')
            print('hosts 文件已导出到 {}'.format(save_path))

    parser = argparse.ArgumentParser(description='cdn-get 配置')
    parser.add_argument('-o', '--out', type=str, default=None, help='输出hosts 文件路径')
    parser.add_argument('-c', '--cdn', nargs='+', default=[], help='cdn configs配置,支持ip| ip:port |ip:port:host 字串或文本或host文件')
    parser.add_argument('-T', '--thread', type=int, default=8, help='多线程数量')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='下载请求超时时间, 默认10s')
    parser.add_argument('-r', '--retry', type=int, default=3, help='下载请求重试次数, 默认3')
    parser.add_argument('domain', nargs='+', help='需要获取cdn的域名或者文本')
    # 'https://dns.google/resolve?name={}&type=A'
    parser.add_argument('--api', type=str, default='https://dns.alidns.com/resolve?name={}&type=1', help='dns api, 默认ali, 使用CF 使用cf dns')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help="是否打印调试信息")
    args = parser.parse_args()
    domain_arg = args.domain
    path_arg = args.out
    api = args.api
    if api == 'CF':
        api = 'https://cloudflare-dns.com/dns-query?name={}&type=A'
    print('DNS API:', api)
    threads = args.thread
    timeout = args.timeout
    retry = args.retry
    global DEBUG
    DEBUG = args.debug
    domains = parse_domains()
    print('待解析域名列表:', domains)
    cdn_configs = args.cdn
    url = api.format(domains[0])
    cdn_map = init_cdn_map()
    dns_map = get_dns(domains)
    save_or_print_hosts()

def main():
    parser = argparse.ArgumentParser(description='cdn-dl 下载配置')
    parser.add_argument('-u', '--url', type=str, required=True, help='文件下载url')
    parser.add_argument('-o', '--out', type=str, required=True, help='文件下载路径')
    parser.add_argument('cdn', nargs='+', help='cdn configs配置,支持ip| ip:port |ip:port:host 字串或文本或host文件')
    parser.add_argument('-ua', '--use_agent', type=bool, default=False, help='是否使用user agent')
    parser.add_argument('-ts', '--trunk_size', type=int, default=8192, help='下载使用的trunk size, 默认8192')
    parser.add_argument('-t', '--timeout', type=int, default=10, help='下载请求超时时间, 默认10s')
    parser.add_argument('-r', '--retry', type=int, default=3, help='下载请求重试次数, 默认3')
    parser.add_argument('-d', '--debug', action='store_true', default=False, help="是否打印调试信息")
    args = parser.parse_args()
    url = args.url
    save_path = path.join(args.out)
    cdn_config = args.cdn
    ua = args.use_agent
    ts = args.trunk_size
    timeout = args.timeout
    retry = args.retry
    global DEBUG
    DEBUG = args.debug
    res = download_file(url, save_path, cdn_config, ua, ts, timeout, retry)
    msg = '从{} 下载文件到{} {}'.format(url, save_path, '成功' if res else '失败')
    print(msg)

if __name__ == '__main__':
    get_cdn()