#!/opt/homebrew/anaconda3/envs/quantfin/bin/ python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/25 下午2:32
# @Author  : @Zhenxi Zhang
# @File    : test.py
# @Software: PyCharm

# %%

from src.LockonToolkit import decorator_utils


@decorator_utils.cached()
def cached_lower(x):
    ...
    return x.lower()


print(cached_lower("CaChInG's FuN AgAiN!"))

# %%
from src.LockonToolkit import dateutils
print(dateutils.get_trade_days_series(start_date="2023-01-01", series_len=12))

# %%
import logging
from logging import FileHandler

file_handler = FileHandler(filename="test.log")
file_handler.setLevel(logging.INFO)

logger1 = logging.getLogger("test")

logger1.setLevel(logging.DEBUG)

logger1.addHandler(file_handler)

logger2 = logging.getLogger("test.123")

logger1.info('1')
logger2.info('logger2123')