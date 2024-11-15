import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Uber pickups in NYC",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': "https://github.com/streamlit/streamlit",
        'About': "# This is a header. This is an *extremely* cool app!"
    }
)

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

if __name__ == "__main__":
    with st.sidebar:
        nrows = st.number_input(label="Enter the number of rows to scan", value=None, placeholder="Type a number...")
    if nrows is not None:
        with st.spinner('Loading data...'):
            df = load_data(nrows)
        st.dataframe(df)

        st.subheader('Number of pickups by hour')
        hist_values = np.histogram(df[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
        st.bar_chart(hist_values)

        # Some number in the range 0-23
        hour_to_filter = st.slider('hour', 0, 23, 17)
        filtered_data = df[df[DATE_COLUMN].dt.hour == hour_to_filter]

        st.subheader('Map of all pickups at %s:00' % hour_to_filter)
        st.map(filtered_data)