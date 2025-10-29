import streamlit as st
import pandas as pd
import random 

# 1. 페이지 설정
st.set_page_config(
    page_title="수도권 폐차장 조회 및 FAQ 시스템",
    page_icon="🚙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. 사이드바 메뉴 구현
st.sidebar.title("🛠️ 시스템 메뉴")
menu = st.sidebar.radio(
    " 원하는 서비스를 선택하세요: ",
    ('폐차장 조회', 'FAQ 검색 시스템', '통계 시각화', 'SQL 질의 진행')
)

# 3. 메인 콘텐츠 함수 정의
def show_scrapyard_finder():
    """ 폐차장 조회 페이지 """
    st.header ("📍수도권 폐차장 조회")
    st.write("지역 또는 업체명으로 등록된 폐차장 정보를 검색하세요.")

    col1, col2 = st.columns(1)

    with col1:
        selected_area = st.selectbox(
            "지역별 검색",
            ['전체', '서울', '경기', '인천'],
            index = 0   # 기본값 '전체'
        )
    with col2:
        search_name = st.text_input("업체명 검색 (키워드)", max_chars=50)


# ------------------------------------------------------------

# 검색 버튼
    if st.button("폐차장 목록 검색"):
        # 검색 조건에 따라 함수 호출
        area_filter = selected_area if selected_area != '전체' else None
        
        # 🚨 DB 함수 호출 (현재는 Mock 함수 사용)
        result_df = get_scrapyard_list(area=area_filter, name=search_name)

        if not result_df.empty:
            st.success(f"검색 조건에 맞는 폐차장 **{len(result_df)}** 건을 찾았습니다.")
            
            # 상세 정보 표시
            st.dataframe(
                result_df[['업체명', '지역', '주소', '연락처']], 
                use_container_width=True,
                hide_index=True
            )
            
            # 지도 기반 시각화 (위도/경도 컬럼이 있어야 함)
            st.subheader("🗺️ 지도 기반 위치 보기")
            st.map(result_df[['lat', 'lon']].rename(columns={'lat': 'latitude', 'lon': 'longitude'}))
            
        else:
            st.warning("해당 조건에 맞는 폐차장 정보가 없습니다.")

def show_faq_system():
    """[2] FAQ 검색 시스템 페이지"""
    st.header("❓ 폐차 관련 자주 묻는 질문 (FAQ)")
    st.write("궁금한 키워드를 입력하시면 관련된 질문과 답변을 찾아드립니다.")
    
    # 사용자 입력: 검색 키워드 위젯
    keyword = st.text_input("검색 키워드 입력", max_chars=50, key="faq_keyword")
    
    if st.button("FAQ 검색"):
        if keyword:
            # 🚨 DB 함수 호출 (현재는 Mock 함수 사용)
            faq_list = search_faq(keyword)
            
            if faq_list:
                st.info(f"'{keyword}'와(과) 관련된 FAQ **{len(faq_list)}** 건이 검색되었습니다.")
                
                # 검색 결과를 확장 가능한 형태로 출력
                for i, item in enumerate(faq_list):
                    # st.expander를 사용하여 답변을 숨겨 사용자 경험 향상
                    with st.expander(f"**Q{i+1}.** {item['Q']}"):
                        st.markdown(f"**A.** {item['A']}")
                        st.caption(f"**출처:** {item['출처']}") # 출처 표기
            else:
                st.warning(f"'{keyword}'와(과) 관련된 질문을 찾을 수 없습니다.")
        else:
            st.error("검색 키워드를 입력해주세요.")


def show_statistics():
    """[3] 통계 시각화 페이지"""
    st.header("📊 수도권 폐차장 현황 통계")
    st.write("저장된 데이터를 기반으로 폐차장 분포 현황을 시각적으로 보여줍니다.")
    
    # 🚨 DB 함수 호출 (현재는 Mock 함수 사용)
    area_counts, trend_data, ratio_data = get_scrapyard_stats()
    
    # 3-1. 지역별 폐차장 수 막대그래프
    st.subheader("1. 지역별 폐차장 수")
    st.bar_chart(area_counts.set_index('지역'))
    st.dataframe(area_counts, hide_index=True)
    
    st.markdown("---")
    
    # 3-2. 등록일자별 추이
    st.subheader("2. 신규 등록일자별 추이 (월별)")
    st.line_chart(trend_data.set_index('등록월'))
    st.dataframe(trend_data, hide_index=True)
    
    st.markdown("---")
    
    # 3-3. 수도권 내 비율 pie chart
    st.subheader("3. 수도권 폐차장 비율")
    
    # Streamlit의 기본 차트 대신 Plotly를 사용해 Pie Chart를 더 잘 시각화할 수 있습니다.
    try:
        import plotly.express as px
        fig = px.pie(
            ratio_data, 
            values='비율', 
            names='지역', 
            title='수도권 폐차장 수 비율',
            hole=.3 # 도넛 차트 형태로 표시
        )
        st.plotly_chart(fig, use_container_width=True)
    except ImportError:
        # plotly가 설치되어 있지 않을 경우를 대비
        st.info("Plotly 라이브러리가 설치되어 있지 않아 파이 차트가 표시되지 않습니다. (pip install plotly)")
        st.dataframe(ratio_data, hide_index=True)

def show_sql_executor():
    """SQL 질의 실행 페이지 (실습 목적)"""
    st.header("💻 SQL 질의 실행기")
    st.warning("이 기능은 데이터 조회 학습 및 디버깅을 위한 기능입니다. `SELECT` 문만 사용해주세요.")
    
    query = st.text_area("SQL Query 입력", 
                         value="SELECT * FROM scrapyard_table WHERE region = '서울' LIMIT 5;", 
                         height=150,
                         key="sql_query_input")
    
    if st.button("쿼리 실행", key="execute_sql_button"):
        try:
            # 🚨 DB 함수 호출
            result_df = execute_custom_sql(query)
            
            st.success("쿼리가 성공적으로 실행되었습니다.")
            st.dataframe(result_df, use_container_width=True)
            
        except Exception as e:
            st.error(f"쿼리 실행 중 오류 발생: {e}")


# --------------------------------------------------------


# 4. 메인 라우팅 (메뉴에 따라 콘텐츠 표시)

if menu == '폐차장 조회':
    show_scrapyard_finder()
elif menu == 'FAQ 검색 시스템':
    show_faq_system()
elif menu == '통계 시각화': # 통계 시각화 추가
    show_statistics()
elif menu == 'SQL 질의 실행':
    show_sql_executor()





#Project README.md
#Readme.md는 발표 자료로 사용할 수 있도록 작성한다.

#    팀원 및 담당 업무
#프로젝트 주제 및 주제 설명 및 선정 이유
#주제를 선택한 이유 주요 기능프로젝트를 구성하는 디렉토리들과 파일들의 구조.수집 데이터 설명데이터 베이스 테이블 설명Application의 주요 기능

#    Application 제공하는 기능 설명
#회고: 구현 도중 생겼던 문제와 어떻게 해결했는지 작성.
#각자 프로젝트 진행하면서 느낀 점

#1차 단위 프로젝트
#주제 - 전국 자동차 등록 현황 및 기업 FAQ 조회 시스템
#자동차나 자동차 회사와 관련된 데이터를 수집해서 Database 에 저장 후 그 데이터 기반 FAQ 시스템 구현

#        자동차와 관련된 다양한 정보를 제공하는 FAQ(Frequently Asked Questions - 자주 묻는 질문) 시스템.
#            차와 관련된 다양한 정보를 중 관심 있는 것을 선택해서 수집.
#               수집한 데이터를 Database에 저장.

#저장된 데이터에 대한 정보 제공하는 시스템을 streamlit 기반으로 구현.프로젝트 주 목적

#    크롤링을 이용한 데이터 수집 실습
#        수집한 데이터를 데이터베이스에  저장하고 조회하여 SQL을 실습

# # 조회 질의를 사용자로 부터 입력받아 조회결과를 출력하는 application 구현
#Github Repository
#https://github.com/orgs/SKNETWORKS-FAMILY-AICAMP/repositories

#산출물
#소스 코드
#    데이터 웹 크롤링 코드

#Application 구현 코드수집/저장한 데이터 

#    Database에 데이터를 script로 입력했을 경우 sql script 파일. 
#        코드를 통해 입력 했으면 python 코드 파일들.

#csv, 엑셀 등 파일이 있는 경우 그 파일들.산출물 문서

#    데이터 베이스 설계 문서
#        데이터베이스 정의서
#            테이블 당 다음 내용을 작성
#                테이블 설명(테이블 이름, 저장하는 데이터에 대한 간략한 설명)
#                    테이블 컬럼들 설명(표로 작성. 속성이름, 결측치 허용여부, 제약 조건, 기본값 을 설명)

#ERD수집 데이터

#    수집 데이터에 대한 설명
#        각 데이터를 어디에서 수집했는지.
#            각 데이터를 수집한 목적

#각 데이터에 대한 설명데이터 조회 프로그램 설명

#    FAQ 프로그램에 대한 설명
#        사용 메뉴얼을 작성한다.

