import streamlit as st
import pandas as pd
import numpy as np
st.title("🎈 My new Streamlit app! Hello")

st.write(
    "This is cool! Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)  # 👈 Download the data
    return df
def transform(df):
    df = df.filter(items=['Lat', 'Lon'])
    df = df.apply(np.sum, axis=0)
    return df

df = load_data("https://github.com/plotly/datasets/raw/master/uber-rides-data1.csv")
st.dataframe(df)
tfed = transform(df)
st.dataframe(tfed)
st.button("Rerun")


@st.cache_data
def add(arr1, arr2):
	return arr1 + arr2



# Check if 'key' already exists in session_state
# If not, then initialize it
if 'key' not in st.session_state:
    st.session_state['key'] = 'value'

# Session State also supports the attribute based syntax
if 'key' not in st.session_state:
    st.session_state.key = 'value'


st.title('Counter Example')
if 'count' not in st.session_state:
    st.session_state.count = 0

increment = st.button('Increment')
if increment:
    st.session_state.count += 1

st.write('Count = ', st.session_state.count)

if "celsius" not in st.session_state:
    # set the initial default value of the slider widget
    st.session_state.celsius = 50.0

st.slider(
    "Temperature in Celsius",
    min_value=-100.0,
    max_value=100.0,
    key="celsius"
)

# This will get the value of the slider widget
st.write(st.session_state.celsius)