"""
ETH DAO Arbitrage

Jon V (May 30th 2016)
"""
import time
from kraken import Kraken
from twilio.rest import TwilioRestClient 

PERCENTAGE_RETURN = 1.10 # 10%
DAO_KRAKEN_DEPOSIT_ADDRESS = 'your_address'
ETH_KRAKEN_RETURN_ADDRESS = 'eth_address'
TWILIO_ACCOUNT_SID = "sid"
TWILIO_AUTH_TOKEN = "token"

def calc_DAO2ETH_price(number_of_start_ethereums, number_of_DAO):
    order_price = (number_of_start_ethereums * PERCENTAGE_RETURN) / 0.99849 / number_of_DAO
    return order_price
    

def load_last_eth_balance():
    with open("eth_balance.txt", "r") as fd:
        return fd.readline()

def save_last_eth_balance(eth_balance):
    with open("eth_balance.txt", "w+") as fd:
        fd.write(str(eth_balance))


def run():
    print "Starting Arb"
    
    k = Kraken()
    last_eth_balance = float(load_last_eth_balance())
    dao_balance = k.dao_balance()
    
    eth_trade_price = round(calc_DAO2ETH_price(float(last_eth_balance), dao_balance), 5)

    if k.latest_price() > eth_trade_price:
        eth_trade_price = k.latest_price()
        
    trade_id = k.trade(price=eth_trade_price, lots=dao_balance)
    if trade_id:
        while k.order_status(trade_id) != 'closed':
            print "Waiting for trade to execute"
            time.sleep(5)
            
        # order was executed, check how much we made
        if k.order_status(trade_id) == 'closed':
            eth_balance = k.eth_balance()
            if eth_balance > last_eth_balance:
                print "Success! We made", eth_balance-last_eth_balance, "ethereum"
                save_last_eth_balance(eth_balance)
                send_sms(eth_balance)

                # now, send to shapeshift
                print "Shapeshift refid", k.withdrawn(eth_balance)

                # check account for DAO and if > 1 that means money are here
                while k.dao_balance() < 1:
                    time.sleep(5)

                # check if all ok and go again
                if k.dao_balance() > dao_balance:
                    print "We are going again!"
                    print "DAO Balance is", k.dao_balance()

            else:
                raise Exception
        else:
            raise Exception


def send_sms(eth_price):
    client = TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) 
    client.sms.messages.create(
        to="+14152835417", 
        from_="+1 415-599-2671",
        body="1353-2236 ETH:" + str(eth_price))
    
    


if __name__ == '__main__':
    while True:
        run()


    
    

    
