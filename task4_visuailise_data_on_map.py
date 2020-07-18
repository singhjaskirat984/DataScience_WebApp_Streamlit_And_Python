import streamlit as st
import pandas as pd
import numpy as np

DATA_URL = ("C:/Users/Jaskirat Singh/Desktop/python programs/Streamlit_coursera/Motor_Vehicle_Collisions_-_Crashes.csv")

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This Application is a Streamlit dashboard that can be used to analyze Motor Vehicle Collisions in NYC")

@st.cache(persist = True) #very important 
def load_data(nrows):
	data = pd.read_csv(DATA_URL,nrows=nrows,parse_dates = [['CRASH DATE','CRASH TIME']])
	data.dropna(subset = ['LATITUDE','LONGITUDE'],inplace = True)
	lowercase = lambda x: str(x).lower()
	data.rename(lowercase,axis = 'columns',inplace = True)
	data.rename(columns={'crash date_crash time':'date/time'},inplace = True)
	data.rename(columns={'number of persons injured' : 'injured_persons'},inplace=True)
	return data

data = load_data(100000)

st.header("Where are the most people injured in NYC??")
injured_people = st.slider("Number of persons injured in vehicle Collisions",0,19)
st.map(data.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any"))


if st.checkbox("Show Raw Data",False):
	st.subheader('Raw Data')
	st.write(data)