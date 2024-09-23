import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL 설정
post_url = 'https://www.codil.or.kr/helpdesk/search.do'
#최초 요청 url: https://www.codil.or.kr/helpdesk/search.do?bbsId=BBSMSTR_900000000202&bbsAttrbCode=BBSA01

# 요청에 포함할 폼 데이터 설정
form_data = {
    'bbsId': 'BBSMSTR_900000000202',
    'nttId': '0',
    'bbsTyCode': 'BBST03',
    'bbsAttrbCode': 'BBSA01',
    'authFlag': '',
    'pageIndex': '1',  # 페이지 번호 (동적으로 변경 가능)
    'searchCnd': '0',  # 검색 조건 (0: 제목)
    'searchWrd': ''    # 검색어 (빈 값)
}

# 사용자 에이전트 설정
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}

# 데이터 저장할 리스트 생성
data = []

# 페이지 번호 순회
for page_num in range(1, 4):
    form_data['pageIndex'] = str(page_num)  # 페이지 번호 변경
    
    # POST 요청 보내기 (SSL 인증서 검증 비활성화)
    response = requests.post(post_url, data=form_data, headers=headers, verify=False)

    
    # 응답 데이터 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 목록 불러오기
    limit_list = soup.select('#content > div > div.content > table > tbody > tr')

    for tr in limit_list:
        depth2_link = tr.get('onclick')
        title = tr.select_one('td.title')

        depth2_start = depth2_link.find("href='")+6 #URL 시작 부분
        depth2_end = depth2_link.find("'", depth2_start) #URL 끝 부분

        # 데이터를 딕셔너리로 저장
        row_data = {
            '제목': title.text if title else '',
            '링크': depth2_link[depth2_start:depth2_end]
        }

        # 데이터 리스트에 추가
        data.append(row_data)

# 데이터프레임 생성
df = pd.DataFrame(data)

# Excel 파일로 저장
df.to_excel('codil_data_post.xlsx', index=False)
