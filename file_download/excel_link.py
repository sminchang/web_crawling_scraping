from urllib import request
import pandas as pd
import ssl

# SSL 인증서 검증을 비활성화
ssl._create_default_https_context = ssl._create_unverified_context

df = pd.read_excel('codil_data_with_depth3.xlsx')

for index, row in df.iterrows():
    depth1_data = row.to_dict()
    url = depth1_data['링크']
    fname = f"./data3/{depth1_data['제목']}.pdf"

    request.urlretrieve(url, fname)
print('다운로드를 완료했습니다.')

#depth2_