# Import Libraries
import pandas as pd
import numpy as np
import streamlit as st
from io import BytesIO
from babel.numbers import format_currency

# Page Settings
st.set_page_config(page_title='Increment Calculator',page_icon=':smile:')

# CSS
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Add commas and Rupee sign
def currency(i):
    new_string=format_currency(i, 'INR', locale='en_IN').replace(u'\xa0', u' ')
    new_string=new_string.replace('.00', '') 
    return new_string

# Generate Table of increment
#ctc_old=2100000
st.success('Calculate Increments based on your Current Salary')
ctc_old=st.number_input('Select your CTC ( 21 Lakhs selected by default )',value=2100000,step=100000,help='Based on your entered salary, you will get the table of hikes with the gaps of 5%',format='%u')

hike = list(range(5, 145, 5))
hike_perc=[ str(i)+str('%') for i in hike]
new_salary = [float(ctc_old) + ((hike[i]/100) * float(ctc_old)) for i in range(len(hike))]

# Creating the dataframe
df = pd.DataFrame({'Hike %': hike_perc, 'New Salary': new_salary})

# Formatting the columns
df['Hike %']=[str(i)+' ⭐️' if i=='50%' or i=='100%' else i for i in df['Hike %']]
df['New Salary']= [currency(i) for i in df['New Salary']]

# Showing Table on Screen
st.table(df)

# Sidebar
with st.sidebar:
    st.info("Got New Salary?")
    ctc_new=st.text_input("Enter your New CTC",help='Enter Number without commas and symbols')
    btn=st.button('Calculate Hike %')

    if btn:
        hike=round(((float(ctc_new)-float(ctc_old))/float(ctc_old))*100,1)
        hike='➡️ You got '+ str(hike)+'%' + ' hike'
        st.write(hike)
        st.success('If you do Negotiation Successful')
        ten_perc_more=float(ctc_new)+((10/100)*float(ctc_new))
        hike_new='➡️ 10 % more will be '+ currency(str(ten_perc_more))
        st.write(hike_new)

# Footer
st.markdown('---')
st.markdown('Made with :heart: by [Sahil Choudhary](https://www.sahilchoudhary.ml/)')
