# ko_en_translator/app.py
## Huggingface transformers.pipeline을 이용해서 한국어를 영어로 번역하는 app.

import streamlit as st
from transformers import pipeline

# 처음 시작할 때 한 번 실행하고 반환되는 리소스를 메모리에 저장해놓고 다음부터는 그걸 사용. 
@st.cache_resource
def get_model():
    model = "Helsinki-NLP/opus-mt-ko-en"
    pipe = pipeline(task="translation", model=model)
    return pipe 

translator = get_model()
