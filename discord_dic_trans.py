# -*- coding: cp949 -*-
import discord
import re
import requests
import sys
from bs4 import BeautifulSoup
import googletrans

class chatbot(discord.Client):

    async def on_ready(self):

        game = discord.CustomActivity("내용")

        await client.change_presence(status=discord.Status.online, activity=game)

        print("READY")

    # 봇에 메시지가 오면 수행 될 액션

    async def on_message(self, message):

        # SENDER가 BOT일 경우 반응을 하지 않도록 한다.
        if message.author.bot:
            return None


        if re.match('trans:', message.content):
            channel = message.channel

            translator = googletrans.Translator()

            eng = re.findall('[a-zA-Z]', message.content[6:])
            kor = re.findall('[ㄱ-ㅎㅏ-ㅣ가-힣]', message.content[6:])

            if len(eng) > len(kor):

                msg = re.sub('[ㄱ-ㅎㅏ-ㅣ가-힣]',' ', message.content[6:])
                result1 = translator.translate(msg, dest='ko')

                await channel.send(msg)
                await channel.send('-->' + result1.text)

            else:

                msg = re.sub('[a-zA-Z]', ' ', message.content[6:])
                result1 = translator.translate(msg, dest='en')

                await channel.send(msg)
                await channel.send('-->' + result1.text)

            return None
        
        if re.match('dic\s?:\s?', message.content):

            url = "http://endic.naver.com/search.nhn?query="

            channel = message.channel

            eng = re.findall('[a-zA-Z]', message.content[4:])
            kor = re.findall('[ㄱ-ㅎㅏ-ㅣ가-힣]', message.content[4:])

            if len(eng) > len(kor):
                msg = re.sub('[ㄱ-ㅎㅏ-ㅣ가-힣]', '', message.content[4:])
            else:
                msg = re.sub('[a-zA-Z]', '', message.content[4:])


            url = "http://endic.naver.com/search.nhn?query=" + msg
            result =""
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "lxml")

            
            try:
                result += soup.find('dl', {'class': 'list_e2'}).find('dd').find('span', {'class': 'fnt_k05'}).get_text()
            except:
                result = "messadic 사전에 등재되어 있지 않습니다."
            
        
            await channel.send(result)
            return None


if __name__ == "__main__":
    
    # 객체를 생성
    client = chatbot()
    # TOKEN 값을 통해 로그인하고 봇을 실행
    client.run("ODgxMTcyMDk3Njg1MTU5OTQ2.YSo9dw.6lWAeVHOUrr2xP2CvjKIN6vhyQU")