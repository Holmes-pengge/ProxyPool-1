PRODUCTION_ENV = True

# Redis数据库地址
REDIS_HOST = "45.34.33.156" if PRODUCTION_ENV else '127.0.0.1'

# Redis端口
REDIS_PORT = "12111" if PRODUCTION_ENV else '6379'

# Redis密码，如无填None
REDIS_PASSWORD = "513f21fbc55d446186c7f1daa9dae626" if PRODUCTION_ENV else None

# REDIS_KEY = ''

REDIS_DB = 10

# 代理分数
MAX_SCORE = 100
MIN_SCORE = 20
INITIAL_SCORE = 10

VALID_STATUS_CODES = [200, 302]

# 代理池数量界限
POOL_UPPER_THRESHOLD = 50000

# 检查周期
TESTER_CYCLE = 20
# 获取周期
GETTER_CYCLE = 300

# 测试API，建议抓哪个网站测哪个
# TEST_URL = 'http://www.baidu.com'
# TEST_URL = 'https://www.1688.com/'
TEST_URL = 'https://www.ebay.com/'

# API配置
API_HOST = '0.0.0.0'
API_PORT = 5555

# 开关
TESTER_ENABLED = True
GETTER_ENABLED = True
API_ENABLED = True

# 最大批测试量
BATCH_TEST_SIZE = 20

# 每次减小的分数
DECREASE = 5

# 请求超时设置
TIMEOUT = 30