'''
bc-cu,jm-j,rb-hcy,wr-rb,SF-SM,不做农产品

跨品种套利，大户持仓alpha，隔夜跳空alpha

大幅盈利后此品种冷冻一天
'''
from jqdata import *
import talib
import pandas as pd
import numpy as np
import datetime
import time
import re


## main函数
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    # # 过滤掉order系列API产生的比error级别低的log
    log.set_level('order', 'info')
    # 输出内容到日志 log.info()
    # log.info('初始函数开始运行且全局只运行一次')
    set_option('avoid_future_data', True)
    # 设定全局函数
    # 数据获取周期
    context.LONGPERIOD = 45

    # 交易日数统计
    context.day = 0

    # 记录买入价
    g.porfolio_long_price = {}
    g.porfolio_short_price = {}

    # 合约交易单位
    g.MarginUnit = {
        'AP': 10,  # 苹果
        'BU': 10,  # 石油沥青
        'FG': 20,  # 玻璃
        'RB': 10,  # 螺纹钢
        'Y': 10,  # 豆油
        'ZC': 100,  # 动力煤
        'AG': 15,  # 白银
        'P': 10,  # 棕榈油
        'TA': 5,  # PTA
        'AU': 1000,  # 黄金
        'CU': 5,  # 铜
        'BC': 5,  # 铜
        'RU': 10,  # 天然橡胶
        'J': 100,  # 焦炭
        'M': 10,  # 豆粕
        'CF': 5,  # 一号棉花
        'SA': 20,  # 纯碱
        'ZN': 5,  # 锌
        'I': 100,  # 铁矿石
        'MA': 10,  # 甲醇
        'SR': 10,  # 白糖
        'UR': 20,  # 尿素
        'IF': 300,  # 沪深300指数期货
        'IH': 300,  # 上证50指数期货
        'IC': 300,  # 中证500指数期货
        'SC': 1000,  # 原油期货
        'CY': 5,  # 棉纱
        'CF': 5,  # 一号棉花
        'HC': 10,  # 热轧卷板,
        'JM': 60,  # 焦煤,
        'SM': 5,  # 锰硅
        'SF': 5,  # 硅铁
        'BU': 10,  # 石油沥青
        'PG': 20,  # 液化石油气
        'PP': 10,  # 聚丙烯
        'A': 10,  # 豆一
        'B': 10,  # 豆二
        'C': 10,  # 玉米
        'NI': 10
    }

    #
    # g.arb_symbol_map = {'BC': 'CU', 'JM': 'J', 'RB': 'HC', 'WR': 'RB', 'CU': 'BC', 'J': 'JM', 'HC': 'RB', 'RB': 'WR','SC':'BU','BU':'SC','SF':'SM','SM':'SF'}
    #
    g.future_list = []

    #
    g.sigma_map = {'SC': 6.375640569358063, 'PG': 190.1044335735892, 'AU': 17.03821842384503, 'AG': 12.61001387782865,
                   'CU': 172.44108241750672, 'PB': 24.702821743751425, 'NI': 1070.4645854004036,
                   'BC': 124.35170270517659, 'A': 14.067671754262467, 'B': 53.20238059150891, 'M': 107.49381811814531,
                   'JM': 285.2695975101679, 'J': 253.29246942819242, 'C': 15.321203083083677, 'CS': 17.389973884029835,
                   'MA': 20.40693932061619, 'PP': 70.17807152517443, 'RU': 54.8160030084124, 'Y': 42.272713109759735,
                   'P': 75.79859330603409, 'AL': 70.1085204367706, 'ZN': 77.34070340695777, 'SN': 706.3942448926812,
                   'RB': 46.67928778074428, 'HC': 45.473493537003044, 'BU': 52.92817597361261, 'FU': 72.16448621141586,
                   'SP': 30.910601446650347, 'WR': 72.85730273715303, 'SS': 64.72623472597093, 'SA': 129.8330350067947,
                   'UR': 71.21139713037063, 'SR': 13.099140634199928, 'CF': 59.978654445813774,
                   'TA': 29.925825593564088, 'FG': 63.855962484042614, 'RS': 102.8452652419582, 'OI': 37.39428667723043,
                   'IF': 10.47937416284728, 'IC': 12.624213340003875, 'IH': 5.926359223467202}
    g.mean_map = {'SC': 1.7807620349715767, 'PG': -61.37475843615282, 'AU': -0.2572692488420486,
                  'AG': -1.781737849779087, 'CU': 42.20450542319458, 'PB': 1.2195059712156782, 'NI': 248.90177039300212,
                  'BC': 9.151633764465624, 'A': 2.2447748513169072, 'B': 10.672946951104398, 'M': 33.36655574043261,
                  'JM': 36.45579964433906, 'J': 30.237430755206507, 'C': 3.7168914669089386, 'CS': 4.1985948127662756,
                  'MA': -5.062662116040956, 'PP': 6.144449562413635, 'RU': -5.624665954035275, 'Y': 7.492476925022126,
                  'P': 5.395820895522388, 'AL': 17.084799636735156, 'ZN': 17.388117953165654, 'SN': -37.6961612067995,
                  'RB': -10.953604193971167, 'HC': 0.9564479980616634, 'BU': 13.766867687232617,
                  'FU': 21.28536701827495, 'SP': -7.433457081786478, 'WR': 2.88459250446163, 'SS': 3.9358349441129508,
                  'SA': 48.737136684996074, 'UR': 28.472015791918253, 'SR': 2.706112992336482,
                  'CF': -15.584020842379505, 'TA': -1.1816079873883343, 'FG': 21.85346142116499,
                  'RS': 1.5278372591006424, 'OI': -0.4571840923669019, 'IF': 0, 'IC': 0, 'IH': 0}

    # kline frequency
    g.freqBase = '1m'
    g.freqMid = '7m'
    g.freqHigh = '5d'
    #
    g.temp_removed_future_list = []

    ### 期货相关设定 ###
    # 合约保证金比例
    context.inc = 0.15
    # 设定账户为金融账户
    set_subportfolios([SubPortfolioConfig(cash=context.portfolio.starting_cash, type='futures')])
    # 期货类每笔交易时的手续费是：买入时万分之0.2,卖出时万分之0.2,平今仓为万分之2
    set_order_cost(OrderCost(open_commission=0.00002, close_commission=0.00002, close_today_commission=0.0002),
                   type='index_futures')
    # 设定保证金比例
    set_option('futures_margin_rate', context.inc)

    # 设置期货交易的滑点
    set_slippage(StepRelatedSlippage(2))
    # 运行函数（reference_security为运行时间的参考标的；传入的标的只做种类区分，因此传入'IF8888.CCFX'或'IH1602.CCFX'是一样的）
    # 注意：before_open/open/close/after_close等相对时间不可用于有夜盘的交易品种，有夜盘的交易品种请指定绝对时间（如9：30）

    # 开盘前运行
    run_daily(before_market_open, time='8:30', reference_security='FG8888.XZCE')
    # 开盘时运行
    run_daily(market_open, time='9:00', reference_security='FG8888.XZCE')
    # 交易
    run_daily(TRADE, time='9:31', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='10:00', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='10:30', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='11:00', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='11:30', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='14:00', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='14:30', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='14:50', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='21:30', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='22:00', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='22:30', reference_security='FG8888.XZCE')
    run_daily(TRADE, time='23:00', reference_security='FG8888.XZCE')

    # 节假日前清仓
    run_weekly(JIEJIARI, weekday=-1, time='9:30', reference_security='FG8888.XZCE')
    # 收盘记录
    run_daily(after_market_close, time='15:30', reference_security='FG8888.XZCE')
    # # 风控止损
    # run_daily(stop_loss_monitor, time='21:00', reference_security='FG8888.XZCE')


## 开盘前运行函数
def before_market_open(context):
    # 输出运行时间
    # log.info('函数运行时间(before_market_open)：'+str(context.current_dt.time()))

    # 给微信发送消息（添加模拟交易，并绑定微信生效）
    # send_message('美好的一天~')

    ## 获取要操作的股票(g.为全局变量)
    # 获取当月指数期货合约
    g.AP = get_dominant_future('AP')
    g.BU = get_dominant_future('BU')
    g.FG = get_dominant_future('FG')
    g.RB = get_dominant_future('RB')
    g.Y = get_dominant_future('Y')
    g.AG = get_dominant_future('AG')
    g.P = get_dominant_future('P')
    g.TA = get_dominant_future('TA')
    g.AU = get_dominant_future('AU')
    g.CU = get_dominant_future('CU')
    g.BC = get_dominant_future('BC')
    g.RU = get_dominant_future('RU')
    g.J = get_dominant_future('J')
    g.M = get_dominant_future('M')
    g.CF = get_dominant_future('CF')
    g.SA = get_dominant_future('SA')
    g.ZN = get_dominant_future('ZN')
    g.MA = get_dominant_future('MA')
    g.I = get_dominant_future('I')
    g.SR = get_dominant_future('SR')
    g.UR = get_dominant_future('UR')
    g.IF = get_dominant_future('IF')
    g.IH = get_dominant_future('IH')
    g.IC = get_dominant_future('IC')
    g.SC = get_dominant_future('SC')
    g.WR = get_dominant_future('WR')
    g.JM = get_dominant_future('JM')
    g.CY = get_dominant_future('CY')
    g.HC = get_dominant_future('HC')
    g.SF = get_dominant_future('SF')
    g.SM = get_dominant_future('SM')
    g.PP = get_dominant_future('PP')
    g.PG = get_dominant_future('PG')
    g.A = get_dominant_future('A')
    g.B = get_dominant_future('B')
    g.NI = get_dominant_future('NI')
    g.ZN = get_dominant_future('ZN')

    # 更新list
    # bc-cu,jm-j,rb-hc,cf-cy,wr-rb,SF,S
    g.future_list = list(
        set([g.SC, g.CU, g.BC, g.M, g.JM, g.J, g.Y, g.P, g.PP, g.A, g.B, g.PG, g.NI, g.ZN, g.IC, g.IF, g.AG, g.AU]))

    ## 移除暂时冻结的合约
    g.future_list = [item for item in g.future_list if item != '']
    for x in g.temp_removed_future_list:
        if x in g.future_list:
            g.future_list.remove(x)


## 开盘时运行函数
def market_open(context):
    # log.info('函数运行时间(market_open):'+str(context.current_dt.time()))
    # future_list = {g.AP, g.BU, g.FG, g.RB, g.Y, g.AG, g.P, g.TA, g.AU, g.CU, g.RU, g.J, g.M, g.CF, g.SA, g.ZN, g.I,
    #               g.MA}
    # future_list = {item for item in future_list if item != ''}
    # log.info(future_list)
    future_list = g.future_list
    # 获取合约数量
    context.num = len(future_list)

    # 主力合约切换主动平仓，使用下面的代码
    for future in context.portfolio.short_positions.keys():
        if future not in g.future_list:
            order_target_value(future, 0, side='short')
            g.porfolio_short_price[future] = 0
    for future in context.portfolio.long_positions.keys():
        if future not in g.future_list:
            order_target_value(future, 0, side='long')
            g.porfolio_long_price[future] = 0
    # 主力合约切换以后不主动平仓，如主动平仓，使用上面的代码
    # 通过以下，发现现象，贴近合约到期月份，不主动平仓，收益是增加的。这一条是否高可能性需要进一步确认。


# 交易
def TRADE(context):
    # fileter 节假日
    trade_days = get_trade_days(start_date=context.current_dt, end_date=context.current_dt + timedelta(days=1))
    if (context.current_dt + timedelta(days=1)) not in trade_days:
        return
    for future_code in g.future_list:
        symbol = re.search(r'^(\D+)', future_code).group(1)
        deal_long(context, future_code, symbol)
        # deal_short(context, future_code, symbol)


# 交易
def JIEJIARI(context):
    for future in context.portfolio.short_positions.keys():
        order_target_value(future, 0, side='short')
        g.porfolio_short_price[future] = 0
    for future in context.portfolio.long_positions.keys():
        order_target_value(future, 0, side='long')
        g.porfolio_long_price[future] = 0


# 交易逻辑
def deal_long(context, future_code, symbol):
    # 当月合约
    current_f = future_code

    # 最新价
    price_l = 0
    df = attribute_history(current_f, count=24 * 60, unit=g.freqBase)
    # arb_df = attribute_history(arb_future_code, count=24*60, unit=g.freqBase)
    price_l = df['close'][-1]

    # 成本价
    cost_price = 0
    # 查看多单仓位情况
    cur_long = 0
    if current_f in context.portfolio.long_positions.keys() and context.portfolio.long_positions[current_f].value > 0:
        cur_long = 1
        price_l = context.portfolio.long_positions[current_f].price
        #
        cost_price = g.porfolio_long_price[current_f]
        if cost_price == 0:
            log.error(current_f, cost_price, "long持仓价为0")
            g.porfolio_long_price[current_f] = price_l

    # 止盈or止损or加仓
    if cur_long > 0:
        #
        is_close_position = close_position(context, symbol, current_f)
        is_stopping_loss = False
        if is_close_position or is_stopping_loss:
            result = order_target_value(current_f, 0, side='long')
            if result is not None:
                g.porfolio_long_price[current_f] = 0
                # 盈利后此品种休息一段时间
                if is_close_position:
                    g.temp_removed_future_list.append(current_f)
                return

        # # 浮盈加仓
        # is_add_position = price_l < cost_price and open_position(context,symbol= symbol, current_f=current_f)
        # open_cash = context.portfolio.available_cash
        # more_amount = amount_available(context, open_cash, price_l, symbol)
        # if is_add_position and more_amount > 0:
        #     result = order(current_f, more_amount, side='long')
        #     if result is not None and result.filled > 0:
        #         g.porfolio_long_price[current_f] = result.price
        #         # log.info("long浮盈加仓",current_f,more_amount)
        #         return

    '''long开仓=============================================================
    '''
    if cur_long == 0:
        #
        # 开仓手数
        # 保证金=合约价格x交易单位x保证金比例
        # 开仓：限制轻每单10w
        # open_cash = 100000 if context.portfolio.available_cash < 500000 else context.portfolio.available_cash * 0.2
        open_cash = context.portfolio.available_cash
        amount = amount_available(context, open_cash, price_l, symbol)
        is_open_position = open_position(context, symbol=symbol, current_f=current_f)

        # 开仓
        if is_open_position and amount > 0:
            result = order_target(current_f, amount, side='long')
            if result is None:
                log.error('下单错误', current_f, price_now)
            else:
                g.porfolio_long_price[current_f] = price_l
                log.info("下单", symbol, context.current_dt)


# 收盘
def after_market_close(context):
    # log.info("总现金",context.portfolio.available_cash)
    for future_code in g.future_list:
        if future_code in (context.portfolio.long_positions.keys() and context.portfolio.short_positions.keys()):
            if context.portfolio.long_positions[future_code].value > 0 and context.portfolio.short_positions[
                future_code].value > 0:
                log.info("同时开了多空", future_code)
    return


'''
-------------------------- 风控--------------------------------------
'''


# 风控,每日执行
def stop_loss_monitor(context):
    for future_code in g.future_list:
        if future_code in context.portfolio.long_positions.keys() and context.portfolio.long_positions[
            future_code].value > 0:
            deal_stop_long_loss(context, future_code)
        if future_code in context.portfolio.short_positions.keys() and context.portfolio.short_positions[
            future_code].value > 0:
            deal_stop_short_loss(context, future_code)


def deal_stop_long_loss(context, future_code):
    # 查看多单仓位情况
    current_f = future_code
    price_now = context.portfolio.long_positions[current_f].price
    is_stopping_loss = price_now <= g.porfolio_long_price[current_f] * 0.995
    if is_stopping_loss:
        result = order_target_value(current_f, 0, side='long')
        if result != None:
            g.porfolio_long_price[current_f] = 0


def deal_stop_short_loss(context, future_code):
    # 查看空单仓位情况
    current_f = future_code
    price_now = context.portfolio.short_positions[current_f].price
    is_stopping_loss = price_now >= g.porfolio_short_price[current_f] * 1.005
    if is_stopping_loss:
        result = order_target_value(current_f, 0, side='short')
        if result != None:
            g.porfolio_short_price[current_f] = 0


'''
----------------------------------------------------------------
'''


##util 是否每周都是递增
def check_weekly_increase(weeks_data):
    for i in range(len(weeks_data)):
        if weeks_data['close'][i] - weeks_data['open'][i] <= 0:
            return False
    return True


## 是否每周都是振幅缩小
def check_weekly_decrease(weeks_data):
    for i in range(len(weeks_data)):
        if weeks_data['close'][i] - weeks_data['open'][i] >= 0:
            return False
    return True


## 是否每周都是振幅扩大
def is_all_week_scaling(weeks_data):
    for i in range(len(weeks_data) - 1):
        current_range = abs(weeks_data['close'][i] - weeks_data['open'][i])
        next_range = abs(weeks_data['close'][i + 1] - weeks_data['open'][i + 1])
        if current_range >= next_range:
            return False
    return True


# 是否过去了N周
def is_one_week_ago(current_date, target_date, weeks=1):
    one_week_ago = current_date - timedelta(weeks=weeks)
    if target_date <= one_week_ago:
        return True
    return False


'''
---------------仓位管理------------------------
'''


# 仓
def open_position(context, symbol, current_f):
    #
    if context.current_dt.hour == 9 and context.current_dt.minute <= 10:
        return False

    if context.current_dt.hour == 21 and context.current_dt.minute <= 10:
        return False
        # bandbool
    df = attribute_history(current_f, count=20, unit='1d')
    upper_band, middle_band, lower_band = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    # log.error(sigma)
    # sigma
    df_mins = attribute_history(current_f, count=1, unit='10m')
    df_1min = attribute_history(current_f, count=1, unit='1m')
    price = df_1min['close'][-1]
    # long 价格低的
    mean = g.mean_map[symbol]
    sigma = g.sigma_map[symbol]
    #
    #
    delta = df_mins['close'][-1] - df_mins['open'][-1]
    log.info(symbol, delta, int(2 * sigma))
    if (price < middle_band[-1] and delta > 2 * sigma):  # and   detla> sigma
        return True
    return False


def close_position(context, symbol, current_f):
    # 持仓
    # if context.current_dt.hour > 14 and context.current_dt.minute >50:
    #     return True
    # bandbool
    df = attribute_history(current_f, count=20, unit='1d')
    upper_band, middle_band, lower_band = talib.BBANDS(df['close'], timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)
    # log.error(sigma)
    # sigma
    df_1min = attribute_history(current_f, count=1, unit='1m')
    price = df_1min['close'][-1]
    # long 价格低的
    mean = g.mean_map[symbol]
    sigma = g.sigma_map[symbol]
    if price > middle_band[-1]:
        return True
    return False


# 计算能开多少手
def amount_available(context, open_cash, price_now, symbol):
    amount = 0
    open_cash = min(open_cash, context.portfolio.available_cash * 0.98)
    amount = math.floor(open_cash / (price_now * g.MarginUnit[symbol] * context.inc))
    return amount


