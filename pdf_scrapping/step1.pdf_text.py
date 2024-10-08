# spire.pdf는 정확도가 높지만 유료 API로 무료 버전에서는 페이지 갯수가 제한되어있다.
# PyMuPDF, PyPDF2 모두 텍스트 내 공백 문자를 생략해버리는 문제와 
    # 페이지 최상단에 위치한 세부사업 번호와 제목을 뒤늦게 추출하는 문제로 사용하지 않았다.
# PyMuPDF는 개행 처리에 있어 텍스트 내 개행 문자 단위를 기준으로 하는 것으로 보인다.
# PyPDF2도 페이지 레이아웃 상 개행을 기준으로 하는 것으로 보인다.
# pdfminer가 가장 정밀하게 pdf 원본을 추출하여 최종 사용하였다.
# .six는 파이썬 2와 3사이의 호환성을 제공한다. 필요한 경우 추가한다.


from pdfminer.high_level import extract_text

def pdf_to_text(pdf_path, output_text_file):
    # PDF 파일에서 텍스트 추출
    text = extract_text(pdf_path)
    
    # 추출한 텍스트를 텍스트 파일로 저장
    with open(output_text_file, 'w', encoding='utf-8') as file:
        file.write(text)

    print(f"텍스트가 '{output_text_file}'에 저장되었습니다.")


# 추출할 PDF 경로, 저장할 파일 경로
pdf_path = '2023_사업별 세부설명자료-A.pdf'
output_text_file = 'output.txt'

#실행
pdf_to_text(pdf_path, output_text_file)


#--------------------------------------------------------------------

# import fitz

# def extract_text_from_pdf(pdf_path, output_txt_path):
#     doc = fitz.open(pdf_path)
    
#     # 전체 텍스트를 저장할 변수
#     full_text = ""
    
#     # 모든 페이지에서 텍스트 추출
#     for page in doc:
#         full_text += page.get_text()
    
#     with open(output_txt_path, 'w', encoding='utf-8') as f:
#         f.write(full_text)
    
#     print(f"텍스트가 '{output_txt_path}'에 저장되었습니다.")


# pdf_path = "2023_사업별 세부설명자료-A.pdf"
# output_txt_path = "output2.txt"

# extract_text_from_pdf(pdf_path, output_txt_path)

#--------------------------------------------------------------------

# import PyPDF2

# def pdf_to_text(pdf_path, output_text_file):

#     with open(pdf_path, 'rb') as pdf_file:
#         pdf_reader = PyPDF2.PdfReader(pdf_file)
        
#         text = ''
#         for page in pdf_reader.pages:
#             text += page.extract_text() + '\n'  # 페이지별로 텍스트 추출하여 추가

#     with open(output_text_file, 'w', encoding='utf-8') as f:
#         f.write(text)

#     print(f"텍스트가 '{output_text_file}'에 저장되었습니다.")


# pdf_path = '2023_사업별 세부설명자료-A.pdf'
# output_text_file = 'output3.txt'

# pdf_to_text(pdf_path, output_text_file)