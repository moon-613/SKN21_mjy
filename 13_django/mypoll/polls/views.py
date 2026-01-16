from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime

# Create your views here.

# 설문 welcome page view
# 요청 - 인사말 화면을 응답. 
def welcome (request):  # 최소 한 개 파라미터는 선언해야 함
    print("Welcome 실행")
    # 요청 처리
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 처리 결과 페이지 생성 -> html을 str로 구현
    res_html = f"""<!DOCTYPE>
<html>
    <head>
        <title>설문</title>
    </head>
    <body>
        <h1>Welcome</h1>
        <p>저희 설문 페이지를 방문해주셔서 감사합니다.</p>
        현재 시간: {now}
    </body>
</html>
"""
    res = HttpResponse(res_html)
    return res