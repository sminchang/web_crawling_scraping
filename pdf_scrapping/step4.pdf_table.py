import pdfplumber
import pandas as pd
import re

# PDF 파일 경로를 지정하세요
pdf_path = '2023_사업별 세부설명자료-A.pdf'
output_file = 'extracted_soyojaewon_data.xlsx'

data = []

# PDF 파일 열기
with pdfplumber.open(pdf_path) as pdf:
    # 페이지를 반복합니다
    for page in pdf.pages:
        # 페이지에서 텍스트 추출
        text = page.extract_text()

        # "소요재원"이 포함된 섹션 추출
        if "소요재원" in text:
            # 정규 표현식을 사용하여 세부사업 번호 추출
            business_numbers = re.findall(r'세부사업:\s*((?:\d|\w){4}-(?:\d|\w){3}-(?:\d|\w){4}-(?:\d|\w){4}-(?:\d|\w){4})', text)

            # 페이지에서 테이블 추출
            tables = page.extract_tables()

            for table in tables:
                # 테이블에 행이 있는지 확인
                if len(table) > 1:  # 헤더가 아닌 경우에만 처리
                    # 각 테이블의 두 번째 행부터 시작하여 마지막으로 발견된 세부사업 번호와 연결
                    for row in table[1:]:  # 헤더를 건너뛰고 두 번째 행부터 시작
                        # 세부사업 번호가 있는 경우 마지막으로 찾은 번호 사용
                        if business_numbers:
                            business_number = business_numbers[-1]
                        else:
                            business_number = "N/A"  # 번호가 없는 경우 기본값

                        # 비즈니스 번호를 행에 추가
                        data.append([business_number] + row)

# 데이터프레임으로 변환하고 엑셀로 저장
columns = ['세부사업 번호', '재 원 별', '계', '기투자', '2023년', '2024년', '2025년', '2026년', '2027년', '향후투자', '연평균증가율']  # 컬럼 이름 설정
df = pd.DataFrame(data, columns=columns)
df.to_excel(output_file, index=False)

print(f"데이터가 '{output_file}'에 저장되었습니다.")
