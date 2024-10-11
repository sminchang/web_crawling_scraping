import pdfplumber
import re
import pandas as pd

def extract_text_to_file(pdf_path, output_file):
    data = []
    previous_row_data = None  # 직전 행 데이터를 저장하기 위한 변수

    # 각 섹션에서 제목을 추출할 때 사용할 패턴 (회계연도 직전 텍스트)
    title_pattern = r'(.*?)(?=\n회계연도)'  

    # 항목별 추출 패턴
    item_patterns = {
        '회계연도': r'회계연도\s*:\s*(\d{4})',
        '회계': r'회\s*계\s*:\s*(.+?)(?=\n)',
        '조직': r'조\s*직\s*:\s*(.+?)(?=기\s*능\s*|$)',
        '기능': r'기\s*능\s*:\s*(.+?)(?=\n)',
        '정책사업': r'정책사업\s*:\s*(.+?)(?=단위사업\s*|$)',
        '단위사업': r'단위사업\s*:\s*(.*?)(?=\n\s*□\s*사업개요|$)',
        '사업목적': r'○\s*사업목적\s*:(.*?)(?=○\s*사업기간|$)',
        '사업기간': r'○\s*사업기간\s*:(.*?)(?=○\s*총사업비|$)',
        '총사업비': r'○\s*총사업비\s*:(.*?)(?=○\s*사업규모|$)',
        '사업규모': r'○\s*사업규모\s*:(.*?)(?=○\s*사업내용|$)',
        '사업내용': r'○\s*사업내용\s*:(.*?)(?=○\s*지원형태|$)',
        '지원형태': r'○\s*지원형태\s*:(.*?)(?=○\s*지원조건|$)',
        '지원조건': r'○\s*지원조건\s*:(.*?)(?=○\s*사업위치|$)',
        '사업위치': r'○\s*사업위치\s*:(.*?)(?=○\s*시행주체|$)',
        '시행주체': r'○\s*시행주체\s*:(.*?)(?=○\s*추진근거|$)',
        '추진근거': r'○\s*추진근거\s*:(.*?)(?=○\s*추진경위|$)',
        '추진경위': r'○\s*추진경위\s*:(.*?)(?=○\s*추진계획|$)',
        '추진계획': r'○\s*추진계획\s*:(.*?)(?=□|\Z)'
    }

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, 1):
            text = page.extract_text()

            # 제목 추출 (회계연도 바로 위 텍스트)
            title_match = re.search(title_pattern, text, re.DOTALL)
            if title_match:
                title = title_match.group(0).strip()
                start_page = page_num
                end_page = page_num

                # 새로운 행 데이터를 추가
                row_data = [title, start_page, end_page]

                # 각 항목별로 데이터를 추출해서 저장
                for item_key, item_pattern in item_patterns.items():
                    match = re.search(item_pattern, text, re.DOTALL)
                    if match:
                        content = match.group(1).strip()
                        row_data.append(content)
                    else:
                        row_data.append(" ")

                data.append(row_data)
                previous_row_data = row_data  # 현재 행을 저장하여 다음에 사용할 수 있게 함
            else:
                # 새로운 제목이 없을 경우, 이전 행의 마지막 페이지 번호를 현재 페이지 번호로 업데이트
                if previous_row_data:
                    previous_row_data[2] = page_num

    # 결과를 엑셀 파일로 저장
    columns = ['제목', '시작페이지', '마지막페이지'] + list(item_patterns.keys())
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(output_file, index=False)

    print(f"데이터가 '{output_file}'에 저장되었습니다.")

pdf_path = "2018_사업별 세부설명자료.pdf"
output_file = "pdfplumber_content_2018.xlsx"

extract_text_to_file(pdf_path, output_file)