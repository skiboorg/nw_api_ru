from django.shortcuts import render

import json
from pytils.translit import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from bs4 import BeautifulSoup
import requests


class GetTexts(generics.RetrieveAPIView):
    serializer_class = TextsSerializer
    def get_object(self):
        return Texts.objects.all().first()



class AddFb(APIView):
    def post(self, request):
        data = request.data
        Feedback.objects.create(user=data['fb_user'],text=data['fb_text'])
        return Response(status=200)
class Craft(APIView):
    def get(self, request):
        main_url = 'https://newworldfans.com/crafting/Arcana?tier='

        page_response = requests.get(main_url, timeout=5)
        page_content = BeautifulSoup(page_response.content, "lxml")
        item_table = page_content.find('table')

        total_pages = len(page_content.find_all('ul',{"class": "pagination-list"})[::-1][0].find_all('li'))
        rows = item_table.find_all('tr')[1::]

        items = []
        for row in rows:
            item = []
            td_s = row.find_all('td')
            i = 0
            item_image = ''
            item_name = ''
            item_category = ''
            item_subcategory = ''
            item_ingridients = ''
            item_tier = ''
            item_level = ''
            for td in td_s:
                if i == 0:  # image
                    item.append(td.find('img').attrs['src'])
                if i == 1:  # name
                    item.append(td.find('span').text)
                if i == 2:  # Category
                    item.append(td.text.replace('\n','').replace('Category:','').replace(' ',''))
                if i == 3:  # SubCategory
                    item.append(td.text.replace('\n','').replace('SubCategory:','').replace(' ',''))
                if i == 4:  # Ingrid
                    ingr_count=td.text.replace('\n','').split('x')[:-1]
                    print('-----')
                    i=0
                    for a in td.find_all('a'):
                        print(ingr_count[i])
                        print(a.attrs['data-tooltip'])
                        print(a.find('img').attrs['src'])
                        i+=1
                    print('-----')
                i += 1
            items.append(item)
        print(total_pages)
        return Response(items, status=200)

class Item(APIView):
    def get(self,request):
        main_url = 'https://newworldfans.com/db?page=1&rarity=&tier='

        page_response = requests.get(main_url, timeout=5)
        page_content = BeautifulSoup(page_response.content, "lxml")
        item_table = page_content.find('table')
        rows = item_table.find_all('tr')[1::]
        items=[]
        for row in rows:
            item=[]
            td_s = row.find_all('td')
            i=0
            item_image = ''
            item_rarity = ''
            item_name = ''
            item_slot = ''
            item_type = ''
            item_tier = ''
            item_gs = ''
            item_level = ''
            item_bop = ''
            item_craft = ''
            for td in td_s:
                if i == 0: #image
                    item.append(td.find('img').attrs['src'])
                    item.append(td.find('div').attrs['class'][0].replace('-frame',''))
                    item_rarity = td.find('div').attrs['class'][0].replace('-frame','')
                    item_image = td.find('img').attrs['src']
                    # response = requests.get(item_image)
                    # if response.status_code == 200:
                    #     with open('temp/' + item_image.split('/')[::-1][0], 'wb') as f:
                    #         f.write(response.content)
                if i == 1: #name
                    item.append(td.find('span').text)
                    item_name = td.find('span').text
                    item.append(slugify(item_name))
                if i == 2: #slot
                    item.append(td.text.replace('\n','').replace('Slot:','').replace(' ',''))
                    item_slot = td.text.replace('\n','').replace('Slot:','').replace(' ','')
                if i == 3:  # type
                    item.append(td.text.replace('\n', '').replace('Type:', '').replace(' ', ''))
                    item_type = td.text.replace('\n', '').replace('Type:', '').replace(' ', '')
                if i == 4:  # tier

                    item_tier = td.text.replace('\n', '').replace('Tier:', '').replace(' ', '')
                    try:
                        item_tier = int(td.text.replace('\n', '').replace('Tier:', '').replace(' ', ''))
                    except:
                        item_tier = 0
                    item.append(item_tier)
                if i == 5:  # gs
                    item.append(td.text.replace('\n', '').replace('Gear Score:', '').replace(' ', ''))
                    item_gs= td.text.replace('\n', '').replace('Gear Score:', '').replace(' ', '')
                if i == 6:  # level
                    try:
                        item_level = int(td.text.replace('\n', '').replace('Level:', '').replace(' ', ''))
                    except:
                        item_level = 0
                    item.append(item_level)
                if i == 7:  # bop

                    item_bop = True if td.text.replace('\n', '').replace('Bind on Pickup:', '').replace(' ', '') == 'Yes' else False
                    item.append(item_bop)
                if i == 8:  # craft

                    item_craft = td.text.replace('\n', '').replace('Crafted by:', '').replace(' ', '')
                    item.append(slugify(item_craft))



                i += 1
            items.append(item)


        return Response(items,status=200)


class GetBanner(generics.ListAPIView):
    serializer_class = BannerSerializer
    queryset = Banner.objects.all()


class GetFaq(generics.ListAPIView):
    serializer_class = FaqSerializer
    queryset = Faq.objects.all()

class GetSocial(generics.ListAPIView):
    serializer_class = SocialItemSerializer
    queryset = SocialItem.objects.all()