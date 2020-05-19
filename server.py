import argparse
import importlib
import time

from proxypool.tester import Tester
CRAWLER_LS = [
    "proxy_pool_us_2",
    "proxy_pool_us_3",
]

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Start optional redis')
    parser.add_argument('-s', '--server', dest='server', choices=CRAWLER_LS,
                        required=True, help='specify which server should be started')
    args = parser.parse_args()

    if args.server == 'proxy_pool_us_2':
        REDIS_KEY = "proxy_pool_us_2"
        tester = Tester(REDIS_KEY)
        while True:
            print('proxy_pool_us_2 测试器开始运行')
            tester.run()
            time.sleep(20)
    elif args.server == 'proxy_pool_us_3':
        REDIS_KEY = "proxy_pool_us_3"
        tester = Tester(REDIS_KEY)
        while True:
            print('proxy_pool_us_3 测试器开始运行')
            tester.run()
            time.sleep(20)
    else:
        raise ValueError('not support redis')
