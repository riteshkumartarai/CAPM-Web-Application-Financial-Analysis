import streamlit as st 
import pandas as pd
import yfinance as yf
import datetime
import pandas_datareader as web
import CAPM_function

st.set_page_config(page_title="CAPM CALCULATION",page_icon="chart_with_upwards_trend",layout="wide")

st.title("capital Asset Pricing Model")

#geting input from user
col1,col2=st.columns([1,1])
with col1:
    stock_list=st.multiselect("Choose 4 dtocks",('TSLA','AAPL','NFLX','MSFT','MGM','AMZN','NVDA','GOOGL'),['TSLA','AAPL','AMZN','GOOGL'])
with col2:
    year_back=st.number_input("Number of year",1,10)

#downloding data for sp500
try:

    start =datetime.date(datetime.date.today().year-year_back,datetime.date.today().month,datetime.date.today().day) 
    end=datetime.date.today()
    SP500 = web.DataReader('SP500', 'fred', start, end)
    # print(SP500.head(10))
    stock_df=pd.DataFrame()

    for stock in stock_list:
        data=yf.download(stock,period=f'{year_back}y')
        stock_df[f'{stock}']=data['Close']

    stock_df.reset_index(inplace=True)
    SP500.reset_index(inplace=True)
    SP500.columns=['Date','sp500']
    # print(stock_df.dtypes)
    # print(SP500.dtypes)
    stock_df=pd.merge(stock_df,SP500,on='Date',how='inner')

    col1,col2 =st.columns([1,1])
    with col1:
        st.markdown("###DataFrame Head")
        st.dataframe(stock_df.head(),use_container_width=True)
    with col2:
        st.markdown("###Dataframe Tail")    
        st.dataframe(stock_df.tail(),use_container_width=True)
    col1,col2=st.columns([1,1])
    with col1:
        st.markdown("###prince of all stock")
        st.plotly_chart(CAPM_function.interactive_plot(stock_df))
        
    with col2:
        st.markdown("After normalized")
        st.plotly_chart(CAPM_function.interactive_plot(CAPM_function.normalize(stock_df)))   

    stock_df_daily_return=CAPM_function.daily_return(stock_df)   
    print(stock_df_daily_return.head())


    beta={}
    alpha={}

    for i in stock_df_daily_return.columns:
        if i !='Date' and i !='sp500':
            b,a=CAPM_function.calculate_beta(stock_df_daily_return,i)
            beta[i]=b
            alpha[i]=a
    print(beta,alpha)        
    beta_df=pd.DataFrame(columns=['Stock','Beta_values'])
    beta_df['Stock'] =beta.keys()
    beta_df['Beta_values'] = [str(round(i, 2)) for i in beta.values()]


    with col1:
        st.markdown("### Calculated Beta Value")
        st.dataframe(beta_df,use_container_width=True)

    rf= 0
    rm=stock_df_daily_return['sp500'].mean()*252  

    return_df=pd.DataFrame()
    return_value=[]
    for stock,value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)),2)))
    return_df['Stock']=stock_list
    return_df['Return Value'] =return_value 

    with col2:
        st.markdown("###Calculated retun using capm")
        
        st.dataframe(return_df,use_container_width=True)  
except:
    st.write("Please Select Valid input")
            