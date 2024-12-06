from threading import Thread
from time import sleep
import requests
import pandas as pd


def _background_periodically_update_orders(order_controller):
    while True:
        sleep(order_controller.sampleInterval)
        df_orders = order_controller.summary()
        for index, order in df_orders.iterrows():
            order_controller.order_update_callback(order)

def generic_update_callback(order):
    
    ret = f"OrderId: {order.get('clOrdId')} - [{order.get('ordStatus')}] {order.get('side')} {order.get('cumQty')}/{order.get('qty')} {order.get('symbol')} @ {order.get('avgPx')}"
    if order.get('price') is not None:
        ret += f" with Px: {order.get('price')}"
    if order.get('stopPx') is not None:
        ret += f" and stopPx: {order.get('stopPx')}"
    if order.get('text') and order.get('text').replace('[B3]','').strip() != "":
        ret += f"\nWARNING: {order.get('text')}"
    
    print(f"Order update: {ret}\n")

class TradeAPIRequester:
    def __init__(self, token:str, host:str=None):

        if host is None:
            host = "https://localhost"
            print(f"WARNING: API host was not provided. Using default localhost host '{host}'")
        self.base_url = host + "/api/v1/order"
        self.base_url_v2 = host + "/api/v2/order"
        self.trade_url_v2 = host + "/api/v2/trade"
        self.headers = {
            "Authorization" : f"Bearer {token}"
        }

    # criar ordem
    def create_order(self, 
                     symbol:str, 
                     side:str,
                     qty:str, 
                     account:str, 
                     execBroker:str, 
                     ordType:str, 
                     timeInForce:str, 
                     isDMA:str, 
                     entity:str, 
                     price:str, 
                     stopPx:str,
                     memo:str=None, 
                     strategy:str=None, 
                     strategyParameter = None):

        body = {
            "symbol" : symbol,
            "side" : side,
            "qty" : qty,
            "account" : account,
            "execBroker" : execBroker,
            "ordType" : ordType,
            "timeInForce" : timeInForce,
            "isDMA" : isDMA,
            "entity" : entity,
            "memo": memo
        }

        if(strategy and strategyParameter):
            body["strategy"] = strategy
            body["strategyParameter"] = strategyParameter

        if price: body["price"] = price
        if stopPx: body["stopPx"] = stopPx

        r = requests.post(self.base_url, headers=self.headers, json=body)

        if r.status_code in [200, 202]:
            return r.json()
        else:
            return r.status_code

    # alterar ordem
    def update_order(self, id:str, ordType:str=None, qty:str=None, price:str=None, stopPx:str=None, timeInForce:str=None, strategy:str=None, strategyParameter = None):

        body = {
            "id": id,
            "ordType": ordType,
        }

        if qty: body["qty"] = qty
        if price: body["price"] = price
        if stopPx: body["stopPx"] = stopPx
        if timeInForce: body["timeInForce"] = timeInForce

        if(strategy and strategyParameter):
            body["strategy"] = strategy
            body["strategyParameter"] = strategyParameter

        r = requests.put(self.base_url, headers=self.headers, json=body)

        if r.status_code in [200, 202]:
            return r.json()
        else:
            return r.status_code

    # cancelar ordem por id
    def cancel_order(self, id:str):
        r = requests.delete(self.base_url + f"/{id}", headers=self.headers)

        if r.status_code in [200, 202]:
            return r.json()
        else:
            return r.status_code

    # cancelar todas as ordens
    def cancel_all_orders(self):
        r = requests.delete(self.base_url_v2 + "/myorders", headers=self.headers)

        if r.status_code not in [200, 202, 204]:
            print(f"{r.status_code} - {r.text}")

        if r.status_code == 204:
            return r.text
        return r.status_code

    # consultar todas as ordens
    def get_orders(self):
        r = requests.get(self.base_url_v2, headers=self.headers)

        if r.status_code in [200, 202]:            
            return r.json()
        else:
            return r.status_code

    # consultar ordem por ID
    def get_order(self, id:str):
        r = requests.get(f"{self.base_url_v2}/id/{id}", headers=self.headers)

        if r.status_code in [200, 202]:            
            return r.json()
        else:
            return r.status_code
    
    # consultar ordem por ID
    def get_ordersByParams(self, complete:bool = None, symbol:str=None, status:str=None, side:str=None, memo:str=None, parent:bool=None):
        resource:str = ""

        if complete != None:
            resource += f"&complete={complete}"
        if symbol != None:
            resource += f"&symbol={symbol}"
        if status != None:
            resource += f"&status={status}"
        if side != None:
            resource += f"&side={side}"
        if memo != None:
            resource += f"&memo={memo}"
        if parent != None:
            resource += f"&parent={parent}"
                
        r = requests.get(f"{self.base_url_v2}?{resource}", headers=self.headers)

        if r.status_code in [200, 202]:            
            return r.json()
        else:
            return r.status_code


    # consultar todas as ordens
    def get_trades(self):
        r = requests.get(self.trade_url_v2, headers=self.headers)
        
        if r.status_code in [200, 202]:            
            return r.json()
        else:
            return r.status_code
        
    

class OrderController:
    """
    Instantiate an order controller. Provide your token, account number, execution broker and entity to start sending orders.

    >>> from btgsolutions_tradeservices import OrderController

    >>> controller = OrderController(
    >>>     token="YOUR_TOKEN",
    >>>     account="YOUR_ACCOUNT_NUMBER",
    >>>     execBroker="YOUR_EXEC_BROKER",
    >>>     entity="YOUR_ENTITY",
    >>> )

    One can provide a custom order update callback function.

    >>> def order_update_callback(order):
    >>>     print(f"Order update: {order}")

    >>> controller = OrderController(
    >>>     token="YOUR_TOKEN",
    >>>     order_update_callback=order_update_callback,
    >>> )

    Parameters
    ----------------
    token: str
        User token.
        Field is required.
    order_api_host: str
        Order API host address. If not provided, default UAT host will be used.
        Field is not required.
    account: str
        Account.
        Field is not required.
    execBroker: str
        Execution broker.
        Field is not required.
    entity: str
        Associated entity.
        Field is not required.
    order_update_callback: Callable
        Order update callback function. If not provided, a generic callback function will be used.
        Field is not required.
    """
    def __init__(self, token:str, order_api_host:str=None, account:str=None, execBroker:str=None, entity:str=None, order_update_callback=None, sampleInterval = None):

        if order_update_callback is None:
            self.order_update_callback = generic_update_callback
        else:
            self.order_update_callback = order_update_callback
        
        self.token = token
        self.sampleInterval = sampleInterval

        self.account = account
        self.execBroker = execBroker
        self.entity = entity

        self.key_columns = ['clOrdId', 'symbol', 'side', 'qty', 'price', 'stopPx', 'ordStatus', 'text']

        self._t_api = TradeAPIRequester(token=token, host=order_api_host)

        if sampleInterval != None and sampleInterval > 0:
            self.daemon = Thread(target=_background_periodically_update_orders, args=(self,), daemon=True, name='order_updater')
            self.daemon.start()

    def create_order(self, 
                     symbol:str, 
                     side:str, 
                     qty:str, 
                     timeInForce:str, 
                     isDMA:str, 
                     price:str=None, 
                     stopPx:str=None, 
                     ordType:str=None, 
                     account:str=None, 
                     execBroker:str=None, 
                     entity:str=None, 
                     strategy:str=None, 
                     strategyParameter = None,
                     memo:str = None):
        """
        Create new order

        >>> orderId = controller.create_order(
        >>>     symbol="PETR4",
        >>>     side="S",
        >>>     qty="5000",
        >>>     price="20.41",
        >>>     timeInForce="Day",
        >>>     isDMA="true"
        >>> )

        Parameters
        ----------------
        symbol: str
            Ticker symbol.
            Field is required.
        side: str
            Side of transaction.
            Allowed values: 'B', 'S'.
            Field is required.
        qty: str
            Number of units to transact.
            Field is required.
        timeInForce: str
            New order time in force (if applicable).
            Field is required.
        isDMA: str
            is DMA.
            Field is required.
        price: str
            New order price (if applicable).
            Field is not required.
        stopPx: str
            New order stop price (if applicable).
            Field is not required.
        ordType: str
            Order type.
            Field is required.
        account: str
            Account.
            Field is not required if it has already been provided at class instantiation.
        execBroker: str
            Execution broker.
            Field is not required if it has already been provided at class instantiation.
        entity: str
            Associated entity.
            Field is not required if it has already been provided at class instantiation.
        strategy: str
            Strategy name.
            Field is not required.
        strategyParameter: str
            Dictionary with paramerts.
            Field is not required.
        memo: str
            Memo and subaccount
            Field is not required              
        """
        if symbol is None:
            print("error: symbol is None")
            return 400
        if side is None:
            print("error: side is None")
            return 400
        if qty is None:
            print("error: qty is None")
            return 400
        if timeInForce is None:
            print("error: timeInForce is None")
            return 400
        if ordType is None:
            print("error: ordType is None")
            return 400

        if account is None: account = self.account
        if execBroker is None: execBroker = self.execBroker 
        if entity is None: entity = self.entity
        
        return self._t_api.create_order( 
            symbol=symbol,
            side=side,
            qty=qty,
            account=account,
            execBroker=execBroker,
            ordType=ordType,
            timeInForce=timeInForce,
            isDMA=isDMA,
            entity=entity,
            price=price,
            stopPx=stopPx,
            strategy=strategy,
            strategyParameter=strategyParameter,
            memo=memo
        )
    
    def change_order(self, id:str, qty:str, timeInForce:str, ordType:str, price:str=None, stopPx:str=None, strategy:str=None, strategyParameter = None):
        """
        Change an order

        >>> orderId = controller.create_order(
        >>>     id="YOUR_ORDER_ID",
        >>>     qty="5000",
        >>>     price="20.43",
        >>>     timeInForce="Day",
        >>>     ordType="Limit"
        >>> )

        Parameters
        ----------------
        id: str
            Order id.
            Field is required.
        qty: str
            New order quantity (if applicable).
            Field is required.
        price: str
            New order price (if applicable).
            Field is not required.
        timeInForce: str
            New order time in force (if applicable).
            Field is required.
        ordType: str
            Order type.
            Field is required.
        stopPx: str
            New order stop price (if applicable).
            Field is not required.
        strategy: str
            Strategy name.
            Field is not required.
        strategyParameter: str
            Dictionary with paramerts.
            Field is not required.            
        """
        if id is None:
            print("error: Id is None")
            return 400
        if qty is None:
            print("error: qty is None")
            return 400
        if timeInForce is None:
            print("error: timeInForce is None")
            return 400
        if ordType is None:
            print("error: ordType is None")
            return 400
        if price is None and ordType == 'Limit':
            print("error: price is None")
            return 400
        
        if ':' in id:
            id = id.split(':')[0]   
        return self._t_api.update_order(
            id=id,
            ordType=ordType,
            qty=qty,
            price=price,
            stopPx=stopPx,
            timeInForce=timeInForce,
            strategy=strategy,
            strategyParameter=strategyParameter
        )
    
    def cancel_order(self, id:str):
        """
        Cancel an order

        >>> orderId = controller.cancel_order(
        >>>     id="YOUR_ORDER_ID",
        >>> )

        Parameters
        ----------------
        id: str
            Order id.
            Field is required.
        """
        if id is None:
            print("error: Id is None")
            return
        if ':' in id:
            id = id.split(':')[0]   
        return self._t_api.cancel_order(id)

    def cancel_all_orders(self,):
        """
        Cancel all orders

        >>> controller.cancel_all_orders()
        """
        return self._t_api.cancel_all_orders()

    def get_order(self, id:str):
        """
        Retrieve an order status

        >>> orderStatus = controller.get_order(
        >>>     id="YOUR_ORDER_ID",
        >>> )

        Parameters
        ----------------
        id: str
            Order id.
            Field is required.
        """
        if id is None:
            print("error: Id is None")
            return

        if ':' in id:
            id = id.split(':')[0]        
        return self._t_api.get_order(id)
    
    
 
    def get_ordersByParams(self, complete:bool = None, symbol:str=None, status:str=None, side:str=None, memo:str=None, parent:bool = None):
        """
        Retrieve an order status

        >>> orderStatus = controller.get_order(
        >>>     id="YOUR_ORDER_ID",
        >>> )

        Parameters
        ----------------
            complete
            symbol
            status
            side
            memo
            parent
        """
        return self._t_api.get_ordersByParams(complete, symbol, status, side, memo, parent)



    def get_orders(self):
        """
        Retrieve all order status

        >>> controller.get_orders()
        """
        return self._t_api.get_orders()
    
    def summary(self, detailed:bool=True):
        """
        Get a summary of all order status, in a Pandas DataFrame format.

        >>> summary = controller.summary()

        Parameters
        ----------------
        detailed: str
            If 'True', returns all status info about an order. If 'False', returns a summarized version.
            Field is not required.
        """
        res = self.get_orders()
        df = pd.DataFrame(res)
        
        if detailed is True:
            return df
        return df[df.columns[df.columns.isin(self.key_columns)]]

    def get_trades(self):
        """
        Retrieve all trades

        >>> controller.get_trades()
        """
        return self._t_api.get_trades()
