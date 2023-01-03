import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import plotly.graph_objects as go

st.header('Predicting Responsibility for events with Unknown Attacker')
st.header('Under Development')
#CHIAD decision tree https://datapeaker.com/en/big--data/chaid-algorithm-for-decision-trees/#:~:text=Python%20implementation%20of%20a%20decision%20tree%20using%20CHAID,%23%20test_instance%20%3D%20%5B%27sunny%27%2C%27hot%27%2C%27high%27%2C%27weak%27%2C%27no%27%5D%20test_instance%20%3D%20data.iloc%20test_instance
#T-SNE

# data = pd.read_csv("globalterrorismdb_0718dist (2).csv",
#     # dtype={4:,6:,31:,33:,61:,62:,63:,76:,79:,90:,92:,94:,96:,114:,115:,121:}
#     )

# data.rename(columns={'iyear':'Year','imonth':'Month','iday':'Day','country_txt':'Country','region_txt':'Region','attacktype1_txt':'AttackType','target1':'Target','nkill':'Killed','nwound':'Wounded','summary':'Summary','gname':'Group','targtype1_txt':'Target_type','weaptype1_txt':'Weapon_type','motive':'Motive'},inplace=True)
# data=data[['eventid','Year','Month','Day','Country','Region','city','latitude','longitude','AttackType','Killed','Wounded','Target','Summary','Group','Target_type','Weapon_type','Motive']]
# data['casualities']=data['Killed']+data['Wounded']

# def decade_stacked_plot(data,value,index,title_txt,num = 20):
#         temp_bar = pd.pivot_table(data, values=value, index=[index],
#                         columns=['Year'], aggfunc='count').fillna(0)

#         temp_bar = temp_bar.loc[data[index].value_counts().iloc[:num].index]
#         i = 0
#         for decade in ['70s','80s','90s','00s']:
#             temp_bar[decade] = temp_bar[temp_bar.columns[i]]
#             i+=1
#             for x in range(1,10):
#                 temp_bar[decade] += temp_bar[temp_bar.columns[i]]
#                 i+=1
        
        
#         temp_bar['10s'] = temp_bar[temp_bar.columns[i]]
#         i+=1

#         for x in range(1,8):
#                 temp_bar['10s'] += temp_bar[temp_bar.columns[i]]
#                 i+=1

#         temp_bar=temp_bar[['70s','80s','90s','00s','10s']]

#         fig, ax = plt.subplots(figsize= (5,10))
#         ax.bar(x=temp_bar.index,
#                 height = temp_bar[temp_bar.columns[0]],
#                 label=temp_bar.columns[0])
        
#         bottom_col = [temp_bar.columns[0]]
#         for year in range(1,len(temp_bar.columns)):
#             ax.bar(x=temp_bar.index,
#                 height = temp_bar[temp_bar.columns[year]],
#                 bottom = temp_bar[bottom_col].sum(axis=1),
#                 label=temp_bar.columns[year])
#             bottom_col.append(temp_bar.columns[year])

#         ax.legend()
#         ax.set_xticklabels(temp_bar.index, rotation=90)
#         ax.set_title(title_txt)
#         st.pyplot(fig)


# decade_stacked_plot(data,'Month','Group','Terrorists Groups responsible for most attacks',num = 10)

# col1, col2 = st.columns(2)

# with col1:
#     decade_stacked_plot(data,'Month','AttackType','Methods of Attack',num = 10)# Break This into those commited by Unknown vs known

# with col2:
#     decade_stacked_plot(data,'Month','Target_type','Terrorist Targets',num = 10)# Break This into those commited by Unknown vs known