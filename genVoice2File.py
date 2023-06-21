token = '24dc31d7baeaec48c00cb3b96889e36e'
email = 'alex997@list.ru'
urlApi = 'https://zvukogram.com/index.php?r=api/longtext'
urlResult = 'https://zvukogram.com/index.php?r=api/result'

emotion = ['good',  'evil', 'neutral']
emotionPeople = ['Филипп new','Эрмил new','Филипп','Омаж','Омажа new', 'Мария', 'Мартын', 'Оксана', 'Джейн', 'Алена', 'Эрмил', 'Джейн new','Захар', 'Оксана new', 'Захар new']
otherPeople = []

import requests
from time import sleep
import json
import random
import winsound

Peoples = []

def genVoice2(text: str, nameFile : str) -> str:
    with open('voice\\voice.json', encoding="utf8") as json_file:
        data = json.load(json_file)
        Peoples = [i["voice"] for i in data["Русский"]]
        #print(Peoples)

    if len(Peoples)==0:
        return 'error1'
    voice = random.choice(Peoples)
    emot = 'good'
    if voice in emotionPeople:
        emot = random.choice(emotion)
    params={'token': f'{token}', 'email':f'{email}',
                'voice': f'{voice}', 'text': text,
                'format':'wav', 'speed': 1.1, 
            'pitch': 0.8,   
            'emotion': f'{emot}',
                }

    response = requests.get(
        urlApi,
        params 
    )

    #res = requests.post('https://httpbin.org/post', data=urlApi)
    #print(res.text)

    if  response.status_code != 200:
        return 'error'
    if response.status_code == 200:
        response.encoding = 'utf-8'
        responsejson = response.json()
        
        if responsejson['status'] == 1:
            idResponse = responsejson['id']
            
            responsejsonResult = {'status': 0}

            varsleep = 0

            while responsejsonResult['status'] == 0:
                params= {'token': f'{token}', 'email':f'{email}', 'id' : idResponse}
                response = requests.get(
                    urlResult,
                    params 
                )
                sleep(0.01)

                varsleep += 0.01
                #print(varsleep)
                if varsleep>0.9:
                    return 'error time'

                responsejsonResult = response.json()

            #print(responsejsonResult['file'])
            if len(responsejsonResult['file'])==0:

                return 'error getFile'
                #genVoice2(text)
                #genVoice2(text,nameFile)

                
            urlFile = responsejsonResult['file']

            try:
                myfile = requests.get(urlFile)
            except:
                pass
                #return 'error2'
            status = 1
            while status:
                if response.status_code == 200:
                    try:
                        open(f'voice\\{nameFile}.wav', 'wb').write(myfile.content)
                        #winsound.PlaySound(f'voice\\{nameFile}.wav', winsound.SND_FILENAME)
                        status = 0
                        return 'norm'
                    except:
                        return 'norm'
                        #return 'error3'

import os
print()
for x in os.listdir(path='.\\files'):
    if x.endswith(".txt"):
        name = x.split('.')[:-1][0]
        with open('.\\files\\'+x, encoding="utf-8") as f:
            lines = f.readlines()
            text = '\n'.join(lines)
        if not name+'.wav' in os.listdir('.\\voice'):
            print(f'file: {x} -- {genVoice2(text,name)}')

print('Все файлы готовы')
         #print(genVoice2('Вот это текст','Метопролол'))
#print(genVoice2('текст'))


