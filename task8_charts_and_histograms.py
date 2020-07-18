import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly_express as px


DATA_URL = ("C:/Users/Jaskirat Singh/Desktop/python programs/Streamlit_coursera/Motor_Vehicle_Collisions_-_Crashes.csv")

st.title("Motor Vehicle Collisions in New York City")
st.markdown("This Application is a Streamlit dashboard that can be used to analyze Motor Vehicle Collisions in NYC")

@st.cache(persist = True) #very important 
def load_data(nrows):
	data = pd.read_csv(DATA_URL,nrows=nrows,parse_dates = [['CRASH DATE','CRASH TIME']])
	data.dropna(subset = ['LATITUDE','LONGITUDE'],inplace = True)
	lowercase = lambda x: str(x).lower()
	data.rename(	lowercase,axis = 'columns',inplace = True)
	data.rename(columns={'crash date_crash time':'date/time'},inplace = True)
	data.rename(columns={'number of persons injured' : 'injured_persons'},inplace=True)
	return data

data = load_data(100000)

st.header("Where are the most people injured in NYC??")
injured_people = st.slider("Number of persons injured in vehicle Collisions",0,19)
st.map(data.query("injured_persons >= @injured_people")[["latitude","longitude"]].dropna(how="any"))

st.header("How many Collisions occur during a given time of day")
# hour = st.selectbox("Hour to look at", range(0,24),1)
hour = st.slider("Hour to look at", 0,23)
# hour = st.sidebar.slider("Hour to look at", 0,23)
data = data[data['date/time'].dt.hour == hour]

st.markdown("Vehicle Collisions betwwen %i:00 and %i:00 " % (hour,(hour+1) % 24))
midpoint = (np.average(data['latitude']),np.average(data['longitude']))
st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
    "latitude": midpoint[0],
    "longitude": midpoint[1],
    "zoom": 11,
    "pitch": 50,
    },
    layers=[
    pdk.Layer(
    	"HexagonLayer",
    	data=data[['date/time','latitude','longitude']], 
    	get_position=['longitude','latitude'],
    	radius=100,
    	extruded=True, #makes map 3D
    	pickable=True,
    	elevation_scale=4,
    	elevation_range=[0,1000],
    	),
    ],
))


st.subheader("Breakdown by minute between %i:00 and %i:00 " % (hour,(hour+1) % 24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour+1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute' : range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute','crashes'],height=400)
st.write(fig)

if st.checkbox("Show Raw Data",False):
	st.subheader('Raw Data')
	st.write(data)