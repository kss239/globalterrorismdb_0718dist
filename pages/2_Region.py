import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import seaborn as sns
sns.set_style('darkgrid')
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

data = pd.read_csv("globalterrorismdb_0718dist (2).csv",
    # dtype={4:,6:,31:,33:,61:,62:,63:,76:,79:,90:,92:,94:,96:,114:,115:,121:}
    )

data.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed','nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
data=data[['eventid','Year','Month','Day','Country','Region','city','latitude','longitude','AttackType','Killed','Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]
data['casualities']=data['Killed']+data['Wounded']

st.title("Global Terrorism")

import datashader as ds
from colorcet import fire
import datashader.transfer_functions as tf

st.subheader('Terrorist Attacks By Region & Country')

option = st.selectbox('Filter Region',options = data['Region'].unique())
temp_data = data[data['Region'] == option]

temp_sankey_1 = temp_data.groupby(['Region','Country'])['casualities'].sum().reset_index()
temp_sankey_1.columns = ['source','target','value']
temp_sankey_2 = temp_data.groupby(['Country','AttackType'])['casualities'].sum().reset_index()
temp_sankey_2.columns = ['source','target','value']

links = pd.concat([temp_sankey_1,temp_sankey_2], axis = 0)
unique_sources_targets = list(pd.unique(links[['source','target']].values.ravel("K")))
mapping_dict = {k:v for v,k in enumerate(unique_sources_targets)}

links['source'] = links['source'].map(mapping_dict)
links['target'] = links['target'].map(mapping_dict)
links_dict = links.to_dict(orient='list')

fig = go.Figure(data=[go.Sankey(
    node = dict(
    pad = 15,
    thickness = 20,
    line = dict(color = "black", width = 0.5),
    label = unique_sources_targets,
    color = "blue"
    ),
    link = dict(
        source = links_dict['source'],
        target = links_dict['target'],
        value = links_dict['value'],
    )
)])

fig.update_layout(title_text="Terrorist Attack Type", font_size=10)
st.plotly_chart(fig, use_container_width=True)

options = st.multiselect('Highligh Country', temp_data['Country'].unique())

temp_line=pd.pivot_table(temp_data, values='Month', index=['Year'],
                columns=['Country'], aggfunc='count').fillna(0)
temp_line = temp_line.cumsum()

fig = plt.figure(figsize=(12,4))
option_1 = options
if option_1 == []:
    option_1 = temp_line.columns
sns.lineplot(data = temp_line[option_1])
plt.legend(loc='upper left',bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=90)
plt.title('Cumulative Sum of Terror Attacks')
st.pyplot(fig)


temp_line=pd.pivot_table(temp_data, values='casualities', index=['Year'],
                columns=['Country'], aggfunc='sum').fillna(0)


fig = plt.figure(figsize=(12,4))
option_2 = options
if option_2 == []:
    option_2 = temp_line.columns
sns.lineplot(data = temp_line[option_2])
plt.legend(loc='upper left',bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=90)
plt.title('Casualities By Year')
st.pyplot(fig)


temp_data = data[data['Country'].isin(option_2)]
print(temp_data)
st.write('Count Type of attacks by each country')
fig = plt.figure(figsize=(12,4))
sns.countplot(x = temp_data['AttackType'],hue = temp_data['Country'])
plt.legend(loc='upper left',bbox_to_anchor=(1.05, 1))
plt.xticks(rotation=90)
plt.title('Number Of Terrorist Activities Each Year')
st.pyplot(fig)
fig = plt.figure()



options = st.selectbox('Filter Countries',options = temp_data['Country'].unique())
temp_data = data[data['Country']==options]

range = st.slider(
    'Select a range of Years',
    min_value = 1970, max_value = 2017, 
    value = (1970,2017), step = 1, help = None
    )

cvs = ds.Canvas(plot_width=1000, plot_height=1000)
agg = cvs.points(temp_data, x='longitude', y='latitude')
# agg is an xarray object, see http://xarray.pydata.org/en/stable/ for more details
coords_lat, coords_lon = agg.coords['latitude'].values, agg.coords['longitude'].values
# Corners of the image, which need to be passed to mapbox
coordinates = [[coords_lon[0], coords_lat[0]],
            [coords_lon[-1], coords_lat[0]],
            [coords_lon[-1], coords_lat[-1]],
            [coords_lon[0], coords_lat[-1]]]


img = tf.shade(agg, cmap=fire)[::-1].to_pil()
fig = plt.figure(figsize=(12,4))

fig = px.scatter_mapbox(temp_data[(temp_data['Year']>=range[0]) & (temp_data['Year']<=range[1])], lat='latitude', lon='longitude',color = 'Group',hover_name = 'eventid',hover_data = ['Group','city','AttackType','Target_type','Killed','Wounded'],zoom = 5)
# Add the datashader image as a mapbox layer image
fig.update_layout(mapbox_style="carto-darkmatter",
                mapbox_layers = [
                {
                    "sourcetype": "image",
                    "source": img,
                    "coordinates": coordinates
                }]
)
st.plotly_chart(fig, use_container_width=True)

#Most Active Groups