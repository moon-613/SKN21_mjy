import streamlit as st
# streamlit lit 실행하게 해주는 것.

st.divider()  # 얇은 선.
st.title ('🚙 폐차')  # 두꺼운 글씨로 나온다.

st.header('중제목입니다.')

st.subheader('소제목입니다. ')

st.text('일반 텍스트입니다.')
st.text(10)

st.badge("python")

sample_code = '''
def function()
    print('hello, world~')
'''
st.code(sample_code, language = "python")
# python 문법으로 ''' ''' 안의 코드 보여줌.

st.markdown("컬러코드를 이용해 텍스트 색을 지정합니다. :green[초록색]")






