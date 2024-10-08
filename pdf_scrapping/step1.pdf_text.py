from pdfminer.high_level import extract_text

def pdf_to_text(pdf_path, output_text_file):
    # PDF 파일에서 텍스트 추출
    text = extract_text(pdf_path)
    
    # 추출한 텍스트를 텍스트 파일로 저장
    with open(output_text_file, 'w', encoding='utf-8') as fileA:
        fileA.write(text)

# 실행
pdf_path = '2023_사업별 세부설명자료-A.pdf'  # 변환할 PDF 파일 경로
output_text_file = 'output.txt'  # 저장할 텍스트 파일 경로

pdf_to_text(pdf_path, output_text_file)
print(f"텍스트가 '{output_text_file}'에 저장되었습니다.")