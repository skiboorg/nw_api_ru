import json
from pytils.translit import slugify
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from bs4 import BeautifulSoup
import requests
import shutil
import  os
class ParceMap(APIView):
    def get(self,request):

        for tile in range(7,8):
            print(tile)
            os.mkdir(f'media/map/{tile}')
            for y in range(0, (tile+1)*10):
                for x in range(0, 70):
                    print('y=', y)
                    print('x=', x)
                    url = f'https://newworldfans.com/tiles/{tile}/map_y-{y}_x{x}.jpg'

                    responce = requests.get(url, stream=True)
                    print('responce.status_code=', responce.status_code)
                    if responce.status_code == 200:
                        with open(f'media/map/{tile}/map_y-{y}_x{x}.jpg', 'wb') as out_file:
                            shutil.copyfileobj(responce.raw, out_file)

        return Response(status=200)
class ParcePoi(APIView):
    def get(self,request):
        key = 't1.9euelZqLnpOUkYybi53PyJjKyZuMku3rnpWazcjMkJbLx5DLnpeYkovOkovl9PdmQgF4-e9UYSLz3fT3JnF-d_nvVGEi8w.bOAlto-xkC1uK4skQVJVb5YQ_eY1xXCcRCLSZqcGSUq09Ri1_9PRH-OBHi1p8x9AqOAipYpAV20FwNEopaSnBQ'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {key}",
        }
        Poi.objects.all().delete()
        url = 'https://newworldfans.com/api/v1/map/resource'
        responce = requests.get(url)
        for i in responce.json():
            description_tr = ''
            name_tr = ''
            if i['category'] == 'poi':
                data = {
                    "folder_id": "b1grf2b1imq40far6803",
                    "texts": [i['description'].replace('\n\n',' ').replace('\n',' '), ],
                    "targetLanguageCode": "ru"
                }

                response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                         headers=headers,
                                         data=json.dumps(data))

                description_tr = response.json().get('translations')[0]['text']
                print(description_tr)
                data = {
                    "folder_id": "b1grf2b1imq40far6803",
                    "texts": [f"{i['name']}", ],
                    "targetLanguageCode": "ru"
                }

                response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                         headers=headers,
                                         data=json.dumps(data))

                name_tr = response.json().get('translations')[0]['text']
                print(name_tr)


                # headers_img = {
                #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                # response = requests.get(f'https://cdn.newworldfans.com/map_images/icon/pois/{i["resource_icon"].lower()}.png', headers=headers_img)
                #
                # with open(f'media/icons/poi/{i["resource_icon"].lower()}.png', 'wb') as f:
                #     f.write(response.content)

                Poi.objects.create(
                                    name=name_tr,
                                    name_en=i['name'],
                                   image=f'icons/poi/{i["resource_icon"].lower()}.png',
                                   level=i['level_range'],
                                   description=description_tr,
                                   description_en=i['description'].replace('\n\n',' ').replace('\n',' '),
                                   lat=i['lat'],
                                   lng=i['lng'],
                                   )

        return Response(status=200)

class ParceResource(APIView):
    def get(self,request):

        key = 't1.9euelZqLnpOUkYybi53PyJjKyZuMku3rnpWazcjMkJbLx5DLnpeYkovOkovl9PdmQgF4-e9UYSLz3fT3JnF-d_nvVGEi8w.bOAlto-xkC1uK4skQVJVb5YQ_eY1xXCcRCLSZqcGSUq09Ri1_9PRH-OBHi1p8x9AqOAipYpAV20FwNEopaSnBQ'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {key}",
        }

        ResourceCategory.objects.all().delete()
        Resource.objects.all().delete()
        img_urls = ['https://cdn.newworldfans.com/map_images/icon/',
                    'https://cdn.newworldfans.com/map_images/icon/npcs/',
                    'https://cdn.newworldfans.com/map_images/icon/gatherables/']
        url = 'https://newworldfans.com/api/v1/map/resource'
        responce = requests.get(url)

        for i in responce.json():
            if i['category'] != 'poi':
                description_tr=''
                cat_tr=''
                if i['description']:
                    data = {
                        "folder_id": "b1grf2b1imq40far6803",
                        "texts": [i['description'].replace('\n\n',' ').replace('\n',' ') ],
                        "targetLanguageCode": "ru"
                    }

                    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                             headers=headers,
                                             data=json.dumps(data))
                    print(response.json())
                    description_tr = response.json().get('translations')[0]['text']
                    print(description_tr)


                cat,create = ResourceCategory.objects.get_or_create(name_slug=i['category'])
                if create:
                    data = {
                        "folder_id": "b1grf2b1imq40far6803",
                        "texts": [f"{i['category']}", ],
                        "targetLanguageCode": "ru"
                    }

                    response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                             headers=headers,
                                             data=json.dumps(data))
                    print(response.json())
                    cat_tr = response.json().get('translations')[0]['text']
                    print(description_tr)
                    # for url in img_urls:
                    #     headers_img = {
                    #         'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                    #     response = requests.get(f'{url}{i["resource_icon"].lower()}.png', headers=headers_img)
                    #     print(response.status_code)
                    #     with open(f'media/icons/{i["resource_icon"].lower()}.png', 'wb') as f:
                    #         f.write(response.content)

                    cat.name=cat_tr
                    cat.name_en=i['category'].capitalize()
                    cat.name_slug=i['category']
                    cat.image = f'icons/{i["resource_icon"].lower()}.png'

                    cat.save()
                try:
                    Resource.objects.create(category=cat,
                                            lat=i['lat'],
                                            name=i['name'],
                                            level=i['level_range'],
                                            description=description_tr,
                                            description_en=i['description'].replace('\n\n',' ').replace('\n',' '),
                                            lng=i['lng'],
                                            )
                except:
                    Resource.objects.create(category=cat,
                                            lat=i['lat'],
                                            name=i['name'],
                                            level='',
                                            description=description_tr,
                                            description_en=i['description'].replace('\n\n',' ').replace('\n',' '),
                                            lng=i['lng'],
                                            )
        return Response(status=200)

class GetPoi(generics.ListAPIView):
    serializer_class = PoiSerializer
    queryset = Poi.objects.all()

class GetResourse(generics.ListAPIView):
    serializer_class = ResourceTypeSerializer
    queryset = ResourceType.objects.all()

