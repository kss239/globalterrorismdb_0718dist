import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import seaborn as sns
sns.set_style('darkgrid')
import matplotlib.pyplot as plt
import plotly.express as px

data = pd.read_csv("globalterrorismdb_0718dist (2).csv",
    # dtype={4:,6:,31:,33:,61:,62:,63:,76:,79:,90:,92:,94:,96:,114:,115:,121:}
    )

data.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed','nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
data=data[['eventid','Year','Month','Day','Country','Region','city','latitude','longitude','AttackType','Killed','Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]
data['casualities']=data['Killed']+data['Wounded']



st.title("Global Terrorism")

fig = px.scatter_geo(data.dropna(), lat='latitude',lon = 'longitude',
                    hover_name='Country', hover_data=['AttackType','Group','Motive'],
                    size='casualities',
                    animation_frame="Year",
                    projection="natural earth",
                    width=1200, height=600)
st.plotly_chart(fig, use_container_width=True)


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
        print(temp_bar[bottom_col].sum())
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



col1, col2, col3 = st.columns([2,1,1])

with col1:
    st.header('App Summary:')
    st.write('There have been two periods of Global Terrorism see in this data, One that started in the 70s and continued until the late 90s, the Second that started in the early 2000 that persists beyond the data covered. This App should give a breif but insightful overview of Global Terrorism through Time, Place, and Organizations, and giving tools for deeper investigation while in the Unknown Attackers page this app will give clarity into who the unknown perpetrators of many attacks were.')
    fig = plt.figure(figsize=(12,4))
    sns.countplot(x = data['Year'])
    plt.xticks(rotation=90)
    plt.title('Number Of Terrorist Activities Each Year')
    st.pyplot(fig)


with col2:
    decade_stacked_plot(data,'Month','Country','Number of Terrorist Activities in Each County',num=10)

with col3:
    decade_stacked_plot(data,'Month','Region','Number of Terrorist Activities in Each Region')


