import redis
from random import choice
import re

from proxypool.error import PoolEmptyError
from proxypool.setting import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB
from proxypool.setting import MAX_SCORE, MIN_SCORE, INITIAL_SCORE, DECREASE


class RedisClient(object):

    def __init__(self, redis_key, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, db=db, decode_responses=True)
        self.REDIS_KEY = redis_key

    def add(self, proxy, score=INITIAL_SCORE):
        """
        添加代理，设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        # if not re.match(r'\d+\.\d+\.\d+\.\d+:\d+', proxy):
        if not re.findall(re.compile(r'\d+\.\d+\.\d+\.\d+:\d+'), proxy):
            print('代理不符合规范', proxy, '丢弃')
            return
        if not self.db.zscore(self.REDIS_KEY, proxy):
            # return self.db.zadd(REDIS_KEY, score, proxy)
            # 更新为redis3.0+版本，解决redis3.0更新后的报错，如用旧版本还原上方代码
            return self.db.zadd(self.REDIS_KEY, {proxy: score})

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(self.REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(self.REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(self.REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减{}'.format(DECREASE))
            # return self.db.zincrby(self.REDIS_KEY, proxy, -1)
            # 更新为redis3.0+版本，解决redis3.0更新后的报错，如用旧版本还原上方代码
            return self.db.zincrby(self.REDIS_KEY, -DECREASE, proxy)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(self.REDIS_KEY, proxy)

    def exists(self, proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 是否存在
        """
        return not self.db.zscore(self.REDIS_KEY, proxy) is None

    def max(self, proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print('代理', proxy, '可用，设置为', MAX_SCORE)
        # return self.db.zadd(self.REDIS_KEY, MAX_SCORE, proxy)
        # 更新为redis3.0+版本，解决redis3.0更新后的报错，如用旧版本还原上方代码
        return self.db.zadd(self.REDIS_KEY, {proxy: MAX_SCORE})

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.zcard(self.REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(self.REDIS_KEY, MIN_SCORE, MAX_SCORE)

    def batch(self, start, stop):
        """
        批量获取
        :param start: 开始索引
        :param stop: 结束索引
        :return: 代理列表
        """
        return self.db.zrevrange(self.REDIS_KEY, start, stop - 1)


if __name__ == '__main__':
    conn = RedisClient()
    result = conn.batch(680, 688)
    print(result)
