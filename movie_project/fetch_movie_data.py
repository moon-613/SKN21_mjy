import requests
import pandas as pd
import json

TMDB_API_KEY = 'f012e69a23da703566a215dae9c5708a'  # 🔑 여기에 발급받은 실제 TMDB API 키를 붙여넣으세요!

ACTION_GENRE_ID = 28             # 액션 장르 ID
COUNTRY_CODE = 'KR'              # 한국 (데이터 및 플랫폼 조회용)
CSV_FILENAME = 'tmdb_ott_movies_for_db.csv'

# TMDB 기본 URL
BASE_URL = 'https://api.themoviedb.org/3'
IMAGE_BASE_URL = 'https://image.tmdb.org/t/p/w500' 

# 한국 OTT 서비스 이름 (TMDB API 응답 이름과 일치해야 함)
KOREAN_OTT_NAMES = ['Tving', 'Wavve', 'Coupang Play', 'Watcha', 'Netflix'] 

# ==========================================================
# 2. 데이터 수집 함수
# ==========================================================
def fetch_movie_data_with_platform():
    """TMDB에서 영화 메타데이터, 출연진, OTT 플랫폼 정보를 가져와 정리하는 함수"""
    
    print("TMDB API에서 영화 목록을 가져옵니다...")
    
    # 2-1. 액션 장르 영화 목록 가져오기 (1페이지 기준)
    discover_params = {
        'api_key': TMDB_API_KEY,
        'with_genres': ACTION_GENRE_ID,
        'language': 'ko-KR',
        'sort_by': 'popularity.desc'
    }
    
    discover_response = requests.get(f'{BASE_URL}/discover/movie', params=discover_params)
    
    # API 키 오류 등 상태 확인
    print(f"Discovery API Status Code: {discover_response.status_code}") 
    if discover_response.status_code != 200:
        print("🚨 API 요청 실패! TMDB_API_KEY가 유효한지 확인하세요 (401 오류 예상).")
        return []
    
    movies_results = discover_response.json().get('results', [])
    if not movies_results:
        print("🔍 조건에 맞는 영화 데이터가 없습니다. 검색 연도(RELEASE_YEAR)를 변경해보세요.")
        return []
        
    print(f"총 {len(movies_results)}개의 영화 데이터를 가져왔습니다. 상세 정보를 처리합니다...")
    processed_list = []

    for movie in movies_results:
        movie_id = movie.get('id')
        
        # 2-2. Watch Providers 정보 (플랫폼) 가져오기
        platforms = []
        try:
            providers_url = f"{BASE_URL}/movie/{movie_id}/watch/providers"
            providers_response = requests.get(providers_url, params={'api_key': TMDB_API_KEY})
            providers_data = providers_response.json().get('results', {})
            
            if COUNTRY_CODE in providers_data:
                kr_providers = providers_data[COUNTRY_CODE]
                
                if 'flatrate' in kr_providers: # 스트리밍 서비스 확인
                    for provider in kr_providers['flatrate']:
                        provider_name = provider.get('provider_name')
                        if provider_name in KOREAN_OTT_NAMES: 
                            platforms.append(provider_name)
        except:
            # 플랫폼 정보 가져오기 실패 시 무시
            pass

        # 2-3. 주연배우(credits) 정보 가져오기
        actors_list = []
        try:
            credits_url = f"{BASE_URL}/movie/{movie_id}/credits"
            credits_response = requests.get(credits_url, params={'api_key': TMDB_API_KEY})
            if credits_response.status_code == 200:
                cast = credits_response.json().get('cast', [])
                # 주연 배우 상위 3명
                actors_list = [actor['name'] for actor in cast[:3]] 
        except:
            # 출연진 정보 가져오기 실패 시 무시
            pass

        # 2-4. 최종 데이터 조합
        poster_path = movie.get('poster_path')
        poster_url = f"{IMAGE_BASE_URL}{poster_path}" if poster_path else None
        
        processed_data = {
            'title': movie.get('title'),
            'genre': '액션', 
            'poster_url': poster_url,
            'actors': ", ".join(actors_list),
            'rating': round(movie.get('vote_average'), 2) if movie.get('vote_average') else None,
            'release_date': movie.get('release_date'),
            'platform': ", ".join(platforms) if platforms else 'Not available on selected OTTs'
        }
        processed_list.append(processed_data)
        
    return processed_list

# ==========================================================
# 3. 메인 실행 블록
# ==========================================================
if __name__ == "__main__":
    
    # 필요한 라이브러리가 설치되어 있는지 확인하는 코드 (선택 사항)
    try:
        import requests
        import pandas as pd
    except ImportError:
        print("🚨 'requests' 또는 'pandas' 라이브러리가 설치되지 않았습니다.")
        print("pip install requests pandas 명령어를 실행하여 설치해 주세요.")
    
    final_data = fetch_movie_data_with_platform()

    if final_data:
        df = pd.DataFrame(final_data)
        df.to_csv(CSV_FILENAME, index=False, encoding='utf-8-sig')
        
        print(f"\n✅ 데이터 수집 및 처리가 완료되었습니다.")
        print(f"결과 파일: {CSV_FILENAME}가 'movie_project' 폴더에 생성되었습니다.")
        print("\n--- 수집된 데이터 미리보기 (상위 5개) ---")
        print(df.head())
    else:
        print("\n❌ 최종적으로 수집된 유효 데이터가 없어 CSV 파일이 생성되지 않았습니다.")

