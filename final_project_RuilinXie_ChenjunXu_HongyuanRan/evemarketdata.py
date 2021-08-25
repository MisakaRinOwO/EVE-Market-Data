#evemarketdata by Misaka Rin in Py3.8
import requests, json, os, pprint
from urllib.parse import *
from pathlib import Path
#add functions to cloe connection after requests.get()
#12/16 V1.2
#fixed parameters
#12/17 V1.3
#class Batch work in progress
#12/17 V1.4
#reworked to fit GUI requirements

class ItemNameError(Exception):
    pass
class FilesNotFoundError(Exception):
    pass
class PlaceNameError(Exception):
    pass
class MarketerServerError(Exception):
    pass
class EmptyFileError(Exception):
    pass

#check the current buy/sell orders price on a specific item in a specific region/system market.
class marketdata(): 

    def __init__(self, item = '', place = '', place_id = '', placetype = ''):
        self.item = item
        self.place = place
        self.place_id = place_id
        self.placetype = placetype
    #get price data of an item in a specific location
    def getprice(self):
        url = f"https://api.evemarketer.com/ec/marketstat/json?typeid={self.item_id}&{self.placetype}={self.place_id}"
        u = requests.get(url)
        u.close()
        u = u.json()
        if type(u) is list:
            sell = u[0]['sell']
            buy = u[0]['buy']
            
            self.minsell = sell['min'] #useful data for users to know ↓
            self.avgsell = sell['avg']
            self.volsell = sell['volume']
            self.medsell = sell['median']
            self.stdsell = sell['stdDev']
            self.varsell = sell['variance']

            self.maxbuy = buy['max']
            self.avgbuy = buy['avg']
            self.volbuy = buy['volume']
            self.medbuy = buy['median']
            self.stdbuy = buy['stdDev']
            self.varbuy = buy['variance'] #useful data for users to know ↑
            return u


        else:
            raise MarketerServerError('The evemarketer server is down, please try it later.')
    #check item name validity through api
    def checkitem(self):
        url = f'http://www.fuzzwork.co.uk/api/typeid.php?typename={self.item}'
        self.item_id = requests.get(url)
        self.item_id.close()
        self.item_id = self.item_id.json()['typeID']
        if self.item_id == 0:
            raise ItemNameError('Please enter a valid item name.')
    #check place name validity through local file
    def checkplace(self):
        system_id_path = Path(os.getcwd())/'system_id.txt'
        region_id_path = Path(os.getcwd())/'region_id.txt'
        if os.path.exists(system_id_path):
            s = open(system_id_path,'r')
            sid = eval(s.read())
            s.close()
        else:
            raise FilesNotFoundError('Current folder is missing a system id file.')
        if os.path.exists(region_id_path):
            r = open(region_id_path,'r')
            rid = eval(r.read())
            r.close()
        else:
            raise FilesNotFoundError('Current folder is missing a region id file.')

        c = 0
        for i in sid:
            if self.place in str(i.keys()).lower():
                c += 1
                self.place_id = str(i.values())[str(i.values()).index('\'')+1 : -3]
        for i in rid:
            if self.place in str(i.keys()).lower():
                c += 1
                self.place_id = str(i.values())[str(i.values()).index('\'')+1 : -3]
        if c == 0:
            raise PlaceNameError('Please enter a valid region/system name.')
        if int(self.place_id) > 30000000:
            self.placetype = 'usesystem'
        else:
            self.placetype = 'regionlimit'



#check the value of a batch of items in a specific region/system market.
class batch(): 
    def __init__(self,place = ''):
        self.place = place
    #check place name validity through checkplace() method in class marketdata
    def checkplace_b(self):
        check = marketdata()
        check.place = self.place
        check.checkplace()
        self.place_id = check.place_id
        self.placetype = check.placetype
    #proccess entry and creats batch information
    def proccessfile(self,lst):
        self.batch = []
        self.items = []
        self.count = []
        item = 0
        count = 1
        volume = -2
        self.totvolume = 0 #final output
        for i in lst:
            self.batch.append(i.split('\t'))

        for i in self.batch:
            if i[item].lower() != 'personal items' and 'blueprint' not in i[item].lower():
                self.items.append(i[item])
                if ',' in i[count]:
                    self.count.append(i[count].replace(',',''))
                elif i[count] == '':
                    self.count.append('1')
                else:
                    self.count.append(i[count])
                if ',' in i[volume]:
                    self.totvolume += float(i[volume].replace(',','')[0 : i[volume].replace(',','').index(' ')])
                else:
                    self.totvolume += float(i[volume][0 : i[volume].index(' ')])
    #uses batch information to get total prices from the batch
    def getprices(self):
        self.totalsell = 0 #final output
        self.totalbuy = 0  #final output
        
        for i,x in zip(self.items,self.count):
            p = marketdata(item = i, place_id = self.place_id, placetype = self.placetype)
            p.checkitem()
            p.getprice()

            self.totalsell += p.minsell * float(x)
            self.totalbuy += p.maxbuy * float(x)







