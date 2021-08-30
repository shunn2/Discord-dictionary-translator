# -*- coding: cp949 -*-
import discord
import re
import requests
import sys
from bs4 import BeautifulSoup
import googletrans

class chatbot(discord.Client):

    async def on_ready(self):

        game = discord.CustomActivity("����")

        await client.change_presence(status=discord.Status.online, activity=game)

        print("READY")

    # ���� �޽����� ���� ���� �� �׼�

    async def on_message(self, message):

        # SENDER�� BOT�� ��� ������ ���� �ʵ��� �Ѵ�.
        if message.author.bot:
            return None


        if re.match('trans:', message.content):
            channel = message.channel

            translator = googletrans.Translator()

            eng = re.findall('[a-zA-Z]', message.content[6:])
            kor = re.findall('[��-����-�Ӱ�-�R]', message.content[6:])

            if len(eng) > len(kor):

                msg = re.sub('[��-����-�Ӱ�-�R]',' ', message.content[6:])
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
            kor = re.findall('[��-����-�Ӱ�-�R]', message.content[4:])

            if len(eng) > len(kor):
                msg = re.sub('[��-����-�Ӱ�-�R]', '', message.content[4:])
            else:
                msg = re.sub('[a-zA-Z]', '', message.content[4:])


            url = "http://endic.naver.com/search.nhn?query=" + msg
            result =""
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "lxml")

            
            try:
                result += soup.find('dl', {'class': 'list_e2'}).find('dd').find('span', {'class': 'fnt_k05'}).get_text()
            except:
                result = "messadic ������ ����Ǿ� ���� �ʽ��ϴ�."
            
        
            await channel.send(result)
            return None


if __name__ == "__main__":
    
    # ��ü�� ����
    client = chatbot()
    # TOKEN ���� ���� �α����ϰ� ���� ����
    client.run("ODgxMTcyMDk3Njg1MTU5OTQ2.YSo9dw.6lWAeVHOUrr2xP2CvjKIN6vhyQU")