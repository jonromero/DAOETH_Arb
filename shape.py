"""
Lib for Shapeshuft

Jon V (May 30th 2016)
"""
from shapeshiftio import ShapeShiftIO

class Shape():

    def __init__(self):
        self.__api = ShapeShiftIO()

    #shift(DAO_KRAKEN_DEPOSIT_ADDRESS,
    """
    def shift(self, deposit_address, return_address):
        postdata = {'withdrawal', deposit_address,
                    'pair': 'eth_dao',
                    'returnAddress': return_address,
                    
                   
        self.__api.shift(postdata)
    """

    def send_amount(self, deposit_address, return_address, amount):
        post_data = {'amount': amount,
                     
        
        self.__api.send_amount()
        
    def account_balance(self):
        return self.__api.query_private('Balance')['result']


    def dao_balance(self):
        return float(self.account_balance()['XDAO'])


    def eth_balance(self):
        return float(self.account_balance()['XETH'])


    def trade(self, price, lots):
        print "Selling", lots,  "DAO/ETH @", price
        b = 1/0
        result = self.__api.query_private('AddOrder', {'pair': 'XDAOETH',
                                                       'type': 'sell',
                                                       'ordertype': 'limit',
                                                       'price': str(price),
                                                       'volume': str(lots)})
        print result['txid']


    def order_status(self, order_id):
        result = self.__api.query_private('QueryOrders', {'txid': order_id})
        print result['txid']

