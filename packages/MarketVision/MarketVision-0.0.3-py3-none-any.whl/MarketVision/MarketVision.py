import numpy as np
import pandas as pd

import yfinance as yf

getData=yf.download

def MACD(df,a,b,c):
	df['MA Fast']=df['Close'].ewm(span=a,min_periods=a).mean()
	df['MA Slow']=df['Close'].ewm(span=b,min_periods=b).mean()
	df['MACD']=df['MA Fast']-df['MA Slow']
	df['Signal']=df['MACD'].ewm(span=c,min_periods=c).mean()
	df['Histrogram']=df['MACD']-df['Signal']
	return df
