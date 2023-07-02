# Notes
# Right screen table is based on simple interest
# Left screen dream ctc calculator is based on compound interest so both might not match

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
st.header('Calculate Increments on your Current Salary')
ctc_old=st.number_input('Select your CTC ( 21 Lakhs selected by default )',value=2100000,step=100000,help='Based on your entered salary, you will get the table of hikes with the gaps of 5%',format='%u')

hike = list(range(5, 105, 5))
hike_perc=[ str(i)+str('%') for i in hike]
new_salary = [float(ctc_old) + ((hike[i]/100) * float(ctc_old)) for i in range(len(hike))]

# Creating the dataframe
df = pd.DataFrame({'Hike %': hike_perc, 'New Salary': new_salary})

# Formatting the columns
df['Hike %']=[str(i)+' ⭐️' if i=='50%' or i=='100%' else i for i in df['Hike %']]
df['New Salary']= [currency(i) for i in df['New Salary']]

df1={'Hike':[5,10],'Salary':[200,400]}
# Showing Table on Screen
st.table(df)

st.markdown('---')
st.header('Your Salary Projections')
ctc1=st.number_input("Enter your Current CTC",value=2100000,step=100000)
avg_hike1=st.number_input("Enter your annual Increment",value=20,step=5)
btn11=st.button('Generate Graph')
if btn11 and avg_hike1: 
    # Bar Chart starts
    years = [2023, 2024, 2025]
    salaries = [ctc1]
    for i in range(1, len(years)):
            previous_salary = salaries[i - 1]
            new_salary = previous_salary + ((20/100) * previous_salary)
            salaries.append(new_salary)
    df = pd.DataFrame({'Year': years, 'Salary': salaries})
    st.bar_chart(df.set_index('Year'))
#st.bar_chart(df1,x='Hike',y='Salary')
# Bar Chart ends

# Initialize session state
# By default, streamlit rerun everytime button is pressed
if "load_state" not in st.session_state:
    st.session_state.load_state=False

# Sidebar
with st.sidebar:
    st.info("Hike Calculator")
    ctc_new=st.text_input("Enter your New CTC",help='Enter Salary without commas and symbols')
    btn=st.button('Calculate Hike %')

# Keep the session of button active 
    if btn or st.session_state.load_state:
        st.session_state.load_state=True
        hike_num=round(((float(ctc_new)-float(ctc_old))/float(ctc_old))*100,3)
        hike='➡️ You got '+ str(hike_num)+'%' + ' hike 🥳'
        st.write(hike)
        negotiation_header='If you do Negotiation Successful,'
        ten_perc_more=float(ctc_old)+(((10+hike_num)/100)*float(ctc_old))
        hike_new='10% more will be '+ currency(str(ten_perc_more))
        full_hike_msg=negotiation_header+  '  \n' +hike_new
        st.success(full_hike_msg)
    # Steps to reach goal
    st.markdown("""<hr style="height:1px;border:none;color:#808080;background-color:#808080;" /> """, unsafe_allow_html=True)
    st.info("Dream CTC Tracker")
    dream_ctc=st.number_input("Enter your Dream CTC",value=5000000,step=100000)
    avg_increment=st.number_input("Enter your average annual Increment",value=15,step=5)
    time=np.log10((dream_ctc/ctc_old))/np.log10(1+(avg_increment/100))
    msg="It will take " + str(round(time,2)) + " years/increments to reach the goal"
    btn2=st.button('Calculate years needed')
    if btn2:
            st.warning(msg)
# Footer
st.markdown('---')
st.markdown('Made with :heart: by [Sahil Choudhary](https://www.sahilchoudhary.ml/)')
