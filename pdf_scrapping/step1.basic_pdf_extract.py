#spire.pdf는 유료 API로 무료 버전에서는 페이지 갯수가 제한되어있다.
#PyMuPDF는 텍스트 내 공백 문자를 인식하지 못하는 문제가 있어 사용하지 않았다.
#PyPDF2는 사용해보지 않았다.
#pdfminer의 최신 버전인 pdfminer.six로 해결이 되었다.

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
