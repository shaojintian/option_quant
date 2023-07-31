# 14天关注股票列表，卖put
import schedule
import time
from datetime import date, timedelta
from longbridge.openapi import TradeContext, Config,QuoteContext

config = Config.from_env()
ctx = QuoteContext(config)
account = TradeContext(config)
###################
SYMBOL = []

PUTS_WAITED_TO_SELL = []


# # 查询账户余额
# resp = account.account_balance()
# print(resp)

def my_task():
    RESULT = []
    EXPIRY = find_next_friday(date.today())
    #
    # 在这里写你要执行的任务
    print("定时任务执行中...")
    resp = ctx.watch_list()
    if resp:
        # 遍历每个WatchListGroup
        for watch_list_group in resp:
            # 遍历每个WatchListSecurity
            for security in watch_list_group.securities:
                # 获取symbol并添加到列表中
                symbol = security.symbol
                SYMBOL.append(symbol)

    for i in range(len(SYMBOL)):
        #
        resp = ctx.intraday(SYMBOL[i])
        if not resp:
            continue
        price_now = int(resp[0].price)
        # 找期权链
        resp_options = ctx.option_chain_info_by_date(SYMBOL[i],EXPIRY)
        if not resp_options:
            continue
        for option in resp_options:
            if option.price == price_now:
                PUTS_WAITED_TO_SELL.append(option.put_symbol)

        #print(len(PUTS_WAITED_TO_SELL))
        # 查询期权信息
        resp = ctx.option_quote(PUTS_WAITED_TO_SELL)
        if not resp:
            continue
        for option in resp:
            if (option.high -  option.low)/option.low > 0.6:
                RESULT.append(option.symbol)

    RESULT = list(set(RESULT))
    print(RESULT)


def find_next_friday(start_date):
    # 计算距离当前日期两周后的日期
    two_weeks_later = start_date + timedelta(weeks=2)

    # 找到该日期最近的周五
    while two_weeks_later.weekday() != 4:  # 周五的weekday()为4
        two_weeks_later += timedelta(days=1)

    return two_weeks_later

if __name__ == '__main__':
    my_task()
    # 每天的特定时间执行任务（这里设定为每天的9点执行）
    schedule.every().day.at("22:30").do(my_task)

    while True:
        schedule.run_pending()
        time.sleep(1)