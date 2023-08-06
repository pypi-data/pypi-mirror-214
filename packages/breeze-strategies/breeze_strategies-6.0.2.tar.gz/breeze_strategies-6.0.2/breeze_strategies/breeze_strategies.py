import threading
import queue
import time 
#import datetime
import sys
import asyncio
import nest_asyncio
from breeze_connect import BreezeConnect
from datetime import datetime

#nest_asyncio.apply()

class Strategies:
    
    #initialize strategy object
    def __init__(self,app_key,secret_key,api_session,max_profit,max_loss):
        
        self.maxloss = int(max_loss)
        self.maxprofit = int(max_profit)
        self.currentcall = 0
        self.currentput = 0
        self.flag = False
        self.client = BreezeConnect(app_key)
        self.client.generate_session(secret_key,api_session)
        self.client.ws_connect()
        self.quantity = 0
        self.exchange_code = ""
        self.stock_code = ""
        self.product_type = ""
        self.expiry_date = ""
        self.strike_price = ""
        self.order_type = ""
        self.validity = ""
        self.stoploss = ""
        self.validity_date = ""
    
    def squareoff(self,exchange_code, stock_code, product_type, expiry_date, strike_price, action, order_type, validity, stoploss, quantity, price,validity_date, trade_password, disclosed_quantity,right):
        data = self.client.square_off(exchange_code=exchange_code,
                            product="options",
                            stock_code=stock_code,
                            expiry_date=expiry_date,
                            right=right,
                            strike_price=strike_price,
                            action=action,
                            order_type=order_type,
                            validity=validity,
                            stoploss="0",
                            quantity=quantity,
                            price=price,
                            validity_date=validity_date,
                            trade_password="",
                            disclosed_quantity="0")
        
        print(f"square off status of {right} is",data)
        
    def get_date_format(self,expiry_date):
        month_names = {
                            '01': 'Jan',
                            '02': 'Feb',
                            '03': 'Mar',
                            '04': 'Apr',
                            '05': 'May',
                            '06': 'Jun',
                            '07': 'Jul',
                            '08': 'Aug',
                            '09': 'Sep',
                            '10': 'Oct',
                            '11': 'Nov',
                            '12': 'Dec'
                      }
        year = expiry_date[:4]
        month = expiry_date[5:7]
        day = expiry_date[8:10]
        formatted_date = f"{day}-{month_names[month]}-{year}"
        return(formatted_date)
        
    def trigger(self,product_type, rightval, stock_code, strike_price, quantity, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, call_execution,put_execution):
        net_gain_loss = (self.currentcall + self.currentput)*int(quantity)
        print(f"net gain/loss  : {round(net_gain_loss,2)}/- Rs")
        print("-------------------------------------------------------------------")
        formatted_date = self.get_date_format(expiry_date)

        if(net_gain_loss > 0 and net_gain_loss >= self.maxprofit):
            print("maxprofit has reached...")
            print("SquareOff operation on both contracts call and put begins....")
            
            self.squareoff(exchange_code, stock_code, product_type, expiry_date, strike_price, order_type, validity, stoploss, quantity, validity_date, "", disclosed_quantity="0",right = "Call",action = "sell", price = "")
            self.squareoff(exchange_code, stock_code, product_type, expiry_date, strike_price , order_type, validity, stoploss, quantity, validity_date, "", disclosed_quantity="0",right = "Put", action = "sell", price = "")
            
            self.client.unsubscribe_feeds(exchange_code=exchange_code, stock_code=stock_code, product_type="options", expiry_date= formatted_date, strike_price=strike_price, right="Call", get_exchange_quotes=True, get_market_depth=False)
            self.client.unsubscribe_feeds(exchange_code=exchange_code, stock_code=stock_code, product_type="options", expiry_date= formatted_date, strike_price=strike_price, right="Put", get_exchange_quotes=True, get_market_depth=False)
            print("-------------END------------------")
            self.flag = True
            return
        if(net_gain_loss < 0 and net_gain_loss <= self.maxloss):
            print("maxloss has reached...")
            print("SquareOff operation on both contracts call and put begins....")
            self.squareoff(exchange_code, stock_code, product_type, expiry_date, strike_price, order_type, validity, stoploss, quantity, validity_date, "", disclosed_quantity="0",right = "Call",action = "sell",price = "")
            self.squareoff(exchange_code, stock_code, product_type, expiry_date, strike_price, order_type, validity, stoploss, quantity, validity_date, "", disclosed_quantity="0",right = "Put",action = "sell",price = "")

            self.client.unsubscribe_feeds(exchange_code=exchange_code, stock_code=stock_code, product_type="options", expiry_date= formatted_date, strike_price=strike_price, right="Call", get_exchange_quotes=True, get_market_depth=False)
            self.client.unsubscribe_feeds(exchange_code=exchange_code, stock_code=stock_code, product_type="options", expiry_date= formatted_date, strike_price=strike_price, right="Put", get_exchange_quotes=True, get_market_depth=False)
            print("---------------END-----------------")
            self.flag = True
            return

    def calculate_current(self,product_type,stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,call_execution,put_execution,flag):
        
        resultcall = []
        formatted_date = self.get_date_format(expiry_date)
        
        def on_ticks(data):
            
            value = data
            
            if(value['right'] == "Call"):
                self.currentcall = round(float(value['last']) - float(call_execution), 2)
                print(f"P & L (CALL)  : {self.currentcall * int(self.quantity)}/- Rs")
                print("-------------------------------------------------------------------")
                if(self.flag == False):
                    self.trigger(product_type, "Call", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,call_execution,put_execution)
            
            if(value['right'] == "Put"):
                self.currentput = round(float(value['last']) - float(put_execution), 2)
                print(f"P & L (PUT) :  {self.currentput * int(self.quantity)}/- Rs")
                print("-------------------------------------------------------------------")
                if(self.flag == False):
                    self.trigger(product_type, "Put", stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price,put_price,call_execution,put_execution)
            
        self.client.on_ticks = on_ticks
        self.client.subscribe_feeds(exchange_code = exchange_code, stock_code = stock_code, product_type = product_type, expiry_date= formatted_date, strike_price=strike_price, right = "Call", get_exchange_quotes=True, get_market_depth=False)
        self.client.subscribe_feeds(exchange_code = exchange_code, stock_code = stock_code, product_type = product_type, expiry_date= formatted_date, strike_price=strike_price, right = "Put", get_exchange_quotes=True, get_market_depth=False) 

        
    def profit_and_loss(self,product_type, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, orderids,call_execution,put_execution):
        self.calculate_current(product_type, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, call_execution, put_execution,False)
            
    def long_straddle(self, stock_code, strike_price, qty, expiry_date, stoploss = "", put_price = "0", call_price = "0",product_type = "options", order_type = "market", validity = "day", validity_date = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ'), exchange_code = "NFO"):
        
        self.quantity = qty
        self.exchange_code = exchange_code 
        self.stock_code = stock_code
        self.product_type = product_type 
        self.expiry_date = expiry_date  
        self.strike_price = strike_price
        self.order_type = order_type
        self.validity = validity
        self.stoploss = stoploss
        #self.quantity = quantity
        self.validity_date = validity_date

        def place_order_method(stock_code,exchange_code,product,action,order_type,stoploss,quantity,price,validity,validity_date,expiry_date,right,strike_price,res_queue):
         
            data =  self.client.place_order(stock_code=stock_code,
                    exchange_code=exchange_code,
                    product="options",
                    action = "buy",
                    order_type=order_type,
                    stoploss=stoploss,
                    quantity=qty,
                    price = price,
                    validity= validity,
                    validity_date = validity_date,
                    disclosed_quantity = "0",
                    expiry_date = expiry_date,
                    right= right,
                    strike_price=strike_price)
            print(data)
            res_queue.put(data)
            return(data)
                  
        res_queue = queue.Queue()
        #create thread for call and put order to execute simultaneously for buy type
        t1 = threading.Thread(target = place_order_method,args = (stock_code,exchange_code,"options","buy",order_type,stoploss,qty,call_price,validity,validity_date,expiry_date,"Call",strike_price,res_queue))
        t1.start()
        t1.join()
        
        firstresponse = res_queue.get()
        
        res_queue = queue.Queue()
        t2 = threading.Thread(target = place_order_method,args = (stock_code,exchange_code,"options","buy",order_type,stoploss,qty,put_price,validity,validity_date,expiry_date,"Put",strike_price,res_queue))
        t2.start()
        t2.join()
        secondresponse = res_queue.get()
        
        
        #if one of the order fails then cancel the other one which is successfull
        if(firstresponse.get('Success',None)!=None and secondresponse.get('Success',None)==None):
            print("Put Order Failed....")
            order_id = firstresponse['Success']['order_id']
            data  = self.client.cancel_order(exchange_code=exchange_code,
                    order_id = order_id)

            if(data.get("Success",None) == None):
                print("Call Order Cancellation has not been successfull")
                print("----------END-------------------")
            else:
                print("Call Order Cancellation has  been successfull")
                print("----------END-------------------")
            
            
        
        elif(secondresponse.get('Success',None)!=None and firstresponse.get('Success',None)==None):
            print("Call order failed....")
            order_id = secondresponse['Success']['order_id']
            
            data = self.client.cancel_order(exchange_code=exchange_code,
                    order_id = order_id)
            
            if(data.get("Success",None) == None):
                print("Put Order Cancellation has not been successfull")
            else:
                print("Put Order Cancellation has  been successfull")
            
        
        elif(firstresponse.get('Success',None)==None and secondresponse.get('Success',None)==None):
            print("both order call and put have failed")
            print("------------END----------------")
            
        
        else:
            orderids = [] #0th index will contain call order, #1st index will contain put order 
            orderids.append(firstresponse['Success']['order_id']) 
            orderids.append(secondresponse['Success']['order_id'])            
            #define a mechanism to get profit and loss
            print("----lets wait for 5 seconds for getting the executed status---")
            time.sleep(5)
            details = self.client.get_order_detail(exchange_code=exchange_code,
                        order_id= orderids[0])

            call_status = None
            put_status = None

            #print(details)
            call_execution = -1
            put_execution = -1
            
            print(f"order ids are : {orderids}")
            for entry in details['Success']:
                if(entry['status'] == "Executed"):
                    call_execution = entry['average_price']
                    call_status = "Executed"
                    break
                    
            details = self.client.get_order_detail(exchange_code=exchange_code,
                        order_id= orderids[1])
            #print(details)
            for entry in details['Success']:
                if(entry['status'] == "Executed"):
                    put_execution = entry['average_price']
                    put_status = "Executed"
                    break
                    
            if(call_execution == -1 or put_execution == -1):
                print("Dear User order could not execute within time limit ..cancelling it")
                if(call_execution == -1 and put_execution == -1):
                    print("Both Order Call and Put could not execute to so cancelling it ..... ")
                    self.client.cancel_order(exchange_code=exchange_code,
                    order_id = orderids[0])
                    self.client.cancel_order(exchange_code=exchange_code,
                    order_id = orderids[1])

                elif(call_execution == -1):
                    #call cancel order api
                    print("call order could not execute due to some reason so cancelling order")
                    #self.squareoff(self,rightval,exchange_code, stock_code, product_type, expiry_date, right, strike_price, action, order_type, validity, stoploss, quantity, price,validity_date, trade_password, disclosed_quantity)
                    self.client.cancel_order(exchange_code=exchange_code,
                    order_id = orderids[0])

                    print("put order is executed squaring off....")
                    self.squareoff(exchange_code = self.exchange_code, stock_code = self.stock_code, product_type = self.product_type , expiry_date = self.expiry_date , strike_price = self.strike_price , order_type = self.order_type, validity = self.validity, stoploss = self.stoploss, quantity = self.quantity, price = "", validity_date = self.validity_date, trade_password = "", disclosed_quantity="0",right = "Put", action = "sell")

                elif(put_execution == -1):
                    #call cancel order api
                    print("put order could not execute due to some reason so cancelling order")
                    status = self.client.cancel_order(exchange_code=exchange_code,
                    order_id = orderids[1])
                    print("call order is executed squaring off....")
                    self.squareoff(exchange_code = self.exchange_code, stock_code = self.stock_code, product_type = self.product_type , expiry_date = self.expiry_date , strike_price = self.strike_price , order_type = self.order_type, validity = self.validity, stoploss = self.stoploss, quantity = self.quantity, price = "", validity_date = self.validity_date, trade_password = "", disclosed_quantity="0",right = "Call", action = "sell")
                    
            else:
                print("Call order got executed at price :{0} Rs and Put Order got executed at price : {1} Rs".format(call_execution,put_execution))
                self.profit_and_loss(product_type, stock_code, strike_price, qty, expiry_date, order_type, validity, validity_date, exchange_code, stoploss, call_price, put_price, orderids,call_execution,put_execution)
            
    def stop(self):

        print("squaring off the contract and exiting strategy...")
        self.squareoff(exchange_code = self.exchange_code, stock_code = self.stock_code, product_type = self.product_type , expiry_date = self.expiry_date , strike_price = self.strike_price , order_type = self.order_type, validity = self.validity, stoploss = self.stoploss, quantity = self.quantity, price = "", validity_date = self.validity_date, trade_password = "", disclosed_quantity="0",right = "Call", action = "sell")
        self.squareoff(exchange_code = self.exchange_code, stock_code = self.stock_code, product_type = self.product_type , expiry_date = self.expiry_date , strike_price = self.strike_price , order_type = self.order_type, validity = self.validity, stoploss = self.stoploss, quantity = self.quantity, price = "", validity_date = self.validity_date, trade_password = "", disclosed_quantity="0",right = "Put", action = "sell")

        self.client.ws_disconnect()

    def get_pnl(self):
        print("- Negative indicates loss")
        print(f" P & L(CALL):  {self.currentcall}/- Rs")
        print(f" P & L(PUT):  {self.currentput}/- Rs")
        outcome = (self.currentcall + self.currentput)*int(self.quantity)
        print(f"Total Profit/Loss for {self.quantity} is {outcome}/- Rs")

        print("------------------------------------------------------------------------------")
