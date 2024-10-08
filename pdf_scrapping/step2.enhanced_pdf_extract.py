#pdfminer,six가 다른 부분은 명확한데 도표 형식을 가져올 때는 행 순서대로 추출하지 않고 열 순서대로 추출하는 문제가 있다.

from pdfminer.high_level import extract_text
import re
import pandas as pd

def clean_text(text):
    # 연속된 개행 문자를 하나의 개행 문자로 대체, 한 문장이 길어져 자동개행된 경우를 원래대로 처리
    text = re.sub(r'\n{2,}', '\n', text)
    return text.strip()

def extract_text_to_file(pdf_path, output_file):
    text = extract_text(pdf_path)
    text = clean_text(text)

    data = []

    section_pattern = r'세부사업:\s*((?:\d|\w){4}-(?:\d|\w){3}-(?:\d|\w){4}-(?:\d|\w){4}-(?:\d|\w){4})\s*([^\n○]+)'

    item_patterns = {
        '회계연도': r'회계연도\s*:\s*(\d{4})년',
        '회계': r'회\s*계\s*:\s*(.+?)(?=\n)',
        '조직': r'조\s*직\s*:\s*(.+?)(?=\n)',
        '기능': r'기\s*능\s*:\s*(.+?)(?=\n)',
        '정책사업': r'정책사업\s*:\s*(.+?)(?=\n)',
        '단위사업': r'단위사업\s*:\s*(.+?)(?=\n)',
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

    # 세부사업 번호를 기준으로 섹션 분리 후 전체 섹션을 리스트로 저장
    sections = list(re.finditer(section_pattern, text, re.DOTALL))

    # 섹션 단위로 세부사업 번호와 제목으
    for i, section in enumerate(sections):

        # 섹션의 세부사업 번호와 제목 추출
        business_number = section.group(1).strip()
        title = clean_text(section.group(2))
        
        # 전체 텍스트에서 해당 섹션의 구간 추출
        start = section.start()
        if i < len(sections) - 1:
            end = sections[i+1].start()
        else:
            end = len(text)
        section_text = text[start:end]
        
        # 해당 섹션 내 개별 아이템값들 검색-추출하여 같은 행의 다른 열에 추가
        row_data = [business_number, title]
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

pdf_path = "2023_사업별 세부설명자료.pdf"
output_file = "extracted_data_enhanced.xlsx"

extract_text_to_file(pdf_path, output_file)
print(f"데이터가 '{output_file}'에 저장되었습니다.")
