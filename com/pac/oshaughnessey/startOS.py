from stockdata.FinViz import FinViz
from stockdata.Yahoo import Yahoo
from Stock import Stock
from algorithm.OShaughnessey import OShaughnessey
import logging
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

'''
The basic principle of the "Trending Value" method is as follows:
Each company is scored on 6 performance metrics:
    * Price to Earnings (P/E ratio)
    * Price to Sales (P/S ratio)
    * Price to Book (P/B ratio)
    * Price to Free Cash Flow (P/FCF ratio)
    * Enterprise Value / EBITDA (EV/EBITDA ratio)
    * Shareholder Yield (Dividend Yield + Buyback Yield = equity returned
    to the investors)
    
    TODO: Allow the script to continue if an interruption occurs 
    
    
'''

if __name__ == '__main__':
    pass

    logging.basicConfig()
    logger = logging.getLogger()

    stockListCSV = FinViz.getStockData()
      
    stockList = []
    skipHeader = True
    for stockData in stockListCSV:
          
        if (skipHeader == False):
            stock = Stock(stockData)
            # Populate Enterprise.Value/EBITDA information from Yahoo's key stats
            stock.updateKeyStats(Yahoo.getKeyStats(stockData[1]))
            print "Update keystats on " + stockData[1]
                
            # Populate buy back yield
            stock.updateCashFlow(Yahoo.getCashFlow(stockData[1]))
            print "Update cashFlow on " + stockData[1]
            print stock.toString()
            stockList.append(stock)
            logging.debug("Updated stock ticker: " + stockData[1])  
              
        else:
            skipHeader = False
      
    ratedStocks=[]
    oShaughnessey = OShaughnessey()    
    ratedStocks = oShaughnessey.sort(stockList)
    
    sortedRatings = sorted(ratedStocks, key=lambda stock: stock.score, reverse=True)
    htmlFile = open('scores.htm', 'w')
    for stock in sortedRatings:
        htmlFile.write(stock.toString())
        htmlFile.write('----------------------------------------------------\n')
    htmlFile.close()

    # Now find the top 10% and sort by momentum
    tenPercentLength = int(round(len(sortedRatings)/10.00))
    topTenPercentOfSortedRatings = sortedRatings[:tenPercentLength]
    sortedRatings = sorted(topTenPercentOfSortedRatings, key=lambda stock: stock.performanceHalfYear, reverse=True)
    topTwentyFiveStocks = sortedRatings[:25]

    headerFile = open(os.path.join(os.path.dirname(__file__), 'templates/headerDiv.html' ), 'r+')
    footerFile = open(os.path.join(os.path.dirname(__file__), 'templates/footerDiv.html' ), 'r+')
        
    filteredFile = open('results.htm', 'w')
    filteredFile.write(headerFile.read())
    for stock in topTwentyFiveStocks:
        filteredFile.write(stock.toHTML('ff'))
    filteredFile.write(footerFile.read())
    filteredFile.close()
    
    headerFile.close()
    footerFile.close()

    
