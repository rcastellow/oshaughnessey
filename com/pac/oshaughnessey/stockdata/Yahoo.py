import urllib2
import json
import time

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

class Yahoo(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''
        
    @staticmethod
    def getKeyStats(stockTicker):  
        yahooURL = 'https://query.yahooapis.com/v1/public/yql?q='
        yqlString1 = 'select%20*%20from%20yahoo.finance.keystats%20where%20symbol%20in%20(%22'  
        yqlString2 = '%22)%0A%09%09&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback='
        try:
            response = urllib2.urlopen(yahooURL + yqlString1 + stockTicker + yqlString2)
        except urllib2.HTTPError:
            time.sleep(15)
            response = urllib2.urlopen(yahooURL + yqlString1 + stockTicker + yqlString2)
        return json.loads(response.read())
    
    @staticmethod
    def getCashFlow(stockTicker):
        yahooURL = 'https://query.yahooapis.com/v1/public/yql?q='
        yqlString1 = 'SELECT%20*%20FROM%20yahoo.finance.cashflow%20WHERE%20symbol%3D\''
        yqlString2 = '\'&format=json&diagnostics=true&env=http%3A%2F%2Fdatatables.org%2Falltables.env&callback='
        try:
            response = urllib2.urlopen(yahooURL + yqlString1 + stockTicker + yqlString2)
        except urllib2.HTTPError:
            time.sleep(15)
            response = urllib2.urlopen(yahooURL + yqlString1 + stockTicker + yqlString2)
        return json.loads(response.read())  
          
