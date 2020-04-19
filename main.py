"""
Ik ben nog even aan het kijken hoe het precies werkt.
"""


import pandas as pd
import http.client
import yaml

conn = http.client.HTTPSConnection("covid-19-data.p.rapidapi.com")

headers = {
    'x-rapidapi-host': "covid-19-data.p.rapidapi.com",
    'x-rapidapi-key': "a49fe3f800msh83aa49ec9ebaf11p1f4e8bjsncef479c922e5"
    }

conn.request("GET", "/country/all?format=json", headers=headers)

res = conn.getresponse()
data = res.read()

data = data.decode("utf-8")
data = data.replace("null", "")

data = yaml.load(data)
df = pd.DataFrame(data)

print(df.head)

