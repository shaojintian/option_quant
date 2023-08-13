

from ast import Slice


def Initialize(self) -> None:
    self.SetStartDate(2017, 4, 1)
    self.SetEndDate(2017, 4, 30)
    self.SetCash(100000)
        
    option = self.AddOption("GOOG")
    self.symbol = option.Symbol
    option.SetFilter(-5, 5, 0, 30)


def OnData(self, slice: Slice) -> None:
    if self.Portfolio.Invested:
        return

    chain = slice.OptionChains.get(self.symbol)
    if not chain:
        return

    # Find options with the farthest expiry
    expiry = max([x.Expiry for x in chain])
    contracts = [contract for contract in chain if contract.Expiry == expiry]
     
    # Order the OTM calls by strike to find the nearest to ATM
    call_contracts = sorted([contract for contract in contracts
        if contract.Right == OptionRight.Call and
            contract.Strike > chain.Underlying.Price],
        key=lambda x: x.Strike)
    if not call_contracts:
        return
        
    # Order the OTM puts by strike to find the nearest to ATM
    put_contracts = sorted([contract for contract in contracts
        if contract.Right == OptionRight.Put and
           contract.Strike < chain.Underlying.Price]
        key=lambda x: x.Strike, reverse=True)
    if not put_contracts:
        return

    call_strike = call_contracts[0].Strike
    put_strike = put_contracts[0].Strike


long_strangle = OptionStrategies.Strangle(self.symbol, call_strike, put_strike, expiry)
self.Buy(long_strangle, 1)
