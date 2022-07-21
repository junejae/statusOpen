import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from collections import defaultdict

NOVEL_NAME = '혁명은 내 취향이 아니었다'
DATE_COLUMN = 'date'
EMOTION_COLUMN = 'emotion'
DATA_DIR = NOVEL_NAME + '_comment_data.csv'

st.title(f'[{NOVEL_NAME}] 댓글 감정 분석 대시보드')

# 데이터 로딩 함수
@st.cache(allow_output_mutation=True)
def load_data():
    data = pd.read_csv(DATA_DIR, encoding="utf-8")
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])

    temp = []

    for emote in data[EMOTION_COLUMN]:
        temp.append(eval(emote))
        
    data[EMOTION_COLUMN] = temp

    return data

data = load_data()

latest_story_num = max(list(data['story_num']))

# 각 화별 감정을 좋아요 수치를 가산하여 카운팅
stories = [defaultdict(int) for _ in range(latest_story_num + 1)]

for emotes, like, num in zip(data[EMOTION_COLUMN], data['like'], data['story_num']):
    for emote in emotes:
        stories[num][emote] += (1 + like)

# 화수별로 볼 수 있도록 슬라이더 세팅
viewing_story_num= st.slider('##열람을 원하는 회차로 슬라이더를 옮겨주세요##', 1, latest_story_num, 1)

temp = list(stories[viewing_story_num].items())

# 가장 많이 언급된 감정 Top 5를 볼 수 있도록 정렬
temp.sort(key=lambda x: x[1], reverse=True) 

emo_keys = [key for key, _ in temp]
emo_vals = [val for _, val in temp]

if len(emo_keys) > 5:
    emo_keys = emo_keys[:5]
    emo_vals = emo_vals[:5]

# 막대 그래프 출력
plt.rcParams['font.family'] = 'NanumGothic'
fig, axs = plt.subplots(figsize=(7, 5))
axs.bar(emo_keys, emo_vals)

st.subheader(f'{viewing_story_num}화 댓글 감정 Top 5')
st.pyplot(fig)

# 각 화별 댓글 데이터 열람
if st.checkbox(f'{viewing_story_num}화 댓글 데이터 보기'):
    st.subheader(f'{viewing_story_num}화 댓글 데이터')
    st.write(data[data['story_num'] == viewing_story_num])
