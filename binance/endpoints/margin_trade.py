from abc import ABCMeta, abstractmethod
from typing import Union
from binance.exceptions import MarginTradingError
from binance.utils import format_time, interval_to_ms

class MarginAccountEndpoints(metaclass = ABCMeta):
    @property
    @abstractmethod
    def request_handler(self):
        pass

    @property
    @abstractmethod
    def API_VERSION(self):
        pass

    @property
    @abstractmethod
    def ORDER_SIDE(self):
        pass
    
    @property
    @abstractmethod
    def ORDER_TYPE(self):
        pass
    
    @abstractmethod
    def _create_margin_api_uri(self, path: str) -> str:
        pass

    def cross_margin_transfer(self,
                              asset: str,
                              amount: float,
                              type: int,
                              recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        if(params['type'] not in [1,2]):
            raise MarginTradingError(
                "Cross Margin transfer called with a type not in [1,2]")
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/transfer')
        return self.request_handler.post(uri, signed=True, **params)
        
    def margin_to_spot_transfer(self,
                                asset: str,
                                amount: float,
                                recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['type'] = 2
        return self.cross_margin_transfer(**params)

    def spot_to_margin_transfer(self,
                                asset: str,
                                amount: float,
                                recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['type'] = 1
        return self.cross_margin_transfer(**params)

    def margin_account_borrow(self,
                              asset: str,
                              amount: float,
                              isIsolated: bool = False,
                              symbol: str = None,
                              recvWindow: int = None):
        
        if(isIsolated == True) and (symbol == None):
            raise ValueError("isIsolated is true but symbol not specified")
        params = locals()
        del params['self']
        if(params['isIsolated']) and (params['symbol'] is None):
            raise MarginTradingError(
                "symbol parameter not passed for Isolated margin borrow request")
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/loan')
        return self.request_handler.post(uri, signed=True, **params)

    def margin_account_repay(self,
                             asset: str,
                             amount: float,
                             isIsolated: bool = False,
                             symbol: str = None,
                             recvWindow: int = None):
        
        if(isIsolated == True) and (symbol == None):
            raise ValueError("isIsolated is true but symbol not specified")
        params = locals()
        del params['self']
        if(params['isIsolated']) and (params['symbol'] is None):
            raise MarginTradingError(
                "symbol parameter not passed for Isolated margin repay request")
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/repay')
        return self.request_handler.post(uri, signed=True, **params)

    def query_margin_asset(self,
                           asset: str):
        params['asset'] = asset 
        uri = self._create_margin_api_uri('margin/asset')
        return self.request_handler.get(uri, signed=False, **params)

    def query_cross_margin_pair(self,
                                symbol: str):
        params['symbol'] = symbol 
        uri = self._create_margin_api_uri('margin/pair')
        return self.request_handler.get(uri, signed=False, **params)

    def get_all_margin_assets(self):
        uri = self._create_margin_api_uri('margin/allAssets')
        return self.request_handler.get(uri, signed=False)

    def get_all_cross_margin_pairs(self):
        uri = self._create_margin_api_uri('margin/allPairs')
        return self.request_handler.get(uri, signed=False)

    def query_cross_margin_price_index(self,
                                       symbol: str):
        params['symbol'] = symbol
        uri = self._create_margin_api_uri('margin/priceIndex')
        return self.request_handler.get(uri, signed=False, **params)

    def create_margin_order(self,
                            symbol: str,
                            side: str,
                            type: str,
                            isIsolated: bool = False,
                            timeInForce: str = None,
                            quantity: float = None,
                            quoteOrderQty: float = None,
                            price: float = None,
                            newClientOrderId: str = None,
                            stopPrice: float = None,
                            icebergQty: float = None,
                            newOrderRespType: str = None,
                            sideEffectType: str = None,
                            recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/order')
        return self.request_handler.post(uri, signed=True, **params)

    def margin_limit_buy_order(self,
                               symbol: str,
                               isIsolated: bool = False,
                               timeInForce: str = None,
                               quantity: float = None,
                               quoteOrderQty: float = None,
                               price: float = None,
                               newClientOrderId: str = None,
                               icebergQty: float = None,
                               newOrderRespType: str = None,
                               sideEffectType: str = None,
                               recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.LIMIT
        return self.create_margin_order(**params)

    def margin_limit_sell_order(self,
                                symbol: str,
                                isIsolated: bool = False,
                                timeInForce: str = None,
                                quantity: float = None,
                                quoteOrderQty: float = None,
                                price: float = None,
                                newClientOrderId: str = None,
                                icebergQty: float = None,
                                newOrderRespType: str = None,
                                sideEffectType: str = None,
                                recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.LIMIT
        return self.create_margin_order(**params)

    def margin_market_buy_order(self,
                                symbol: str,
                                isIsolated: bool = False,
                                timeInForce: str = None,
                                quantity: float = None,
                                quoteOrderQty: float = None,
                                newClientOrderId: str = None,
                                newOrderRespType: str = None,
                                sideEffectType: str = None,
                                recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.MARKET
        return self.create_margin_order(**params)

    def margin_market_sell_order(self,
                                 symbol: str,
                                 isIsolated: bool = False,
                                 timeInForce: str = None,
                                 quantity: float = None,
                                 quoteOrderQty: float = None,
                                 newClientOrderId: str = None,
                                 newOrderRespType: str = None,
                                 sideEffectType: str = None,
                                 recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.MARKET
        return self.create_margin_order(**params)
    
    def margin_limit_stoploss_buy_order(self,
                                        symbol: str,
                                        stopPrice: float,
                                        isIsolated: bool = False,
                                        timeInForce: str = None,
                                        quantity: float = None,
                                        quoteOrderQty: float = None,
                                        price: float = None,
                                        newClientOrderId: str = None,
                                        icebergQty: float = None,
                                        newOrderRespType: str = None,
                                        sideEffectType: str = None,
                                        recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.STOP_LOSS_LIMIT
        return self.create_margin_order(**params)

    def margin_limit_stoploss_sell_order(self,
                                         symbol: str,
                                         stopPrice: float,
                                         isIsolated: bool = False,
                                         timeInForce: str = None,
                                         quantity: float = None,
                                         quoteOrderQty: float = None,
                                         price: float = None,
                                         newClientOrderId: str = None,
                                         icebergQty: float = None,
                                         newOrderRespType: str = None,
                                         sideEffectType: str = None,
                                         recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.STOP_LOSS_LIMIT
        return self.create_margin_order(**params)

    def margin_stoploss_buy_order(self,
                                  symbol: str,
                                  stopPrice: float,
                                  isIsolated: bool = False,
                                  timeInForce: str = None,
                                  quantity: float = None,
                                  quoteOrderQty: float = None,
                                  price: float = None,
                                  newClientOrderId: str = None,
                                  newOrderRespType: str = None,
                                  sideEffectType: str = None,
                                  recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.STOP_LOSS
        return self.create_margin_order(**params)

    def margin_stoploss_sell_order(self,
                                   symbol: str,
                                   stopPrice: float,
                                   isIsolated: bool = False,
                                   timeInForce: str = None,
                                   quantity: float = None,
                                   quoteOrderQty: float = None,
                                   price: float = None,
                                   newClientOrderId: str = None,
                                   newOrderRespType: str = None,
                                   sideEffectType: str = None,
                                   recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.STOP_LOSS
        return self.create_margin_order(**params)

    def margin_takeprofit_buy_order(self,
                                    symbol: str,
                                    stopPrice: float,
                                    isIsolated: bool = False,
                                    timeInForce: str = None,
                                    quantity: float = None,
                                    quoteOrderQty: float = None,
                                    price: float = None,
                                    newClientOrderId: str = None,
                                    newOrderRespType: str = None,
                                    sideEffectType: str = None,
                                    recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.TAKE_PROFIT
        return self.create_margin_order(**params)

    def margin_takeprofit_sell_order(self,
                                     symbol: str,
                                     stopPrice: float,
                                     isIsolated: bool = False,
                                     timeInForce: str = None,
                                     quantity: float = None,
                                     quoteOrderQty: float = None,
                                     price: float = None,
                                     newClientOrderId: str = None,
                                     newOrderRespType: str = None,
                                     sideEffectType: str = None,
                                     recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.SELL
        params['type'] = self.ORDER_TYPE.TAKE_PROFIT
        return self.create_margin_order(**params)
    
    def margin_takeprofit_limit_buy_order(self,
                                          symbol: str,
                                          stopPrice: float,
                                          isIsolated: bool = False,
                                          timeInForce: str = None,
                                          quantity: float = None,
                                          quoteOrderQty: float = None,
                                          price: float = None,
                                          icebergQty: float = None,
                                          newClientOrderId: str = None,
                                          newOrderRespType: str = None,
                                          sideEffectType: str = None,
                                          recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.TAKE_PROFIT_LIMIT
        return self.create_margin_order(**params)

    def margin_takeprofit_limit_buy_order(self,
                                          symbol: str,
                                          stopPrice: float,
                                          isIsolated: bool = False,
                                          timeInForce: str = None,
                                          quantity: float = None,
                                          quoteOrderQty: float = None,
                                          price: float = None,
                                          icebergQty: float = None,
                                          newClientOrderId: str = None,
                                          newOrderRespType: str = None,
                                          sideEffectType: str = None,
                                          recvWindow: int = None) -> dict:
        params = locals()
        del params['self']
        params['side'] = self.ORDER_SIDE.BUY
        params['type'] = self.ORDER_TYPE.TAKE_PROFIT_LIMIT
        return self.create_margin_order(**params)
        
    def cancel_margin_order(self,
                            symbol: str,
                            isIsolated: bool = False,
                            orderId:int = None,
                            origClientOrderId: str = None,
                            newClientOrderId: str = None,                            
                            recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/order')
        return self.request_handler.delete(uri, signed=True, **params)

    def cancel_all_margin_order(self,
                                symbol: str,
                                isIsolated: bool = False,
                                orderId:int = None,
                                origClientOrderId: str = None,
                                newClientOrderId: str = None,                            
                                recvWindow: int = None) -> dict:

        params = locals()
        del params['self']
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/openOrders')
        return self.request_handler.delete(uri, signed=True, **params)

    
    def get_cross_margin_transfer_history(self,
                                          asset: str = None,
                                          type: str = None,
                                          startTime: int = None,
                                          endTime: int = None,
                                          current: int = 1,
                                          size: int = 10,
                                          archived: bool = False,
                                          recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/transfer')
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_loan_record(self,
                                 asset: str,
                                 isolatedSymbol: str = None,
                                 txId: int = None,
                                 startTime: int = None,
                                 endTime: int = None,
                                 current: int = 1,
                                 size: int = 10,
                                 archived: bool = False,
                                 recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/loan',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_repay_record(self,
                                  asset: str,
                                  isolatedSymbol: str = None,
                                  txId: int = None,
                                  startTime: int = None,
                                  endTime: int = None,
                                  current: int = 1,
                                  size: int = 10,
                                  archived: bool = False,
                                  recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/repay',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def get_margin_interest_history(self,
                                    asset: str,
                                    isolatedSymbol: str = None,
                                    txId: int = None,
                                    startTime: int = None,
                                    endTime: int = None,
                                    current: int = 1,
                                    size: int = 10,
                                    archived: bool = False,
                                    recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/interestHistory',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def get_margin_force_liquidation_record(self,
                                            isolatedSymbol: str = None,
                                            txId: int = None,
                                            startTime: int = None,
                                            endTime: int = None,
                                            current: int = 1,
                                            size: int = 10,
                                            recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/forceLiquidationRec',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_cross_margin_account_details(self,
                                            recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        uri = self._create_margin_api_uri('margin/account',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_account_order(self,
                                   symbol: str,
                                   isIsolated: bool = False,
                                   orderId: str = None,
                                   orderClientOrderId: str = None,
                                   recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/order',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_account_open_orders(self,
                                         symbol: str = None,
                                         isIsolated: bool = False,
                                         recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/openOrders',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)

    def query_margin_account_order(self,
                                   symbol: str,
                                   isIsolated: bool = False,
                                   orderId: str = None,
                                   startTime: int = None,
                                   endTime: int = None,
                                   limit: int = 500,
                                   recvWindow: int = None):
        params = locals()
        del params['self']
        params = {k: v for k, v in params.items() if v is not None}
        params['isIsolated'] = 'TRUE' if (params['isIsolated'] == True) else 'FALSE'
        uri = self._create_margin_api_uri('margin/allOrders',
                                          version=self.PRIVATE_API_VERSION)
        return self.request_handler.get(uri, signed=True, **params)
    
if __name__ == '__main__':
    pass
