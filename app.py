'''
제작일자: ( 제작 완료일 or 마지막 수정일 ) 20.02.05
프로그램 이름: 
설명: 트위치 다시보기 영상 중, 내가 원하는 부분의 채팅 데이터를 불러와 csv파일로 저장한다.
작성자: 김대호, kfdream123@gmail.com
'''
import requests
import json
import csv

nextCursor = None
URL = 'https://api.twitch.tv/v5/videos/542058917/comments?content_offset_seconds=0'
params = {}
params['client_id'] = 'i0xz1n3g3e61fto07o9taanicb1l4x'

response = requests.get(url = URL, params = params)
response_json = json.loads(response.text)

csvFile = open('test.csv', 'w', encoding='euc_kr', newline='')
csvWriter = csv.writer(csvFile)

tictoc = 1
test = 1
while True:
    for i in response_json["comments"]:
        try:
            csvWriter.writerow([test, str(i["content_offset_seconds"]), i["message"]["body"]])
        except UnicodeEncodeError as e:
            print("what's wrong : " + str(test)) #오류 비율 기록해 놓으라네?(지연)
            print(e)
        test = test + 1
    print("is working ... " + str(tictoc))
    tictoc = tictoc + 1
    
    nextCursor = response_json["_next"]
    if nextCursor == None: #이걸로("") 끝부분 처리 안되는듯?
        break
    URL = 'https://api.twitch.tv/v5/videos/542058917/comments?cursor=' + nextCursor
    response = requests.get(url = URL, params = params)
    response_json = json.loads(response.text)
csvFile.close()

#https://steemit.com/kr-dev/@steemonen1/twitch
#http://pythonstudy.xyz/python/article/207-CSV-%ED%8C%8C%EC%9D%BC-%EC%82%AC%EC%9A%A9%ED%95%98%EA%B8%B0
#https://hotman.tistory.com/entry/csv-%ED%8C%8C%EC%9D%BC-%ED%95%9C%EA%B8%80-%EA%B9%A8%EC%A7%90-%ED%95%B4%EA%B2%B0
#https://wikidocs.net/30
'''
직면한 오류들:
1. 인코딩 관련
 _1. utf-8이 한글이 깨짐 >> euc_kr로 바꿔봄
 _2. euc_kr은 \n2014를 처리할 수 없다는 UnicodeEncodeError가 뜸 >> 해결은 X, 예외처리로 pass함
2. connect aborted? 네트워크 오류 뜸[error 10053]
'''