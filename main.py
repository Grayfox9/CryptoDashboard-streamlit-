#Importing libraries

import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import webbrowser

from streamlit.elements import button

linkedin = 'https://www.linkedin.com/in/ingmarorta/'
github = 'https://github.com/Grayfox9/CryptoDashboard-streamlit-'

#Page line
st.set_page_config(page_icon="📈", page_title= "Proyecto Individual 03: CryptoDashboard")

#----------------------------------------------------------------------------
#Setting sidebar
with st.sidebar:
        pages = st.radio(
                "Contenido",
                ('1. Introduction', '2. Crypto Prices','3. CryptoDashboard')
        )
#----------------------------------------------------------------------------

# PART 1 - I INTRODUCTION

if pages == '1. Introduction':
        
        st.title("📈 Proyecto Individual 03: Introduction 📈")


        st.image("https://bancomparamx-static-2.s3.amazonaws.com/images/tmptmpm_8lltka.2e16d0ba.fill-800x450.png")

        st.subheader('**¿Qué es una criptomoneda?**')
        st.markdown('Una criptomoneda, como el bitcoin, es una moneda completamente digital cuyos registros se mantienen en un sistema que utiliza criptografía y cadenas de datos. Es decir, que a esta moneda no la regula ninguna entidad financiera ni ninguna institución en particular.')


        st.subheader('¿Por qué son importantes las criptomonedas?')
        st.markdown('Porque son formas de intercambiar bienes y servicios y de acumular riqueza que no están reguladas por entidades establecidas, pero que se crearon para intercambiar información y datos digitales.')

        st.subheader('¿De dónde salieron las criptomonedas?')
        st.markdown('En octubre de 2008, un señor llamado Satoshi Nakamoto (una persona anónima) sacó a la luz el primer bitcoin, el cual produjo utilizando la tecnología que hoy se usa para crear cualquier moneda digital, la criptomoneda o el sistema Bitcoin.') 
        st.markdown('En 2009 se hizo la primera transacción con Bitcoin y quedó registrada en la blockchain. Nakamoto la creó como una forma de:')

        st.markdown('->Transferir dinero más rápido entre países.')
        st.markdown('->Reducir el control del gobierno en las transacciones.')
#----------------------------------------------------------------------------

elif pages == '2. Crypto Prices':

        st.title("📈 Proyecto Individual 03: Crypto Prices 📈")

        #----------------------------------------------------------------------------
        #Crypto prices

        st.header("💲 Today most interesting Cryptocurrencies prices by Market Cap 💲")

        #Load market data from FTX API

        cryptprice = requests.get('https://ftx.com/api/markets').json()
        
        #Deleting unnecesary data
        cryptos = pd.DataFrame(cryptprice['result'])
        cryptos.drop(['tokenizedEquity', 'highLeverageFeeExempt', 'postOnly', 'enabled', 'futureType','type','baseCurrency','isEtfMarket','restricted','quoteCurrency','underlying'], axis=1, inplace=True)
        cryptos.drop(['largeOrderThreshold'], axis=1, inplace=True)
        

        btc = cryptos[(cryptos['name'] == 'BTC/USD')]
        eth = cryptos[(cryptos['name'] == 'ETH/USD')]
        sol = cryptos[(cryptos['name'] == 'SOL/USD')]
        dot = cryptos[(cryptos['name'] == 'DOT/USD')]
        matic = cryptos[(cryptos['name'] == 'MATIC/USD')]
        bnb = cryptos[(cryptos['name'] == 'BNB/USD')]
        axs = cryptos[(cryptos['name'] == 'AXS/USD')]
        atom = cryptos[(cryptos['name'] == 'ATOM/USD')]
        uni = cryptos[(cryptos['name'] == 'UNI/USD')]

        cryptodf = pd.concat([btc, eth, sol, dot, matic, bnb, axs, atom, uni])
        


        # Creating columns

        col1, col2, col3 = st.columns(3)

        # Placing data in metrics and columns

        for i in range(len(cryptodf)):

                if i < 3:
                        with col1:
                                st.metric(cryptodf.iloc[i]['name'], cryptodf.iloc[i]['price'], round(cryptodf.iloc[i]['change24h'], 3))
                if 2 < i < 6:
                        with col2:
                                st.metric(cryptodf.iloc[i]['name'], cryptodf.iloc[i]['price'], round(cryptodf.iloc[i]['change24h'], 3))
                if i > 5:
                        with col3:
                                st.metric(cryptodf.iloc[i]['name'], cryptodf.iloc[i]['price'], round(cryptodf.iloc[i]['change24h'], 3))



        #Adding selected cryptos dataframe

        st.dataframe(cryptodf)




#----------------------------------------------------------------------------

#PART 2 - CRYPTO DASHBOARD



elif pages == '3. CryptoDashboard':

        st.title("📈 Proyecto Individual 03: CryptoDashboard 📈")




        st.markdown(
        """
        Dashboard pulling price data from [FTX/api](https://docs.ftx.com/#rest-api)
        """
        )
        

        #----------------------------------------------------------------------------

        #Choosing cryptocurrency box

        st.header("📊 Choose a crypto to compare with USD 📊")

        cryp_opt = st.selectbox("", ('BTC', 'ETH', 'SOL', 'DOT','MATIC', 'BNB', 'AXS', 'ATOM', 'UNI'))

        #----------------------------------------------------------------------------

        #

        #----------------------------------------------------------------------------


        #Acquiring Historical cryptocurrencies prices

        historical = requests.get(f'https://ftx.com/api/markets/{cryp_opt}/USD/candles?resolution=86400&start_time=2592000').json()

        historical = pd.DataFrame(historical['result'])
        historical.drop(['startTime'], axis = 1, inplace=True)
        

        #Aplying Simple Moving Average (of 10 and 20 days) to data

        historical['time'] = pd.to_datetime(historical['time'], unit='ms')
        historical.set_index('time', inplace=True)

        



        #----------------------------------------------------------------------------
        #Sidebar options

        days_to_plot = st.sidebar.slider(
                'Days to plot',
                min_value= 1,
                max_value= 300,
                value= 120
        )

        ma1 = st.sidebar.number_input(
                'Moving Average 1 (days)',
                value= 10,
                min_value= 1,
                max_value= 120,
                step= 1,
        )

        ma2 = st.sidebar.number_input(
                'Moving Average 2 (days)',
                value= 20,
                min_value= 1,
                max_value= 120,
                step= 1,
        )
        

        #Adding the moving averages
        historical[f'{ma1}_SMA'] = historical.close.rolling(ma1).mean()
        historical[f'{ma2}_SMA'] = historical.close.rolling(ma2).mean()
        historical = historical[-days_to_plot:]
        

        # Plotly Candlestick chart

                        
        fig = make_subplots(
                rows = 2,
                cols = 1,
                shared_xaxes= True,
                vertical_spacing= 0.1,
                subplot_titles= (f'{cryp_opt}/USD Stock Price', 'Volume chart'),
                row_width = [0.3,1]
        )

        fig.add_trace(
                go.Candlestick(
                x = historical.index,
                open = historical['open'], 
                high = historical['high'],
                low = historical['low'],
                close = historical['close'],
                name = f'{cryp_opt}/USD'
                ),
                row = 1,
                col = 1,
        )

        fig.add_trace(
                go.Line(x =historical.index, y =historical[f'{ma1}_SMA'], line=dict(color='green', width=0.7), name=f'{ma1} SMA')
        )

        fig.add_trace(
                go.Line(x =historical.index, y =historical[f'{ma2}_SMA'], line=dict(color='red', width=0.7), name=f'{ma2} SMA')
        )        
        
        fig.add_trace(
                go.Bar(x = historical.index, y = historical['volume'], name='Volume'),
                row = 2,
                col = 1,

        )



        fig['layout']['xaxis2']['title'] = 'Date'
        fig['layout']['yaxis']['title'] = 'Price'
        fig['layout']['yaxis2']['title'] = 'Volume'
        
        
        fig.update_xaxes(
                rangeslider_visible = False
        )


        
        st.plotly_chart(fig)


        



        #----------------------------------------------------------------------------

        #Crypto/USD converter (calculator)

        st.header(f"💸 {cryp_opt} to USD converter💸")


        spec_market = requests.get(f'https://ftx.com/api/markets/{cryp_opt}/USD').json()
        lastprice = spec_market['result']['ask']

        #Putting a selection box with options of conversion

        crypt_conversion = st.selectbox("Select an option of conversion:", (f'Convert {cryp_opt} to USD', f'Convert USD to {cryp_opt}'))

        if crypt_conversion == f'Convert {cryp_opt} to USD':

                col1, col2 = st.columns(2)

                with col1:
                        calc_input = st.number_input(f'Input amount of {cryp_opt} to convert to USD')
                        st.write(f'Your input of {cryp_opt} is ', calc_input)
                

                with col2:
                        st.write('Amount of USD is ', calc_input*lastprice)
        else:
                col1, col2 = st.columns(2)

                with col1:
                        calc_input = st.number_input(f'Input amount of USD to convert to {cryp_opt}')
                st.write('Your input of USD is ', calc_input)
                

                with col2:
                        st.write(f'Amount of {cryp_opt} is ', calc_input/lastprice)

                
        #Adding social network
        st.sidebar.markdown('Check my social media:')
        if st.sidebar.button('LinkedIn'):
                webbrowser.open_new_tab(linkedin)
        elif st.sidebar.button('Github-repo'):
                webbrowser.open_new_tab(github)

        #-------------------------------------------------------------------------------

#else:
        #st.title("📈 Proyecto Individual 03: CryptoConverter 📈")

        #Acquiring historical data

        #spec_market = requests.get(f'https://ftx.com/api/markets/{cryp_opt}/USD').json()
        #lastprice = spec_market['result']['ask']