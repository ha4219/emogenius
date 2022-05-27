# d = {
#     '가난한, 불우한': 0,
#     '감사하는': 1,
#     '걱정스러운': 2,
#     '고립된': 3,
#     '괴로워하는': 4,
#     '구역질 나는': 5,
#     '기쁨': 6,
#     '낙담한': 7,
#     '남의 시선을 의식하는': 8,
#     '노여워하는': 9,
#     '눈물이 나는': 10,
#     '느긋': 11,
#     '당혹스러운': 12,
#     '당황': 13,
#     '두려운': 14,
#     '마비된': 15,
#     '만족스러운': 16,
#     '방어적인': 17,
#     '배신당한': 18,
#     '버려진': 19,
#     '부끄러운': 20,
#     '분노': 21,
#     '불안': 22,
#     '비통한': 23,
#     '상처': 24,
#     '성가신': 25,
#     '스트레스 받는': 26,
#     '슬픔': 27,
#     '신뢰하는': 28,
#     '신이 난': 29,
#     '실망한': 30,
#     '악의적인': 31,
#     '안달하는': 32,
#     '안도': 33,
#     '억울한': 34,
#     '열등감': 35,
#     '염세적인': 36,
#     '외로운': 37,
#     '우울한': 38,
#     '자신하는': 39,
#     '조심스러운': 40,
#     '좌절한': 41,
#     '죄책감의': 42,
#     '질투하는': 43,
#     '짜증내는': 44,
#     '초조한': 45,
#     '충격 받은': 46,
#     '취약한': 47,     
#     '툴툴대는': 48,
#     '편안한': 49,
#     '한심한': 50,
#     '혐오스러운': 51,
#     '혼란스러운': 52,
#     '환멸을 느끼는': 53,
#     '회의적인': 54,
#     '후회되는': 55,
#     '흥분': 56,
#     '희생된': 57, 
# }

# res = {}
# ret = []

# for i in d.items():
#     res[i[1]] = i[0]
#     ret.append(i[0])
# print(res)
# print(ret)

import requests
from bs4 import BeautifulSoup
import time
import tqdm

d = [
    'poor',
    'grateful',
    'worrisome'
    'isolated',
    'distressed',
    'nauseating',
    'Joy',
    'dejected',
    'self-conscious',
    'angry',
    'tearful',
    'easygoing',
    'baffling',
    'Panic',
'scared',
'paralyzed',
'satisfactory',
'defensive',
'betrayed',
'abandoned',
'Shameful',
'Anger',
'Anxiety',
'sorrowful',
'Wound',
'annoying',
'stressed-out',
'Sadness',
'trustworthy',
'excited',
'Disappointed',
'malicious',
'fretting',
'relief',
'unfair',
'complex',
'pessimistic',
'Lonely',
'Gloomy',
'confident',
'cautious',
'frustrated',
'guilty',
'Jealous',
'annoying',
'Nervous',
'shocked',
'weak',
'grumbling',
'Comfortable',
'pathetic',
'repulsive',
'confused',
'disillusioned',
'skeptical',
'regrettable',
'Excitement',
'victimized',
]

ret = []

LIMIT = 50

base =  'https://emojidb.org/'

pbar = tqdm.tqdm(d)
for word in pbar:
    url = f'{base}{word.lower()}-emojis'

    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    emojis = soup.find_all("div", "emoji")
    tmp = [emoji.text for emoji in emojis[:LIMIT]]
    ret.append(tmp)
    time.sleep(3)

with open('emojis.txt', 'w', encoding='UTF-8') as f:
    for line in ret:
        f.write('[')
        # f.writelines(line)
        for word in line:
            f.write(f'"{word}",')
        f.write('],\n')


# url = f'{base}{d[2].lower()}-emojis'

# url = 'https://emojidb.org/worrisome-emojis'

# res = requests.get(url)
# html = res.text
# soup = BeautifulSoup(html, 'html.parser')
# emojis = soup.find_all("div", "emoji")
# tmp = [emoji.text for emoji in emojis[:LIMIT]]

# with open('tmp.txt', 'w', encoding='UTF-8') as f:
#     f.write('[')
#     for word in tmp:
#         f.write(f'"{word}",')
#     f.write('],\n')