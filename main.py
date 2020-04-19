"""
Ik ben nog even aan het kijken hoe het precies werkt.
"""


import pandas as pd
import http.client
import yaml
import altair as alt
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

alt.Chart(df).mark_point().encode(
    x='deaths',
    y='confirmed',
).interactive()

alt.Chart(df).mark_point().encode(
    y='longitude',
    x='latitude',
).interactive()

from vega_datasets import data as vega_data

source = alt.topo_feature(vega_data.world_110m.url, 'countries')

base = alt.Chart(source).mark_geoshape(
    fill='#666666',
    stroke='white'
).properties(
    width=300,
    height=180
)


gps_df = df[["longitude", "latitude"]]

gps = alt.Chart(gps_df).mark_circle(size=3).encode(
    longitude='longitude',
    latitude='latitude'
).project(
    type='mercator'
)

base + gps

