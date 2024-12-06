
import requests
import json
import sys
sys.path.append("/src/python/btgsolutions_tradeservices/rest")
from order_controller import OrderController


def Start():
    
    #######################
    ##                   ##
    ## INTERNAL USE ONLY ##
    ##                   ##
    #######################

    print("init")    
    
    url = 'https://api-internal.uat.btgpactualsolutions.com/api/Token/RequestTokenExtranet'
    body = { "Username": "jose-g.nascimento@btgpactual.com", "ClientSecret": "nkGjhQoTinErk1QpSMGc"}
    x = requests.post(url, json = body)
   
    Token = json.loads(x.text)['tokenCode']
    controller = OrderController(token=Token, 
                                 order_api_host = "https://api.uat.btgpactualsolutions.com")


    x = controller.get_ordersByParams(symbol='DI1F25', status='Filled')
    print(x)
    # response = controller.get_orders()
    # print(response)

    # msg = controller.create_order(symbol="PETR4", side="S", qty="100", ordType="Limit", price="38.40", timeInForce="Day", isDMA="true")
    # ClOrdId = msg['message']
    # print(ClOrdId)
    # response = controller.get_order(id = ClOrdId)
    # if response is not None:
    #     response = {'orderId': response[0]['clOrdId'], 'status': response[0]['ordStatus'], 'Qty' : response[0]['qty'], 'filledQty': response[0]['cumQty'], 'avgPx' : response[0]['avgPx'] }
    # else:
    #     response = False
    # print(response)

    # strategyParameter = { 
    # "max-floor": "100",    
    # "start-time": "20240614-19:00:00",
    # "end-time": "20240614-20:00:00"
    # }

    # print("new order single")
    # orderId = controller.create_order(symbol="PETR4", side="S", qty="100", ordType="Limit", price="38.40", timeInForce="Day", isDMA="true")
    # controller.change_order(id=orderId['message'], qty="200", price="38", timeInForce="Day", ordType="Limit")



    # print(orderId['message'])


    # print("new order single")
    # orderId = controller.create_order(symbol="PETR4", 
    #                                   side="S", 
    #                                   qty="100", 
    #                                   ordType="Limit", 
    #                                   price="38.40", 
    #                                   timeInForce="Day", 
    #                                   isDMA="true",
    #                                   account="99999", 
    #                                   execBroker="85", 
    #                                   entity="CLIENT_UAT")
    # print(orderId['message'])


    # print("new order single strategy")
    # orderId = controller.create_order(symbol="PETR4", 
    #                                   side="S", 
    #                                   qty="100", 
    #                                   ordType="Limit", 
    #                                   price="38.40", 
    #                                   timeInForce="Day", 
    #                                   isDMA="true", 
    #                                   strategy = "twap", 
    #                                   strategyParameter = strategyParameter)
    

    # print("get order")
    # print(controller.get_order(str(orderId['message'])))
    
    # print("get_orders")
    # print(controller.get_orders())

    # print("cancel_all_orders")
    # print(controller.cancel_all_orders())
    
    # print("end")
Start()