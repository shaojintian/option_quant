# 15天tqqq卖put
from datetime import date
from longbridge.openapi import TradeContext, Config,QuoteContext

config = Config.from_env()
ctx = QuoteContext(config)
account = TradeContext(config)
###################
SYMBOL = ["TQQQ.US","SOXL.US","SPXL.US"]
EXPIRY = date(2023,8,15)
STRIKE = 400
OPTION_TYPE = "PUT"
ORDER_TYPE = "LMT"

PUTS_WAITED_TO_SELL = []

# # 查询账户余额
# resp = account.account_balance()
# print(resp)

#
resp = ctx.trades(SYMBOL[0], 1)
print(resp)

resp = ctx.option_chain_info_by_date(SYMBOL[0],date(2023, 8, 18))
print(resp)


# # 查询期权信息
# resp = ctx.option_quote(PUTS_WAITED_TO_SELL)
# print(resp)
