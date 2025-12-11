# ko_en_translator/app.py
## Huggingface transformers.pipeline을 이용해서 한국어를 영어로 번역하는 app.

import streamlit as st
from transformers import pipeline

# 처음 시작할 때 한 번 실행하고 반환되는 리소스를 메모리에 저장해놓고 다음부터는 그걸 사용. 
@st.cache_resource
def get_model():
    model = "Copycats/koelectra-base-v3-generalized-sentiment-analysis"
    pipe = pipeline(task="text-classification", model=model)
    return pipe 

classifier = get_model()

def classify_and_clear():
    pass

# 긍부정 분류한 내역을 저장할 session_state를 생성
# 어떤 값들을 계속 유지해야 할 때 저장하는 공간 (dict 타입): session_state
if "history" not in st.session_state:
    st.session_state.history = []  # [(댓글1, 분류내역1), (댓글2, 분류내역2), ...]

st.title("댓글분석기")
st.subheader("댓글의 내용이 긍정적인지 부정적인지 분류합니다.")

# on change: event handler (어떤 변화가 발생하면 함수를 호출) - test 입력폼에 값이 바뀌고 엔터가 입력되면 함수를 호출. 
st.text_input("분석할 댓글: ", on_change=classify_and_clear)


st.button("번역")