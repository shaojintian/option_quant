#!/usr/bin/env python
# coding: utf-8

# In[2]:


from platform import python_version
import sys
import pandas as pd
import numpy as np
import jqdatasdk as jq
import jqfactor_analyzer as ja
import numba
import yfinance as yf
print(sys.executable)
print(python_version())


# In[3]:


jq.auth('15340861099','Shaojintian316!')
jq.get_account_info()


# In[4]:


# 获取5日平均换手率因子2018-01-01到2018-12-31之间的数据（示例用从库中直接调取）
# 聚宽因子库数据获取方法在下方
from jqfactor_analyzer.sample import VOL5
factor_data = VOL5

# 对因子进行分析
far = ja.analyze_factor(
    factor_data,  # factor_data 为因子值的 pandas.DataFrame
    quantiles=10,
    periods=(1, 10),
    industry='jq_l1',
    weight_method='avg',
    max_loss=0.1
)

# 获取整理后的因子的IC值
far.ic


# In[30]:


tqqq = yf.Ticker("TQQQ")

# get all stock info
tqqq.history(period="1mo")
#tqqq.history?


# In[30]:


#hushen 300


# In[4]:





# In[4]:





# In[4]:





# In[ ]:




