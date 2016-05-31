"""
Lib for Kraken

Jon V (May 30th 2016)
"""
import krakenex

class Kraken():

    def __init__(self):
        self.__api = krakenex.API()
        self.__api.load_key('kraken_key')
    

    def pair_info(self):
        return self.__api.query_public('AssetPairs')


    def latest_price(self):
        return float(self.__api.query_public('Ticker', {'pair': 'XDAOXETH'})['result']['XDAOXETH']['b'][0])

        
    def account_balance(self):
        return self.__api.query_private('Balance')['result']


    def dao_balance(self):
        return float(self.account_balance()['XDAO'])


    def eth_balance(self):
        return float(self.account_balance()['XETH'])


    def trade(self, price, lots):
        print "Selling", lots,  "DAO/ETH @", price
        result = self.__api.query_private('AddOrder', {'pair': 'XDAOXETH',
                                                       'type': 'sell',
                                                       'ordertype': 'limit',
                                                       'price': str(price),
                                                       'volume': str(lots)})
        return result['result']['txid'][0]


    def order_status(self, order_id):
        result = self.__api.query_private('QueryOrders', {'txid': order_id})
        return result['result'][order_id]['status']


    def withdrawn(self, amount):
        result = self.__api.query_private('Withdraw', {'key': 'Kraken2',
                                                       'asset': 'XETH',
                                                       'amount': amount})
        return result['result']['refid']

                                    

