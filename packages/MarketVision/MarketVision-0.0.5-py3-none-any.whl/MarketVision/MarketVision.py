import numpy as np
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import yfinance as yf

getData=yf.download

def MACD(df,a,b,c):
	df['MA Fast']=df['Close'].ewm(span=a,min_periods=a).mean()
	df['MA Slow']=df['Close'].ewm(span=b,min_periods=b).mean()
	df['MACD']=df['MA Fast']-df['MA Slow']
	df['Signal']=df['MACD'].ewm(span=c,min_periods=c).mean()
	df['Histrogram']=df['MACD']-df['Signal']
	return df
	
def getTarget(df,next):
	conditions=[df['Close']==df['Open'],df['Open']>df['Close'],df['Open']<df['Close']]
	choices=['Equal','Decreasing','Increasing']
	df['target']=np.select(conditions,choices) 
	df['target']=df['target'].shift(-next)
	df=df.dropna()
	target=df['target'].values
	df=df.drop(columns=['target'])
	return {'data':df,'target':target}

def data_display(data):
	print(data,'\n',type(data))

def standardize(X):
	sc=StandardScaler()
	sc.fit(X)
	X_std=sc.transform(X)
	return X_std

def runPCA(X_train_std):
	pca=PCA()
	X_train_pca=pca.fit_transform(X_train_std)
	return pca.explained_variance_ratio_
	