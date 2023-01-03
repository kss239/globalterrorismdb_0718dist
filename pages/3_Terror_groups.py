import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import plotly.graph_objects as go

data = pd.read_csv("globalterrorismdb_0718dist (2).csv",
    # dtype={4:,6:,31:,33:,61:,62:,63:,76:,79:,90:,92:,94:,96:,114:,115:,121:}
    )

data.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed','nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
data=data[['eventid','Year','Month','Day','Country','Region','city','latitude','longitude','AttackType','Killed','Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]
data['casualities']=data['Killed']+data['Wounded']

def decade_stacked_plot(data,value,index,title_txt,num = 20):
        temp_bar = pd.pivot_table(data, values=value, index=[index],
                        columns=['Year'], aggfunc='count').fillna(0)

        temp_bar = temp_bar.loc[data[index].value_counts().iloc[:num].index]
        i = 0
        for decade in ['70s','80s','90s','00s']:
            temp_bar[decade] = temp_bar[temp_bar.columns[i]]
            i+=1
            for x in range(1,10):
                temp_bar[decade] += temp_bar[temp_bar.columns[i]]
                i+=1
        
        
        temp_bar['10s'] = temp_bar[temp_bar.columns[i]]
        i+=1

        for x in range(1,8):
                temp_bar['10s'] += temp_bar[temp_bar.columns[i]]
                i+=1

        temp_bar=temp_bar[['70s','80s','90s','00s','10s']]

        fig, ax = plt.subplots(figsize= (5,10))
        ax.bar(x=temp_bar.index,
                height = temp_bar[temp_bar.columns[0]],
                label=temp_bar.columns[0])
        
        bottom_col = [temp_bar.columns[0]]
        for year in range(1,len(temp_bar.columns)):
            ax.bar(x=temp_bar.index,
                height = temp_bar[temp_bar.columns[year]],
                bottom = temp_bar[bottom_col].sum(axis=1),
                label=temp_bar.columns[year])
            bottom_col.append(temp_bar.columns[year])

        ax.legend()
        ax.set_xticklabels(temp_bar.index, rotation=90)
        ax.set_title(title_txt)
        st.pyplot(fig)


decade_stacked_plot(data[data['Group']!='Unknown'],'Month','Group','Terrorists Groups responsible for most attacks',num = 10)


filter = data.groupby('Group')['casualities'].sum()>1000

temp_lst = list(data[(data['Group']!='Unknown') & (data['Group'].isin(list(filter[filter==True].index))==True)]['Group'].unique())
temp_lst.sort()
option = st.selectbox('Filter Group',options = temp_lst)
temp_data = data[data['Group'] == option]

temp_sankey_2 = temp_data.groupby(['Target_type','AttackType'])['casualities'].sum().reset_index()
temp_sankey_2.columns = ['source','target','value']

links = pd.concat([temp_sankey_2], axis = 0)
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

st.subheader('Target Type/Attack Type casuality numbers')
st.plotly_chart(fig, use_container_width=True)

st.dataframe(temp_data.groupby('Target_type')['casualities'].count().rename('Number of Attacks').sort_values(ascending=False))

st.dataframe(temp_data.groupby('AttackType')['casualities'].count().rename('Number of Attacks').sort_values(ascending=False))

st.dataframe(temp_data.groupby('Target_type')['casualities'].sum().rename('Number of Attacks').sort_values(ascending=False))

st.dataframe(temp_data.groupby('AttackType')['casualities'].sum().rename('Number of Attacks').sort_values(ascending=False))

dis_data = temp_data[temp_data['AttackType']=='Hijacking']
dis_data = dis_data[['Killed','Wounded']].dropna()
st.dataframe(dis_data)
#For every type of attack or Type of target
fig = plt.figure()
sns.distplot(a = dis_data['Killed'], hist = True, kde = False, rug = False)
st.pyplot(fig)