# 120天关注股票列表，卖put
# 二周调仓一次
import json

import itchat
import schedule
import time
from datetime import date, timedelta
from longbridge.openapi import TradeContext, Config, QuoteContext
from send_wx_msg import send_wechat_message

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
        resp_options = ctx.option_chain_info_by_date(SYMBOL[i], EXPIRY)
        if not resp_options:
            continue
        for option in resp_options:
            if option.price == price_now:
                PUTS_WAITED_TO_SELL.append(option.put_symbol)

        # print(len(PUTS_WAITED_TO_SELL))
        # 查询期权信息
        resp = ctx.option_quote(PUTS_WAITED_TO_SELL)
        if not resp:
            continue
        for option in resp:
            if option.low == 0:
                continue
            if (option.high - option.low) / option.low > 0.5:
                RESULT.append(option.symbol)

    RESULT = list(set(RESULT))
    result_json = str(date.today()) + "," + json.dumps(RESULT)
    print(result_json)
    # try:
    #     send_wechat_message(friend_name="filehelper", message=result_json)
    # except:
    #     pass


def find_next_friday(start_date):
    # 计算距离当前日期1.5月后的日期
    two_weeks_later = start_date + timedelta(weeks=int(4*1.5))

    # 找到该日期最近的周五
    while two_weeks_later.weekday() != 4:  # 周五的weekday()为4
        two_weeks_later += timedelta(days=1)

    return two_weeks_later


if __name__ == '__main__':
    # # 登录微信个人号
    # itchat.auto_login(enableCmdQR=False)
    #
    my_task()
    # 每天的特定时间执行任务（这里设定为每天的9点执行）
    schedule.every().day.at("22:30").do(my_task)

    while True:
        schedule.run_pending()
        time.sleep(1)
