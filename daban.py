# 克隆自聚宽文章：https://www.joinquant.com/post/37496
# 标题：首板打板战法，修改参数后年化收益3247.51%
# 作者：tquan

# 克隆自聚宽文章：https://www.joinquant.com/post/29424
# 标题：一个打强势首板的短线策略
# 作者：luckyazhong

# 导入聚宽函数库
#enable_profile()
from jqlib.alpha101 import *
import jqdata
import pandas as pd
from six import BytesIO
from pandas import DataFrame,Series
import numpy as np 
import csv
import os
import xlrd
import math
# 初始化程序, 整个回测只运行一次
def initialize(context):
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    set_slippage(PriceRelatedSlippage(0.0003),type='stock')#

    # # 每天买入股票数量
    # g.daily_buy_count  = 2
###------------------------------------------------------------------------------            
def filter_special(context,stock_list):# 过滤器，过滤停牌，ST，科创，新股.创新
    curr_data = get_current_data()

    stock_list=[stock for stock in stock_list if stock[0:3] != '688'] #过滤科创板'688' 
    stock_list=[stock for stock in stock_list if stock[0:3] != '300']
    stock_list=[stock for stock in stock_list if stock[0:3] != '301']
    stock_list = [stock for stock in stock_list if not curr_data[stock].is_st]
    stock_list = [stock for stock in stock_list if not curr_data[stock].paused] 
    stock_list = [stock for stock in stock_list if 'ST' not in curr_data[stock].name]
    stock_list = [stock for stock in stock_list if '*'  not in curr_data[stock].name]
    stock_list = [stock for stock in stock_list if '退' not in curr_data[stock].name]
    stock_list = [stock for stock in stock_list if  curr_data[stock].day_open>1]
    stock_list = [stock for stock in stock_list if  (context.current_dt.date()-get_security_info(stock).start_date).days>150]

    return   stock_list  
#---------------------------------
time_counter=0
#---------------------------------

# 自动执行
def before_trading_start(context):
    
    global time_counter
    #每天清零时间计数
    time_counter=0
    # 今天要买入的股票
    # 设置我们要操作的股票池
    #---------------------------------
    # 行业代码
    g.stocks_exsit = get_all_securities(types=['stock'], date=context.current_dt).index
    g.stocks_exsit = set(g.stocks_exsit) #当天上市的所有股票，过滤了ST等
    g.today_bought_stocks = set() 
    g.today_filter_stocks = set()
    #--------------更新1日涨停价，收盘价，最低价-----------------
    g.high_limit = history(1,'1d','high_limit',g.stocks_exsit)
    g.high = history(1,'1d','high',g.stocks_exsit)
    g.close = history(1,'1d','close',g.stocks_exsit)
    g.low = history(1,'1d','low',g.stocks_exsit)
    g.volume = history(1,'1d','volume',g.stocks_exsit)
    g.money = history(30,'1d','money',g.stocks_exsit).max()
    #--------------------------------------------
    g.x1 = history(1,'1d','high_limit',g.stocks_exsit)##用来存今日涨停价，后面会重新赋值
    g.x2 = history(1,'1d','high_limit',g.stocks_exsit)##用来存今日开盘价，后面会重新赋值
    g.x3 = history(1,'1d','high_limit',g.stocks_exsit)##用来存今日收盘价，后面会重新赋值
    g.x4 = history(1,'1d','high_limit',g.stocks_exsit)##用来存今日最高价，后面会重新赋值
    for security in (g.stocks_exsit):
        stock_data = get_price(security, end_date=context.current_dt.date(), frequency='daily', fields=['open','close','high','high_limit'],skip_paused=False,fq='pre', count=1)
        g.x1[security][0] = stock_data['high_limit'][0]
        g.x2[security][0] = stock_data['open'][0]
        g.x3[security][0] = stock_data['close'][0]
        g.x4[security][0] = stock_data['high'][0]
    for security in (context.portfolio.positions):
        stock_data = get_price(security, end_date=context.current_dt.date(), frequency='daily', fields=['open','close','high','high_limit'],skip_paused=False,fq='pre', count=1)
        g.x1[security][0] = stock_data['high_limit'][0]
    #----------------------------------------
    g.stocks_exsit = set(filter_special(context,g.stocks_exsit)) #当天上市的所有股票，过滤了ST等
    g.zt_stock=set()
    #股票池
    #获取流通市值数据
    q_cap = query(valuation.code, valuation.circulating_market_cap).filter(valuation.code.in_(g.stocks_exsit))
    df_cap = get_fundamentals(q_cap)
    # 筛选出流通市值小于400亿的股票
    g.stocks_exsit = df_cap[df_cap['circulating_market_cap'] < 400e8]['code']
    for security in (g.stocks_exsit):
        if(g.x4[security][0] == g.x1[security][0]\
        and g.x2[security][0] < g.x1[security][0]\
        and g.close[security][0] < g.high_limit[security][0]):
            g.zt_stock.add(security)
    #print(g.zt_stock)
    #----------------------------------------limit 50w元每只股票max买入
    g.buy_cash = min(context.portfolio.available_cash,500000)
# 在每分钟的第一秒运行, data 是上一分钟的切片数据
#自动执行
def handle_data(context, data):
    #-----------记录时间
    global time_counter
    time_counter += 1
    #------------------处理卖出-------------------
    # 14:50
    if(time_counter>=230):
        for security in context.portfolio.positions:
            if context.current_dt == context.portfolio.positions[security].transact_time:#T + 1
                continue
            if(data[security].close<g.x1[security][0]):#尾盘未涨停
                # 卖出
                order_target(security, 0)
                # 记录这次卖出
                log.info("Selling %s" % (security))

    #-----------------------买入------------------------
    if(g.buy_cash == 0):
        return  
    #开仓条件：10:30以前开仓
    IS_OPEN = time_counter<60 
    if IS_OPEN:#打板
        for security in (g.zt_stock-g.today_filter_stocks):
            #涨了7%
            if((security in context.portfolio.positions)==0\
            and data[security].close/g.close[security][0] >1.07\
            and g.money[security] < 100000000):
                # 仓位控制
                cash_before=context.portfolio.available_cash
                # 数量调整
                # 买入这么多现金的股票
                order_value(security, g.buy_cash)
        
                # 放入今日已买股票的集合
                if(cash_before>context.portfolio.available_cash):#成功买进
                    g.today_bought_stocks.add(security)
                    # 记录这次买入
                    log.info("Buying %s" % (security))
                g.today_filter_stocks.add(security)
    #-----------------
# automated execution
def after_trading_end(context):
    pass
#实时舆情分析
def analyze_great_business():
    return
