import math
'''
Created on February 6, 2014

@author: RobCastellow

Copyright (c) 2014 PAC Enterprises, LLC

Permission is hereby granted, free of charge, to any person obtaining a copy of this software 
and associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, 
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial
portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT 
NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

class OShaughnessey(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def sort(self, stockList):
        sortedByPE = sorted(stockList, key=lambda stock: stock.pe, reverse=True)
        stockList = self.rankByField(sortedByPE, 'pe')
        sortedByPS = sorted(stockList, key=lambda stock: stock.ps, reverse=True)
        stockList = self.rankByField(sortedByPS, 'ps')
        sortedByPB = sorted(stockList, key=lambda stock: stock.pb, reverse=True)
        stockList = self.rankByField(sortedByPB, 'pb')
        sortedByPFreeCashFlow = sorted(stockList, key=lambda stock: stock.pfreeCashFlow, reverse=True)
        stockList = self.rankByField(sortedByPFreeCashFlow, 'pfreeCashFlow')
        sortedByEnterpriseValueEBITDA = sorted(stockList, key=lambda stock: stock.enterpriseValueEBITDA, reverse=False)
        stockList = self.rankByField(sortedByEnterpriseValueEBITDA, 'enterpriseValueEBITDA')
        sortedByShareholderYield = sorted(stockList, key=lambda stock: stock.shareholderYield, reverse=False)
        stockList = self.rankByField(sortedByShareholderYield, 'shareholderYield')

        for stock in stockList:
            stock.calculateScores()
        return stockList
    
    def rankByField(self, sortedList, sortedField):
        listSize = len(sortedList)
        count = 1
        for sortedStock in sortedList:
            if (getattr(sortedStock,sortedField) == sortedStock.defaultHi or \
                getattr(sortedStock,sortedField) == sortedStock.defaultLo):
                rank = 1.0
            else:
                rank = math.ceil((float(count) / listSize) * 100)
            setattr(sortedStock,sortedField + 'Rank',rank) 
            count = count + 1
        return sortedList
            
            
        
        
