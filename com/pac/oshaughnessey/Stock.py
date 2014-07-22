import jinja2
import os

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

class Stock(object):
    '''
    classdocs
    '''
    tickerSymbol = ''
    companyName = ''
    marketCap = 0
    
    #Ranked fields 
    pe = 0
    peRank = 0
    
    ps = 0
    psRank = 0
    
    pb = 0
    pbRank = 0
    
    pfreeCashFlow = 0
    pfreeCashFlowRank = 0
    
    enterpriseValueEBITDA = 0
    enterpriseValueEBITDARank = 0
    
    shareholderYield = 0
    shareholderYieldRank = 0
    
    dividendYield = 0
    salePurchaseOfStock = 0
    performanceHalfYear = 0
    price = 0

    score = 0


    def __init__(self, params):
        '''
        Constructor
        '''
        self.defaultHi=100000
        self.defaultLo=0
        self.tickerSymbol = params[1]
        self.companyName = params[2]
        self.marketCap = (self.convertToFloat(params[3],1))*1000000
        self.pe = self.convertToFloat(params[4],self.defaultHi)
        self.ps = self.convertToFloat(params[5],self.defaultHi)
        self.pb = self.convertToFloat(params[6],self.defaultHi)
        self.pfreeCashFlow = self.convertToFloat(params[7],self.defaultHi)
        self.dividendYield = self.convertToFloat(params[8],self.defaultLo)
        self.performanceHalfYear = self.convertToFloat(params[9],self.defaultLo)
        self.price = self.convertToFloat(params[10],self.defaultHi)
        
    def updateKeyStats(self,json):
        try:
            enterpriseValueEBITDA = json['query']['results']['stats']['EnterpriseValueEBITDA']['content']
        except KeyError:
            enterpriseValueEBITDA = str(self.defaultHi)
        except TypeError:
            enterpriseValueEBITDA = str(self.defaultHi)
                
        self.enterpriseValueEBITDA = self.convertToFloat(enterpriseValueEBITDA, self.defaultHi) 
         
    def updateCashFlow(self,json):
        try:
            salePurchaseOfStock = json['query']['results']['cashflow']['statement'][0]['SalePurchaseofStock']['content']
        except KeyError:
            salePurchaseOfStock = str(self.defaultLo)
        except TypeError:
            salePurchaseOfStock = str(self.defaultLo)
            
        self.salePurchaseOfStock = self.convertToFloat(salePurchaseOfStock, self.defaultLo)
        self.shareholderYield = self.dividendYield - (self.salePurchaseOfStock / self.marketCap)*100
    
    def convertToFloat(self, floatString, defaultValue):
        floatString = floatString.strip('%')
        try:
            floatValue = float(floatString)
        except ValueError,e:
            floatValue = defaultValue
        return floatValue
        
    def toString(self):
        output = self.tickerSymbol + '\n'
        output += self.companyName + '\n'
        output += str(self.score) + '\n'
        output += 'MarketCap=' + str(self.marketCap) + '\n'
        output += 'PE=' + str(self.pe) + '\n'
        output += 'PS=' + str(self.ps) + '\n'
        output += 'PB=' + str(self.pb) + '\n'
        output += 'pfreeCashFlow=' + str(self.pfreeCashFlow) + '\n'
        output += 'dividendYield=' + str(self.dividendYield) + '\n'
        output += 'performanceHalfYear=' + str(self.performanceHalfYear) + '\n'
        output += 'price=' + str(self.price) + '\n'
        output += 'enterpriseValueEBITDA=' + str(self.enterpriseValueEBITDA) + '\n'
        output += 'salePurchaseOfStock=' + str(self.salePurchaseOfStock) + '\n'
        output += 'shareholderYield=' + str(self.shareholderYield) + '\n'      
        return output

    def calculateScores(self):
        score = self.peRank + self.psRank + self.pbRank + self.pfreeCashFlowRank \
            + self.enterpriseValueEBITDARank + self.shareholderYieldRank
        self.score = score
        
    def toHTML(self,templateString):
        print os.path.join(os.path.dirname(__file__))
        templateLoader = jinja2.FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates' ))
        templateEnv = jinja2.Environment( loader=templateLoader )
        template = templateEnv.get_template('stockDiv.html')
        templateVars = { "tickerSymbol" : self.tickerSymbol,
                        "companyName" : self.companyName,
                        "marketCap": self.marketCap,
                        "pe": self.pe,
                        "peRank": self.peRank,
                        "ps": self.ps,
                        "psRank": self.psRank,
                        "pb": self.pb,
                        "pbRank": self.pbRank,
                        "pfreeCashFlow": self.pfreeCashFlow,
                        "pfreeCashFlowRank": self.pfreeCashFlowRank,
                        "enterpriseValueEBITDA": self.enterpriseValueEBITDA,
                        "enterpriseValueEBITDARank": self.enterpriseValueEBITDARank,
                        "shareholderYield": self.shareholderYield,
                        "shareholderYieldRank": self.shareholderYieldRank,
                        "dividendYield": self.dividendYield,
                        "salePurchaseOfStock" :self.salePurchaseOfStock,
                        "performanceHalfYear": self.performanceHalfYear,
                        "price": self.price,
                        "score": self.score}
        return template.render( templateVars )


#     score = 0