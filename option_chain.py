# 获取标的的期权链到期日期权标的列表
# https://open.longportapp.com/docs/quote/pull/optionchain-date-strike
# 运行前请访问“开发者中心”确保账户有正确的行情权限。
# 如没有开通行情权限，可以通过“LongPort”手机客户端，并进入“我的 - 我的行情 - 行情商城”购买开通行情权限。
from datetime import date
from longbridge.openapi import QuoteContext, Config

config = Config.from_env()
ctx = QuoteContext(config)

resp = ctx.option_chain_info_by_date("AAPL.US", date(2023, 8, 18))
print(resp)