#
#  stkDf 1.0 (stock Dataframe version 1.0): Python module - retrieves stock quote data from Yahoo Finance
#  and enables you to create concatenated dataframes for data analysis on daily stock performance
#  as compared to the S&P 500 Index
#  
#  Copyright (c) 2013 Joel O'Neil (joel.oneil@hotmail.com)
#
#  license: GNU LGPL
#
#  This library is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  Requires: Python 2.7/3.2+

#Importing all Necessary libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import pandas.io.data as web
import datetime
%matplotlib inline

####Creating custom libraries#####

#Global Variables to be initialized
#stock_symbol = "AAPL"
#stock_name = "Apple"
start = datetime.datetime(2013, 9, 10)
end = datetime.datetime(2013, 12, 6)
trend_loc = '/Users/joeloneil/Python/newdata1.csv'

#reading price data from Yahoo! finance
def index_price(stock_symbol, stock_name, start, end):
    read_data = web.DataReader(stock_symbol, 'yahoo', start, end)
    price = read_data['Adj Close'].pct_change()
    price.name = stock_name+'_Price'
    return price

#loading S&P pct change data
sandp_price = index_price("^GSPC", "S&P", start, end)

#reading price data from Yahoo! finance
def stk_price(stock_symbol, stock_name, start, end):
    read_data = web.DataReader(stock_symbol, 'yahoo', start, end)
    price = read_data['Adj Close'].pct_change()
    price.name = stock_symbol+'_Price'
    return price

#reading volume data from Yahoo! finance
def stk_vol(stock_symbol, stock_name, start, end):
    read_data = web.DataReader(stock_symbol, 'yahoo', start, end)
    vol = read_data['Volume'].pct_change()
    vol.name = stock_symbol+'_Vol'
    return vol

#loading google trend data
def stk_trend(trend_loc, stock_name, stock_symbol):
    read_trend = pd.read_csv(trend_loc, sep=',', index_col='Day')
    trend = read_trend[stock_name].astype(float)
    trend.name = stock_symbol+'_Trend'
    return trend

###creating stock dataframe####
def stkDf(stock_symbol,
          stock_name,
          start,
          end,
          trend_loc,
          sandp_price,
          targetV):
    stkDf_price = stk_price(stock_symbol, stock_name, start, end)
    stkDf_vol = stk_vol(stock_symbol, stock_name, start, end)
    stkDf_trend = stk_trend(trend_loc, stock_name, stock_symbol)
    stock_dataframe = pd.concat([stkDf_trend, stkDf_vol, stkDf_price, sandp_price], join='outer', axis = 1)
    stkDf_tv = target_variable(stkDf_price, sandp_price)
    stock_dataframe[targetV] = stkDf_tv
    return stock_dataframe

    
###calculating target variable####
def target_variable(stock_price, sandp_price):
    n = 0
    tvlist = []
#iterating and comparing stock and S&P data then populating target variable list
    for n in range(0, len(stock_price)-1):
        tvariable = int(stock_price[n] > sandp_price[n+1])
        tvlist.append(tvariable)
        n = 1 + n
#needed to append final value
    tvlist.append('??')
    return tvlist


###-----------Example-----------####

###Generating Training data for all 10 stocks by creating & contatenating dataframes####

#Creating Dataframes
apple = stkDf('AAPL', 'Apple', start, end, trend_loc, sandp_price, 'Apple_TV')
amazon = stkDf('AMZN', 'Amazon', start, end, trend_loc, sandp_price, 'Amazon_TV')

#concatenating dataframes
training_data = pd.concat([apple, amazon,], join='outer', axis = 1)

#printing sample
print training_data.head()


###-------Output---------####

AAPL_Trend  AAPL_Vol  AAPL_Price  S&P_Price Apple_TV  AMZN_Trend  \
Day                                                                         
9/10/13         100       NaN         NaN        NaN        0          51   
9/11/13          58  0.209233   -0.054436   0.003052        0          50   
9/12/13          35 -0.550403    0.010645  -0.003380        1          50   
9/13/13          31 -0.260402   -0.016491   0.002715        0          49   
9/16/13          26  0.819418   -0.031783   0.005693        0          52   

         AMZN_Vol  AMZN_Price  S&P_Price Amazon_TV  
Day                                                 
9/10/13       NaN         NaN        NaN         0  
9/11/13 -0.020130   -0.002397   0.003052         1  
9/12/13 -0.078274   -0.002603  -0.003380         0  
9/13/13 -0.159133   -0.003145   0.002715         0  
9/16/13  0.338960   -0.006243   0.005693         0  
