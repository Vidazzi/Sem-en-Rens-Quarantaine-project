# -*- coding: utf-8 -*-
"""
Created on Wed Apr 22 21:02:18 2020

@author: SCHIPP02
"""

import http.client
from datetime import timedelta, date
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

data_dict = {}

start_date = date(2020, 2, 1)
end_date = date(2020, 4, 22)
for single_date in daterange(start_date, end_date):
    var_date = single_date.strftime("%Y-%m-%d")
    
    
    conn = http.client.HTTPSConnection("covid-19-statistics.p.rapidapi.com")
    
    headers = {
        'x-rapidapi-host': "covid-19-statistics.p.rapidapi.com",
        'x-rapidapi-key': "a49fe3f800msh83aa49ec9ebaf11p1f4e8bjsncef479c922e5"
        }
    
    conn.request("GET", f"/reports/total?date={var_date}", headers=headers)
    
    res = conn.getresponse()
    data = res.read()
    
    data = data.decode("utf-8")
    data = eval(data)
    
    data_dict[var_date] = data["data"]
    

df = pd.DataFrame.from_dict(data_dict, orient='index')
print(df.columns)

df["date"] = df["date"].str.strip()
to_predict = df.tail(1)

df.drop(df.tail(1).index,inplace=True)

X = df.iloc[:, 2:3].values
Y = df.iloc[:, 4:5].values

from sklearn.linear_model import LinearRegression
lin_reg = LinearRegression()
lin_reg.fit(X, Y)

#polynomial
from sklearn.preprocessing import PolynomialFeatures
poly_reg = PolynomialFeatures(degree = 4)
X_poly = poly_reg.fit_transform(X)

lin_reg2 = LinearRegression()
lin_reg2.fit(X_poly, Y)

plt.scatter(X, Y, color = 'red')
plt.plot(X, lin_reg.predict(X), color = 'blue')
plt.title("Covid (Linear plot)")
plt.xlabel("Confirmed")
plt.ylabel("Deaths")
plt.show()


#polynomial visuals
X_grid = np.arange(min(X), max(X), 0.1)
X_grid = X_grid.reshape((len(X_grid), 1))
plt.scatter(X, Y, color = 'red')
plt.plot(X_grid, lin_reg2.predict(poly_reg.fit_transform(X_grid)), color = 'blue')
plt.title("Covid(Polynomial plot)")
plt.xlabel("Confirmed")
plt.ylabel("Deaths")
plt.show()


# linear regression predict
z = lin_reg.predict(np.array(int([to_predict["confirmed"].values][0])).reshape(1, 1))
print("Linear predict",z)
q = lin_reg2.predict(poly_reg.fit_transform(np.array(int([to_predict["confirmed"].values][0])).reshape(1, 1)))
print("Non-linear predict", q)

print("Actual", to_predict["deaths"])