# pdfplumber, 탭 문자를 하나의 공백 문자로 처리한다.
# 항목별로 텍스트를 추출하는 스크립트

import pdfplumber
import re
import pandas as pd

def clean_text(text):
    # 연속된 개행 문자를 하나의 개행 문자로 대체, 한 문장이 길어져 자동개행된 경우를 원래대로 처리
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

def extract_text_to_file(pdf_path, output_file):
    data = []

    section_pattern = r'(?:세부사업:\s*((?:\d|\w){4}-(?:\d|\w){3}-(?:\d|\w){4}-(?:\d|\w){4}-(?:\d|\w){4}))\s*\n+(.*?)\s*(?=회계연도\s*:)'

    item_patterns = {
        '회계연도': r'회계연도\s*:\s*(\d{4})년',
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
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"

    text = clean_text(text)

    # 세부사업 번호를 기준으로 섹션 분리 후 전체 섹션을 리스트로 저장
    sections = list(re.finditer(section_pattern, text, re.DOTALL))

    # 섹션 하나씩 세부 아이템 추출 반복
    for i, section in enumerate(sections):
        # 섹션의 세부사업 번호와 제목 추출
        business_number = section.group(1).strip()
        title = clean_text(section.group(2)).strip().replace('\n', '')  # 제목이 길어서 개행된 경우도 처리
        
        # 전체 텍스트에서 해당 섹션 구간 추출
        start = section.start()
        if i < len(sections) - 1:
            end = sections[i+1].start()
        else:
            end = len(text)
        section_text = text[start:end]
        
        row_data = [business_number, title]

        # 해당 섹션 내 아이템별 추출, 같은 행의 다른 열에 추가
        for item_key, item_pattern in item_patterns.items():
            match = re.search(item_pattern, section_text, re.DOTALL)
            if match:
                content = match.group(1).strip()
                row_data.append(content)
            else:
                row_data.append(" ")
        data.append(row_data)

    # 모든 섹션에 대한 통합 엑셀 파일 생성
    columns = ['세부사업 번호', '제목'] + list(item_patterns.keys())
    df = pd.DataFrame(data, columns=columns)
    df.to_excel(output_file, index=False)

    print(f"데이터가 '{output_file}'에 저장되었습니다.")

pdf_path = "2023_사업별 세부설명자료.pdf"
output_file = "pdfplumber_content.xlsx"

extract_text_to_file(pdf_path, output_file)