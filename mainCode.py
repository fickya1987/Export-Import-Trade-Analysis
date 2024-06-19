from unicodedata import name
import numpy as np
import pandas as pd
import streamlit as st
import plotly.graph_objs as go
import chart_studio.plotly as py
from plotly.offline import init_notebook_mode, iplot
from countryinfo import CountryInfo
import folium
from streamlit_folium import folium_static
import pycountry
import plotly.express as px
from footer_utils import image, link, layout, footer
@st.cache(allow_output_mutation=True,suppress_st_warning=True)
def Pageviews():
    return []
#animations--------------------------------------------------------------------------------------
from streamlit_lottie import st_lottie
import json
import requests 
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_hello = load_lottieurl("https://assets3.lottiefiles.com/private_files/lf30_ahlkj7sh.json")
st_lottie(
    lottie_hello,
    speed=0.8,
    reverse=False,
    loop=True,
    quality="high", # medium ; high
    renderer="svg", # canvas
    height=400,
    width=None,
    key="2",
)
# animations--------------------------------------------------------------------------------------
#Country Names------------------------------------------------------------------------------------
country_name = ['Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
       'Anguilla', 'Antigua and Barbuda', 'Argentina', 'Armenia', 'Aruba',
       'Australia', 'Austria', 'Azerbaijan', 'Bahamas', 'Bahrain',
       'Bangladesh', 'Barbados', 'Belarus', 'Belgium',
       'Belgium-Luxembourg', 'Belize', 'Benin', 'Bermuda', 'Bhutan',
       'Bolivia (Plurinational State of)', 'Bosnia Herzegovina',
       'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria',
       'Burkina Faso', 'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon',
       'Canada', 'Central African Rep.', 'Chad', 'Chile', 'China',
       'China, Hong Kong SAR', 'China, Macao SAR', 'Colombia', 'Comoros',
       'Congo', 'Cook Isds', 'Costa Rica', "Côte d'Ivoire", 'Croatia',
       'Cuba', 'Cyprus', 'Czech Rep.', 'Denmark', 'Djibouti', 'Dominica',
       'Dominican Rep.', 'Ecuador', 'Egypt', 'El Salvador', 'Eritrea',
       'Estonia', 'Ethiopia', 'EU-28', 'Faeroe Isds', 'Fiji', 'Finland',
       'Fmr Fed. Rep. of Germany', 'Fmr Sudan', 'France', 'French Guiana',
       'French Polynesia', 'FS Micronesia', 'Gabon', 'Gambia', 'Georgia',
       'Germany', 'Ghana', 'Greece', 'Greenland', 'Grenada', 'Guadeloupe',
       'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana', 'Haiti',
       'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
       'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan',
       'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan',
       "Lao People's Dem. Rep.", 'Latvia', 'Lebanon', 'Lesotho', 'Libya',
       'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia',
       'Maldives', 'Mali', 'Malta', 'Martinique', 'Mauritania',
       'Mauritius', 'Mayotte', 'Mexico', 'Mongolia', 'Montenegro',
       'Montserrat', 'Morocco', 'Mozambique', 'Myanmar', 'Namibia',
       'Nepal', 'Neth. Antilles', 'Netherlands', 'New Caledonia',
       'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway', 'Oman',
       'Other Asia, nes', 'Pakistan', 'Palau', 'Panama',
       'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland',
       'Portugal', 'Qatar', 'Rep. of Korea', 'Rep. of Moldova', 'Réunion',
       'Romania', 'Russian Federation', 'Rwanda', 'Saint Kitts and Nevis',
       'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa',
       'Sao Tome and Principe', 'Saudi Arabia', 'Senegal', 'Serbia',
       'Serbia and Montenegro', 'Seychelles', 'Sierra Leone', 'Singapore',
       'Slovakia', 'Slovenia', 'So. African Customs Union',
       'Solomon Isds', 'South Africa', 'Spain', 'Sri Lanka',
       'State of Palestine', 'Sudan', 'Suriname', 'Swaziland', 'Sweden',
       'Switzerland', 'Syria', 'TFYR of Macedonia', 'Thailand',
       'Timor-Leste', 'Togo', 'Tonga', 'Trinidad and Tobago', 'Tunisia',
       'Turkey', 'Turkmenistan', 'Turks and Caicos Isds', 'Uganda',
       'Ukraine', 'United Arab Emirates', 'United Kingdom',
       'United Rep. of Tanzania', 'Uruguay', 'USA', 'Vanuatu',
       'Venezuela', 'Viet Nam', 'Wallis and Futuna Isds', 'Yemen',
       'Zambia', 'Zimbabwe', 'Tuvalu', 'Cayman Isds', 'Tajikistan']
#Country Names------------------------------------------------------------------------------------
#Trade dataset import-----------------------------------------------------------------------------
@st.cache(allow_output_mutation=True,suppress_st_warning=True)
def import_dataset():
    return pd.read_csv("trade.csv") 
world_df = import_dataset()
#Trade dataset import-----------------------------------------------------------------------------
#Country Wise DataSet import----------------------------------------------------------------------
def country_dataset(country_name):
    return world_df[world_df["country_or_area"] == country_name]
#Country Wise DataSet import----------------------------------------------------------------------
#Service One Useful Functions---------------------------------------------------------------------
def import_and_export_graph(country_name):
    input_df = country_dataset(country_name)
    input_df_i = input_df[(input_df.flow == 'Import') & (input_df.comm_code!= 'TOTAL')].groupby(['year'],as_index=False)['trade_usd'].agg('sum')
    
    input_df_e = input_df[(input_df.flow == 'Export') & (input_df.comm_code!= 'TOTAL')].groupby(['year'],as_index=False)['trade_usd'].agg('sum')
    trace1 = go.Bar(
        x = input_df_i.year,
        y = input_df_i.trade_usd,
        name = f"{country_name} Import",
        marker = dict(color = 'rgba(102, 216, 137, 0.8)'),
    )
    trace2 = go.Bar(
        x = input_df_e.year,
        y = input_df_e.trade_usd,
        name = f"{country_name} Export",
        marker = dict(color = 'rgba(224, 148, 215, 0.8)'),
    )
    data = [trace1, trace2]
    layout = {
        'xaxis': {'title': 'Year 1992-2016'},
        'yaxis': {'title': f'Trade of Import & Export in {country_name} (USD)'},
        'barmode': 'group'
    }
    return go.Figure(data = data, layout = layout)
def top_10_commodities_imports_and_export(country_name , type , key):
    input_df = country_dataset(country_name)
    if(len(input_df[(input_df.year==1992) & (input_df.flow== type)])):
        temp_1992 = input_df[(input_df.year==1992) & (input_df.flow== type)].sort_values(by="trade_usd",  ascending=False).iloc[1:11, :]
        country_1992i = temp_1992.sort_values(by="trade_usd",  ascending=True)
        trace_1992 = go.Bar(
                        x = country_1992i.trade_usd,
                        y = country_1992i.commodity,
                        marker = dict(color = 'rgba(152, 213, 245, 0.8)'),
                        orientation = 'h'
        )
        data_1992 = [trace_1992]
        layout_1992 = {
            'yaxis': {'automargin':True,}
        }
        
        temp_2016 = input_df[(input_df.year==2016) & (input_df.flow==type)].sort_values(by="trade_usd",  ascending=False).iloc[1:11, :]
        country_2016i = temp_2016.sort_values(by="trade_usd",  ascending=True)
        trace1 = go.Bar(
                        x = country_2016i.trade_usd,
                        y = country_2016i.commodity.tolist(),
                        marker = dict(color = 'rgba(249, 205, 190, 0.8)'),
                        orientation = 'h'
        )
        data_2016 = [trace1]
        layout_2016 = {
            'yaxis': {'automargin':True,}
        }
        return [go.Figure(data = data_1992, layout = layout_1992),go.Figure(data = data_2016, layout = layout_2016)]
    else:
        lottie_hello = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_h81pyyr2.json")
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # medium ; high
            renderer="svg", # canvas
            height=400,
            width=None,
            key=key,
        )
        return 0
    
def top_10_commodities(country_name):
    input_df = country_dataset(country_name)
    input_df = input_df.groupby("commodity")[["trade_usd"]].agg("sum").sort_values(by="trade_usd" , ascending=False).iloc[1:11,:][["trade_usd"]]
    input_df.sort_values(by="trade_usd",ascending = True , inplace =  True)
    trace_comm = go.Bar(
                x = input_df.trade_usd,
                y = input_df.index,
                marker = dict(color = 'rgba(249, 205, 190, 0.8)'),
                orientation = 'h'
            )
    data_comm = [trace_comm]
    layout_comm = {
        'xaxis': {'title': 'Trade in USD'},
        'yaxis': {'automargin':True,}
    }
    return go.Figure(data = data_comm, layout = layout_comm)
def country_vs_world(country_name):
    input_df = country_dataset(country_name)
    country_trade = input_df[(input_df.comm_code != 'TOTAL')].groupby("year",as_index = False)['trade_usd'].agg('sum')
    wd_trade = world_df[(world_df['year']>1991)&(world_df['comm_code']!='TOTAL')].groupby('year',as_index=False)['trade_usd'].agg('sum')
    trace0 = {
    'x':country_trade.year,
    'y':country_trade.trade_usd,
    'name':f'{country_name}',
    'type':'bar',
        'marker': {'color':'rgba(129, 239, 208, 0.8)'}
    }
    trace1 = {
    'x':wd_trade.year,
    'y':wd_trade.trade_usd,
    'name':'World',
    'type':'bar',
        'marker': {'color':'rgba(255, 171, 202, 0.8)'}
    }
    data = [trace0 , trace1]
    layout={
    'xaxis': {'title': 'Year 1992-2016'},
    'yaxis': {'title': 'Value of Trade in USD'},
    'barmode': 'relative'
    }
    trace3 = go.Scatter(
        x = country_trade.year,
        y = (country_trade.trade_usd/wd_trade.trade_usd)*100,
        mode = "lines+markers",
        name = f"Ratio of {country_name}/World",
        marker = dict(color = 'rgba(245, 150, 104, 0.8)')
    )
    data2 = [trace3]
    layout2 = dict(xaxis= dict(title= 'Year 1992-2016',ticklen= 5,zeroline= False),yaxis = {'title': 'Percentage (%)'})
    return [go.Figure(data= data , layout = layout) , dict(data = data2, layout = layout2)]
def country_vs_world_in_weights(country_name):
    input_df = country_dataset(country_name)
    cn_ie = input_df[input_df.comm_code!= 'TOTAL'].groupby(['year'],as_index=False)['weight_kg'].agg('sum')
    wd_ie = world_df[(world_df.year >1991) & (world_df.comm_code!= 'TOTAL')].groupby(['year'],as_index=False)['weight_kg'].agg('sum')
    trace1 = go.Bar(
                    x = wd_ie.year,
                    y = wd_ie.weight_kg,
                    name = "World",
                    marker = dict(color = 'rgba(104, 206, 245, 0.8)'),
    )
    trace2 = go.Bar(
                    x = cn_ie.year,
                    y = cn_ie.weight_kg,
                    name = f"{country_name}",
                    marker = dict(color = 'rgba(255, 248, 12, 0.8)'),
    )
    data = [trace1, trace2]
    layout = {
        'xaxis': {'title': 'Year 1992-2016'},
        'yaxis': {'title': 'Import & Export in Weight (kg)'},
        'barmode': 'group'
    }
    trace3 = go.Scatter(
                        x = cn_ie.year,
                        y = cn_ie.weight_kg/wd_ie.weight_kg*100,
                        mode = "lines+markers",
                        name = "Ratio of China/World",
                        marker = dict(color = 'rgba(84, 222, 90, 0.8)')
    )
    data2 = [trace3]
    layout2 = dict(
                xaxis= dict(title= 'Year 1992-2016',ticklen= 5,zeroline= False),
                yaxis = {'title': 'Percentage (%)'}
    )
    return [go.Figure(data = data, layout = layout),dict(data = data2, layout = layout2)]
def country_top_3_import_exported_commodities(country_name , type):
    input_df = country_dataset(country_name)
    top_3_comm_lst = list(input_df[(input_df["commodity"] !="ALL COMMODITIES")&(input_df["flow"] ==type)][["trade_usd" , "commodity"]].groupby("commodity").agg("sum").sort_values(by="trade_usd" , ascending=False)[:3].index)
    ele_one=input_df[(input_df["commodity"] == top_3_comm_lst[0])&(input_df["year"] >1991)&(input_df["flow"] == type)].groupby("year")[["trade_usd"]].agg("sum")
    ele_two =input_df[(input_df["commodity"] == top_3_comm_lst[1])&(input_df["year"] >1991)&(input_df["flow"] == type)].groupby("year")[["trade_usd"]].agg("sum")
    ele_three = input_df[(input_df["commodity"] == top_3_comm_lst[2])&(input_df["year"] >1991)&(input_df["flow"] == type)].groupby("year")[["trade_usd"]].agg("sum")
    trace1 = go.Scatter(
        x = ele_one.index,
        y = ele_one.trade_usd,
        mode = "lines+markers",
        name = f"{top_3_comm_lst[0]}",
        marker = dict(color = 'rgba(255, 196, 100, 0.8)')
    )
    trace2 = go.Scatter(
        x = ele_two.index,
        y = ele_two.trade_usd,
        mode = "lines+markers",
        name = f"{top_3_comm_lst[1]}",
        marker = dict(color = 'rgba(241, 130, 133, 0.8)')
    )
    trace3 = go.Scatter(
        x = ele_three.index,
        y = ele_three.trade_usd,
        mode = "lines+markers",
        name = f"{top_3_comm_lst[2]}",
        marker = dict(color = 'rgba(130, 241, 140, 0.8)')
    )
    data = [trace1, trace2, trace3]
    layout = dict(
                xaxis= dict(ticklen= 5,zeroline= False),
                yaxis = {'title': f'{type} trade value(USD)'}
    )
    return dict(data = data, layout = layout)
#Service One Useful Functions---------------------------------------------------------------------
#Service Two Useful Functions---------------------------------------------------------------------
def c1_vs_c2_exports(c1 , c2 , type):
    c1_df = country_dataset(c1)
    c2_df = country_dataset(c2)
    trade_per_year_c1 = c1_df[(c1_df["flow"] == type) &(c1_df["year"]>1991)].groupby("year")[["trade_usd"]].agg("sum")
    trade_per_year_c2 = c2_df[(c2_df["flow"] == type)&(c2_df["year"]>1991)].groupby("year")[["trade_usd"]].agg("sum")
    trace3 = go.Scatter(
                        x = trade_per_year_c1.index,
                        y = trade_per_year_c1.trade_usd,
                        mode = "lines+markers",
                        name = f"{c1}",
                        marker = dict(color = 'rgba(104, 206, 245, 0.8)')
    )
    trace4 = go.Scatter(
                        x = trade_per_year_c2.index,
                        y = trade_per_year_c2.trade_usd,
                        mode = "lines+markers",
                        name = f"{c2}",
                        marker = dict(color = 'rgba(84, 222, 90, 0.8)')
    )
    data2 = [trace3 , trace4]
    layout2 = dict(
                xaxis= dict(title= 'Year 1992-2016',ticklen= 5,zeroline= False),
                yaxis = {'title': 'Trade USD($)'}
    )
    return dict(data = data2, layout = layout2)
def overall_c1_vs_c2_export(c1 , c2):
    c1_df = country_dataset(c1)
    c2_df = country_dataset(c2)
    trade_per_year_c1 = c1_df.groupby("year")[["trade_usd"]].agg("sum")
    trade_per_year_c2 = c2_df.groupby("year")[["trade_usd"]].agg("sum")
    trace0 = {
        'x':trade_per_year_c1.index,
        'y':trade_per_year_c1.trade_usd,
        'name': c1,
        'type':'bar',
        'marker': {'color':'rgba(129, 239, 208, 0.8)'}
    }
    trace1 = {
        'x':trade_per_year_c2.index,
        'y':trade_per_year_c2.trade_usd,
        'name':c2,
        'type':'bar',
        'marker': {'color':'rgba(255, 171, 202, 0.8)'}
    }
    data = [trace0 , trace1]
    layout={
        'xaxis': {'title': 'Year 1992-2016'},
        'yaxis': {'title': 'Value of Trade in USD'},
        'barmode': 'relative'
    }
    return go.Figure(data= data , layout = layout)
def top_10_commodities_by_c1_and_c2(c1 , c2 ,type , key_lst):
    c1_df = country_dataset(c1)
    c2_df = country_dataset(c2)
    lst_result = []
    if(len(c1_df[(c1_df.year==1992) & (c1_df.flow== type)]) != 0):
        temp_c1 = c1_df[(c1_df.year==1992) & (c1_df.flow==type)].sort_values(by="trade_usd",  ascending=False).iloc[1:11, :]
        c1_1992i = temp_c1.sort_values(by="trade_usd",  ascending=True)
        trace1 = go.Bar(
                        x = c1_1992i.trade_usd,
                        y = c1_1992i.commodity,
                        marker = dict(color = 'rgba(152, 213, 245, 0.8)'),
                        orientation = 'h'
        )
        data1 = [trace1]
        layout1 = {
        'xaxis': {'title': 'Trade in USD'},
        'yaxis': {'automargin':True,}
        }
        lst_result.append(go.Figure(data = data1, layout = layout1))
    else:
        lst_result.append(0)
    if(len(c2_df[(c2_df.year==1992) & (c2_df.flow== type)]) != 0):
        temp_c2 = c2_df[(c2_df.year==1992) & (c2_df.flow==type)].sort_values(by="trade_usd",  ascending=False).iloc[1:11, :]
        c2_1992i = temp_c2.sort_values(by="trade_usd",  ascending=True)
        trace2 = go.Bar(
                        x = c2_1992i.trade_usd,
                        y = c2_1992i.commodity,
                        marker = dict(color='rgba(255, 171, 202, 0.8)'),
                        orientation = 'h'
        )
        data2 = [trace2]
        layout2 = {
            'xaxis': {'title': 'Trade in USD'},
            'yaxis': {'automargin':True,}
        }
        lst_result.append(go.Figure(data = data2, layout = layout2))
    else:
        lst_result.append(0)
    return lst_result
def pecentage_of_c1_and_c2(c1 ,c2):
    c1_df = country_dataset(c1)
    c2_df = country_dataset(c2)
    c1_trade = c1_df[(c1_df.comm_code != 'TOTAL')&(c1_df.year>1991)].groupby("year",as_index = False)['trade_usd'].agg('sum')
    c2_trade = c2_df[(c2_df.comm_code != 'TOTAL')&(c2_df.year>1991)].groupby("year",as_index = False)['trade_usd'].agg('sum')
    wd__trade = world_df[(world_df['year']>1991)&(world_df['comm_code']!='TOTAL')].groupby('year',as_index=False)['trade_usd'].agg('sum')
    trace3 = go.Scatter(
                        x = c1_trade.year,
                        y = c1_trade.trade_usd/wd__trade.trade_usd*100,
                        mode = "lines+markers",
                        name = f"{c1}/World",
                        marker = dict(color = 'rgba(245, 150, 104, 0.8)')
    )
    trace4 = go.Scatter(
                        x = c2_trade.year,
                        y = c2_trade.trade_usd/wd__trade.trade_usd*100,
                        mode = "lines+markers",
                        name = f"{c2}/World",
                        marker = dict(color = 'rgba(129, 239, 208, 0.8)')
    )
    data2 = [trace3 , trace4]
    layout2 = dict(title = f'Percentage of {c1} , {c2} Trade in World Trade (%)',
                xaxis= dict(title= 'Year 1992-2016',ticklen=5 ,zeroline= False),
                yaxis = {'title': 'Percentage (%)'}
    )
    return  dict(data = data2, layout = layout2)
#Service Two Useful Functions---------------------------------------------------------------------
#Front Page Input-----------------------------------------------------------------------------------------
service_input = st.selectbox("Select Services",["","Countrywise Trade Analysis","Trade Comparison Of Two Countries"])
#Front Page Input-----------------------------------------------------------------------------------------
#Front Page Input input check-----------------------------------------------------------------------------
if service_input == "Countrywise Trade Analysis":
    country_input = st.sidebar.selectbox("Select a Country",[""]+country_name)
    choice_radio = st.sidebar.radio("What Are You Willing To See",["Data Visualisation","About Country"])
    if(country_input and choice_radio == "Data Visualisation"):
        st.title(f"{country_input} Trade Analysis")
        #1
        st.text("")
        st.text("")
        st.text("")
        st.subheader(f"Import And Export In {country_input} from 1992 - 2016")
        st.plotly_chart(import_and_export_graph(country_input))
        #2
        st.subheader(f"Top 10 Commodity Imported By  {country_input} In 1992")
        import_commodity_1992_2016 = top_10_commodities_imports_and_export(country_input , "Import" , 3)
        if(import_commodity_1992_2016):
            st.plotly_chart(import_commodity_1992_2016[0])
            st.subheader(f"Top 10 Commodity Imported By  {country_input} In 2016")
            st.plotly_chart(import_commodity_1992_2016[1])
        #3
        st.subheader(f"{country_input}'s Top 3 Imported Commodities")
        st.plotly_chart(country_top_3_import_exported_commodities(country_input , "Export"))
        st.subheader(f"{country_input}'s Top 3 Exported Commodities")
        st.plotly_chart(country_top_3_import_exported_commodities(country_input , "Import"))
        #4
        st.subheader(f"{country_input}'s Top 10 Traded Commodities Values")
        st.plotly_chart(top_10_commodities(country_input))
        #5
        st.subheader(f"Top 10 Commodity Exported By  {country_input} In 1992")
        export_commodity_1992_2016 = top_10_commodities_imports_and_export(country_input , "Export",4)
        if(import_commodity_1992_2016):
            st.plotly_chart(export_commodity_1992_2016[1])
            st.subheader(f"Top 10 Commodity Exported By  {country_input} In 2016")
            st.plotly_chart(export_commodity_1992_2016[0])
        #6
        st.subheader(f"World vs {country_input} : Value Of Trade")
        c_vs_w = country_vs_world(country_input)
        st.plotly_chart(c_vs_w[0])
        st.subheader(f"Contribution of {country_input} in World Trade")
        st.plotly_chart(c_vs_w[1])
        #7
        st.subheader(f"World vs {country_input} : Import And Export In Weights")
        c_Vs_w_weights= country_vs_world_in_weights(country_input)
        st.plotly_chart(c_Vs_w_weights[0])
        st.subheader(f"World vs {country_input} (%) Of Trade")
        st.plotly_chart(c_Vs_w_weights[1])
        @st.cache(allow_output_mutation=True)
        def Pageviews():
            return []
        pageviews=[]
        pageviews.append('dummy')
        pg_views = len(pageviews)
        footer(pg_views)
    elif(country_input and choice_radio == "About Country"):
        st.title(f"About {country_input}")
        st.text("")
        st.text("")
        st.text("")
        country = CountryInfo(country_input)
        with st.expander(f"{country_input}'s Area"):
            st.write(country.info()["area"])
        with st.expander(f"{country_input}'s Neighbouring Countries"):
            for i in range(0,len(country.info()["borders"])):
                converted_name = pycountry.countries.get(alpha_3=country.info()["borders"][i]).name
                st.write(f"{i+1} : {converted_name}")
        with st.expander(f"{country_input}'s capital"):
            capital = country.info()["capital"]
            st.write(capital)
        with st.expander(f"{capital}'s  Location"):
            df = pd.DataFrame(pd.Series({"lat": country.info()["capital_latlng"][0],"lon":country.info()["capital_latlng"][1]})).T
            st.map(df,zoom=5)
        with st.expander(f"{country_input}'s  Location"):
            df = pd.DataFrame(pd.Series({"lat": country.info()["latlng"][0],"lon":country.info()["latlng"][1]})).T
            st.map(df , zoom= 3)
        with st.expander(f"{country_input}'s Currency"):
            st.write(country.info()["currencies"][0])
            
        with st.expander(f"{country_input}'s population"):
            st.write(country.info()["population"])

        with st.expander(f"{country_input}'s Provinces"):
            for i in range(0,len(country.info()["provinces"])):
                name = country.info()["provinces"][i]
                st.write(f"{i+1} : {name}")
        with st.expander(f"Region"):
            st.write(country.info()["region"])
            
        with st.expander(f"Timezone"):
            st.write(country.info()["timezones"][0])
    else:
        st.title("👈Please Select A Country")
    @st.cache(allow_output_mutation=True)
    def Pageviews():
        return []
    pageviews=[]
    pageviews.append('dummy')
    pg_views = len(pageviews)
    footer(pg_views)
elif service_input == "Trade Comparison Of Two Countries":
    country_input = st.sidebar.multiselect("Select Any Two Countries",country_name)
    if(len(country_input)==2):
        st.title("Trade Comparison Of Two Countries")
        c1 = country_input[0]
        c2 = country_input[1]
        st.write("")
        st.write("")
        st.write("")
        st.subheader(f'{c1} vs {c2} Export Graph')
        st.plotly_chart(c1_vs_c2_exports(c1 , c2 ,"Export"))
        st.subheader(f'{c1} vs {c2} Import Graph')
        st.plotly_chart(c1_vs_c2_exports(c1 , c2 ,"Import"))
        st.subheader(f'{c1} vs {c2} Trade')
        st.plotly_chart(overall_c1_vs_c2_export(c1 , c2))
        var_1 = top_10_commodities_by_c1_and_c2(c1 , c2,"Import" , [6,7])
        if(var_1[0]!=0):
            st.subheader(f"Top 10 Commodities in {c1} Import Trade (USD) in 1992")
            st.plotly_chart(var_1[0])
        if(var_1[1]!=0):
            st.subheader(f"Top 10 Commodities in {c2} Import Trade (USD), 1992")
            st.plotly_chart(var_1[1])
        var_2 = top_10_commodities_by_c1_and_c2(c1 , c2,"Export",[8,9])
        if(var_2[0]!=0):
            st.subheader(f"Top 10 Commodities in {c1} Export Trade (USD) in 1992")
            st.plotly_chart(var_2[0])
        if(var_2[1]!=0):
            st.subheader(f"Top 10 Commodities in {c2} Export Trade (USD), 1992")
            st.plotly_chart(var_2[1])
        st.subheader(f"Percentage of {c1} , {c2} Trade in World Trade (%)")
        st.plotly_chart(pecentage_of_c1_and_c2(c1 , c2))
    elif(len(country_input)==1):
        st.title("👈Please Select One More Countries")
    else:
        st.title("👈Please Select Two Countries")
    @st.cache(allow_output_mutation=True)
    def Pageviews():
        return []
    pageviews=[]
    pageviews.append('dummy')
    pg_views = len(pageviews)
    footer(pg_views)
        
else:
    st.title("Data Analysis On Trade")
    st.write("Brief Explaination:")
    col1 , col2 = st.columns(2)
    with col1:
        st.text("This project shows the amount of import\nand export of different countries.\nThe Data Set stores information from 1992\nto 2016 This application also helps \nto compare the trade statistics between\ntwo countries.")
        st.text("Exports are goods that are\nsold in a foreign market, while imports\nare foreign goods that are purchased in\na domestic market. Exports and imports \nare important for the development and \ngrowth of national economies because not \nall countries have the resources and \nskills required to produce certain goods \nand services.")
    with col2:
        # Front page Animation<Start>------------------------------------------------------------------------
        lottie_hello = load_lottieurl("https://assets4.lottiefiles.com/packages/lf20_c7Gl35.json")
        st_lottie(
            lottie_hello,
            speed=1,
            reverse=False,
            loop=True,
            quality="high", # medium ; high
            renderer="svg", # canvas
            height=None,
            width=None,
            key="1",
        )
    @st.cache(allow_output_mutation=True)
    def Pageviews():
        return []
    pageviews=[]
    pageviews.append('dummy')
    pg_views = len(pageviews)
    footer(pg_views)
        # Front page Animation<End>------------------------------------------------------------------------
#Front Page Input input check-----------------------------------------------------------------------------
