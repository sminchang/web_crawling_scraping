# spire.pdf는 유료 API로 무료 버전에서는 페이지 갯수가 제한되어있다.
# PyMuPDF, PyPDF2 모두 텍스트 내 공백 문자를 생략해버리는 문제와 
# 페이지 레이아웃 상 최상단에 위치한 세부사업 번호와 제목을 뒤늦게 추출하는 문제로 사용하지 않았다.
# PyMuPDF는 개행 처리에 있어 텍스트 내 개행 문자 단위를 기준으로 하는 것으로 보인다.
# PyPDF2도 페이지 레이아웃 상 개행을 기준으로 하는 것으로 보인다.
# pdfminer가 가장 정밀하게 pdf 원본을 추출하여 최종 사용하였다.
# .six는 파이썬 2와 3사이의 호환성을 제공한다.


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


# 추출할 PDF 경로, 저장할 excel 경로
pdf_path = "2023_사업별 세부설명자료.pdf"
output_file = "extracted_data.xlsx"

# 실행
extract_text_to_file(pdf_path, output_file)
print(f"데이터가 '{output_file}'에 저장되었습니다.")
