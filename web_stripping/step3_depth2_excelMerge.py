import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

#주요 기능
#1. 엑셀에 저장된 링크 목록에 접근하여 스크래핑
#2. 기존 엑셀 파일에 새로운 추출 데이터 병합(추가)
#3. depth1:depth2의 관계가 1:N인 경우, 동일한 depth1 데이터를 가지는 여러 depth2 행 생성

#예외 사항
#1. depth2가 페이징되어있는 경우를 예외처리하지 않은 상태(예외처리없이 엑셀로 추출 후 같은 depth1을 가지는 행이 다수인 경우 확인해보기로 함)


# 크롬 드라이버 설정
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# 엑셀 파일 읽기
df = pd.read_excel('codil_data.xlsx')

# 결과를 저장할 새로운 리스트
results = []


# 지정된 링크에서 depth2 데이터를 가져와 기존 depth1 데이터와 합치는 함수
def scrape_depth2(url, depth1_data):
    driver.get(url)
    time.sleep(5)  # 페이지 로딩 대기

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 목록 불러오기
    top_10 = soup.select('#tbody > tr')
    
    depth2_results = []
    
    for tr in top_10:
        title2 = tr.select_one('td:nth-child(2) > a > p')
        place = tr.select_one('td:nth-child(2) > span')

        td3 = tr.select_one('td:nth-child(3)').get_text(separator='<br>')  # '<br>' 기준으로 텍스트 구분
        year = td3.split('<br>')[0]  # 첫 번째 값(개정년도)만 가져오기

        infoType = tr.select_one('td:nth-child(3) > span')
        sourceInfo = tr.select_one('td:nth-child(4) > a')

        depth2_data = {
            'depth2_제목': title2.text.strip() if title2 else '',
            'depth2_출처정보' : place.text.replace('출처정보 :', '').strip() if place else '',
            'depth2_개정연도' : year.replace('개정년도 :', '').strip() if year else '',
            'depth2_정보유형' : infoType.text.strip() if infoType else '',
            'depth2_링크' : f'https://www.codil.or.kr/{sourceInfo.get("href")}' if sourceInfo else ''
        }

        # depth1 데이터와 depth2 데이터를 결합하여 새로운 행을 만듦(1:N 매핑의 경우, 1은 중복되는 데이터 생성하여 N개에 매핑)
        combined_data = {**depth1_data, **depth2_data}
        depth2_results.append(combined_data)

    return depth2_results


# 기존 엑셀 파일의 각 행을 순회하며 '링크'열을 따라 depth2 데이터 스크래핑하는 루프
for index, row in df.iterrows():
    depth1_data = row.to_dict()
    url = depth1_data['링크']
    
    try:
        # 여러 depth2 데이터가 반환되므로 이를 results에 하나씩 추가
        depth2_list = scrape_depth2(url, depth1_data)
        results.extend(depth2_list)
    except Exception as e:
        print(f"Error processing {url}: {str(e)}")
        # 에러 발생 시에도 depth1 데이터를 결과에 추가 (에러 메시지 포함)
        results.append({**depth1_data, 'depth2_내용': f'Error: {str(e)}'})

# 드라이버 종료
driver.quit()

# 결과를 새로운 DataFrame으로 변환
result_df = pd.DataFrame(results)

# 새로운 엑셀 파일로 저장
result_df.to_excel('codil_data_with_depth2.xlsx', index=False)
print("데이터가 'codil_data_with_depth2.xlsx' 파일로 저장되었습니다.")
