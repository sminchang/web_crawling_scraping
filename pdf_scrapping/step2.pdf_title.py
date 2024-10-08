#pdf 내 문건을 분류하는 기준이 되는 세부사업 번호와 제목을 추출하는 스크립트.
#추가로 pdf 전체 페이지(1542)와 추출된 엑셀 행(1539) 사이의 오차를 확인하여
    # 한 문건이 두 페이지를 점유한 3개 유형을 파악하였다.

from pdfminer.high_level import extract_text
import re
import pandas as pd

def extract_text_to_file(pdf_path, output_file):

    # PDF 파일에서 전체 텍스트를 추출
    text = extract_text(pdf_path)

    # 세부사업 번호와 제목을 저장할 리스트
    data = []

    # 정규 표현식, 추출할 형식 패턴 지정 후 해당 데이터들만 추출
    pattern = r'(?:세부사업:\s*((?:\d|\w){4}-(?:\d|\w){3}-(?:\d|\w){4}-(?:\d|\w){4}-(?:\d|\w){4}))\s*\n+([^\n]+)'
    matches = re.findall(pattern, text)

    # 추출한 데이터를 분할하여 리스트에 저장
    for match in matches:
        business_number = match[0].strip()
        title = match[1].strip()
        data.append([business_number, title])

    # DataFrame 생성하여 리스트 데이터를 엑셀 파일에 저장
    df = pd.DataFrame(data, columns=['세부사업 번호', '제목'])
    df.to_excel(output_file, index=False)

    print(f"데이터가 '{output_file}'에 저장되었습니다.")


pdf_path = "2023_사업별 세부설명자료.pdf"
output_file = "extracted_data.xlsx"

extract_text_to_file(pdf_path, output_file)

