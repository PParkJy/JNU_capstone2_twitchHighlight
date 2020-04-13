'''
컴퓨터정보통신공학전공 175704 박지연
하이라이트 데이터를 전처리
'''

import csv
import os
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from soynlp.tokenizer import LTokenizer
from soynlp.word import WordExtractor

file_name = './data/highlight/79매치_1경기/하이라이트/399807785_13.csv'

def make_dir(file_name):
    temp = file_name.split('/')
    temp_num = temp[5].split("_")[1]
    file_num = temp_num.split(".")[0]
    temp[5] = temp[5].split("_")[0]
    result_path = "./data/result/" + temp[2] + "/" + temp[3] + "/" + temp[5]
    try:
        if not os.path.exists(result_path):
            os.makedirs(result_path)
    except OSError:
        print("폴더 생성에 실패했습니다. ")
    return result_path, file_num

def read_data(filename):
    raw_time = []
    raw_chat = []
    f = open(filename, 'r', encoding='euc-kr')
    raw = csv.reader(f)
    for line in raw:
        raw_time.append(line[1])
        raw_chat.append(line[2])
    f.close()
    return raw_time, raw_chat

'''
word extractor로 확인한 결과
가장 많이 나온 단어를 보니까 ㅋ이 많은데..
'''
def laugh_check(raw_chat):
    sentence_cnt = 0 #ㅋ이 들어간 문장의 수
    avg_prob = 0
    list_single = []
    for chat in raw_chat:
        if "ㅋ" in chat:
            sentence_cnt += 1 #ㅋ이 들어간 문장의 개수
            single_cnt = 0
            for single_chat in chat:
                if single_chat == "ㅋ":
                    single_cnt += 1
            list_single.append(single_cnt) #한 문장 내에서의 ㅋ의 개수
            avg_prob += (single_cnt/len(chat))
    np_single = np.array(list_single)
    result_path, file_num = make_dir(file_name)
    f = open(result_path+"/"+file_num+".txt",mode="w")
    f.write("전체 chat 데이터 개수: " + str(len(raw_chat)) + "\n")
    f.write("전체 chat 중 ㅋ이 들어간 chat의 평균 비율: " + str(round(sentence_cnt / len(raw_chat) * 100, 3)) + "%\n")
    f.write("한 chat 내에서 ㅋ이 차지하는 평균 비율: " + str(round((avg_prob / sentence_cnt) * 100, 3)) + '%\n')
    f.write("ㅋ이 들어간 chat 중 ㅋ의 최소 길이: " + str(np.min(np_single)) + '\n')
    f.write("ㅋ이 들어간 chat 중 ㅋ의 최대 길이: " + str(np.max(np_single)) + '\n')
    f.write("ㅋ이 들어간 chat 중 ㅋ의 길이의 분산: " + str(round(np.var(np_single), 3)) + '\n') #분산 크면 데이터가 흩어져있죵
    #print("ㅋ이 들어간 문장 중 ㅋ의 길이의 표준편차: ", np.std(np_single))
    f.write("ㅋ이 들어간 chat 중 ㅋ의 평균 길이: " + str(round(np.mean(np_single),3)) + '\n') #얘가 신뢰할 수 없는 정보인게 히스토그램, 분산, 표준편차 확인해보면 값이 몰려 있음 -> 중앙값도 한 번 봐보자
    f.write("ㅋ이 들어간 chat 중 ㅋ의 길이의 중앙값: " + str(np.median(np_single)) + '\n') #얘도 신뢰할 수 없는 정보인게 자료분포가 중심지향적이지 않음 -> 최빈값도 고려
    f.write("ㅋ이 들어간 chat 중 ㅋ의 길이의 최빈값(상위3개): " + str(Counter(np_single).most_common()[:3])+'\n') #상위 3개 확인
    n, bins, patches = plt.hist(np_single, bins=sentence_cnt)  # ㅋ이 들어간 문장 중 ㅋ의 평균 출현 횟수에 대한 히스토그램
    plt.savefig(result_path+"/"+file_num+".png")
    f.close()

raw_time, raw_chat = read_data(file_name)
laugh_check(raw_chat)

'''
통계에 기반하여 단어를 찾아내는 비지도 학습법
1. Accessor Variety
2. Branching Entropy
3. Cohesion score
'''
word_extractor = WordExtractor(
    min_frequency=20,
    min_cohesion_forward=0.05,
    min_right_branching_entropy=0.0
) #여기서는 Cohesion Score 사용

'''
word_extractor.train(raw_chat)
words = word_extractor.extract()
print("word extraction 길이: ",len(words), " \n결과: ")
print(words)
#words_score = {word : score.cohesion_forward for word, score in words.items()}
#tokenizer = LTokenizer(scores=words_score)
'''
