import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from collections import defaultdict

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date'
EMOTION_COLUMN = 'emotion'
DATA_DIR = ('혁명은 내 취향이 아니었다_comment_data.csv')

@st.cache
def load_data():
    data = pd.read_csv(DATA_DIR, encoding="utf-8")
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    temp = []

    for emote in data[EMOTION_COLUMN]:
        temp.append(eval(emote))
        
    data[EMOTION_COLUMN] = temp

    return data

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text("Done! (using st.cache)")

emotions = defaultdict(int)

for emotes in data[EMOTION_COLUMN]:
    for emote in emotes:
        emotions[emote] += 1


if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

plt.rcParams['font.family'] = 'NanumGothic'
fig, axs = plt.subplots(figsize=(60, 20))
axs.bar(list(emotions.keys()), list(emotions.values()))

st.pyplot(fig)


# st.subheader('Number of pickups by hour')
# hist_values = np.histogram(data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
# st.bar_chart(hist_values)

# hour_to_filter = st.slider('hour', 0, 23, 17)
# filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

# st.subheader('Map of all pickups at %s:00' % hour_to_filter)
# st.map(filtered_data)