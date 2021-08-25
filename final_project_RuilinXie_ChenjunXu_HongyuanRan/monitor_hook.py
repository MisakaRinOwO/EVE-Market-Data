from evemarketdata import marketdata
import time
#Get name from user
from dhooks import Webhook


class Monitor_data:
    #initialize by entering optional place/item data
    def __init__(self, item = '', place = '', place_id = '', placetype = '', datatype = '', comparison = '', expected_price = None, discord_hook = ''):
        self.item = item
        self.place = place
        self.place_id = place_id
        self.placetype = placetype

        self.datatype = datatype
        self.comparison = comparison
        self.expected_price = float(expected_price)

        self.delay = 60
        self.discord_hook = discord_hook
        
        
    #generate item price data
    def generate_data(self):
        mon = marketdata(item = self.item, place = self.place, place_id = self.place_id, placetype = self.placetype)
        mon.checkitem()
        mon.getprice()
        self.minsell = float(mon.minsell)
        self.avgsell = float(mon.avgsell)
        self.volsell = float(mon.volsell)
        self.medsell = float(mon.medsell)
        self.stdsell = float(mon.stdsell)
        self.varsell = float(mon.varsell)

        self.maxbuy = float(mon.maxbuy)
        self.avgbuy = float(mon.avgbuy)
        self.volbuy = float(mon.volbuy)
        self.medbuy = float(mon.medbuy)
        self.stdbuy = float(mon.stdbuy)
        self.varbuy = float(mon.varbuy)


    #sending item data to discord channels through webhook
    def data_solving(self):
        while True:
            hook = Webhook(self.discord_hook)

            list_datatype = ['avgsell', 'volsell', 'medsell', 'stdsell','varsell', 'maxbuy', 'avgbuy', 'volbuy', 'medbuy', 'stdbuy', 'varbuy', 'minsell']
            if self.datatype in list_datatype:
                text = ''
                
                if self.datatype == 'minsell' :
                    if self.minsell >= self.expected_price  and self.comparison =='>=':
                        text = f'Minimum Sell Price of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                    elif self.minsell <= self.expected_price and self.comparison == '<=':
                        text = f'Minimum Sell Price of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text)

                elif self.datatype == 'avgsell':
                    if self.avgsell >= self.expected_price and self.comparison == '>=':
                        text = f'Average Sell Price of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                    elif self.avgsell <= self.expected_price and self.comparison == '<=':
                        text = f'Average Sell Price of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'volsell':
                    if self.volsell >= self.expected_price and self.comparison =='>=':
                        text = f'Volume Sold of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                    elif self.volsell <= self.expected_price and self.comparison == '<=':
                        text = f'Volume Sold {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'medsell':
                    if self.medsell >= self.expected_price and self.comparison =='>=':
                        text = f'Median Sell Price of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                    elif self.medsell <= self.expected_price and self.comparison == '<=':
                        text = f'Median Sell Price of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text)

                elif self.datatype == 'stdsell':
                    if self.stdsell >= self.expected_price and self.comparison =='>=':
                        text = f'Selling Standard Deviation of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                    elif self.stdsell <= self.expected_price and self.comparison == '<=':
                        text = f'Selling Standard Deviation of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'varsell':
                    if self.varsell >= self.expected_price and self.comparison =='>=':
                        text = f'Selling Variance of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                    elif self.varsell <= self.expected_price and self.comparison == '<=':
                        text = f'Selling Variance of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'maxbuy':
                    if self.maxbuy >= self.expected_price and self.comparison =='>=':
                        text = f'Maximum Sell Price of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                    elif self.maxbuy <= self.expected_price and self.comparison == '<=':
                        text = f'Maximum Sell Price of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'avgbuy':
                    if self.avgbuy >= self.expected_price and self.comparison =='>=':
                        text = f'Average Buy Price of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                elif self.avgbuy <= self.expected_price and self.comparison == '<=':
                        text = f'Average Buy Price of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'volbuy':
                    if self.volbuy >= self.expected_price and self.comparison =='>=':
                        text = f'Volume Buy of {self.item} is higher thalower thanexpected price({self.expected_price})'
                        hook.send(text)
                elif self.volbuy <= self.expected_price and self.comparison == '<=':
                        text = f'Volume Buy of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'medbuy':
                    if self.medbuy >= self.expected_price and self.comparison =='>=':
                        text = f'Median Buy Price of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                elif self.medbuy <= self.expected_price and self.comparison == '<=':
                        text = f'Median Buy Price of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'stdbuy' and self.comparison =='>=':
                    if self.stdbuy >= self.expected_price:
                        text = f'Buying Standard Deviation of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                elif self.stdbuy <= self.expected_price and self.comparison == '<=':
                        text = f'Buying Standard Deviation of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text) 

                elif self.datatype == 'varbuy' :
                    if self.varbuy >= self.expected_price  and self.comparison =='>=':
                        text = f'Buying Variance of {self.item} is higher than expected price({self.expected_price})'
                        hook.send(text)
                elif self.varbuy <= self.expected_price and self.comparison == '<=':
                        text = f'Buying Variance of {self.item} is lower than expected price({self.expected_price})'
                        hook.send(text)                                           
                time.sleep(self.delay) 

            else:
                print('Error of datatype')
                time.sleep(self.delay) 






