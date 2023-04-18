import os
from loguru import logger


os.makedirs('log', exist_ok=True)
# 放在 log/log_{time:YYYYMMDD}.log 文件，只记录 INFO 信息
logger.add('log/log_{time:YYYYMMDD}.log',
           format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | {message}",
           level="INFO")
