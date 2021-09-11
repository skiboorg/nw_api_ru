import json
from random import choices
import string
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from .serializers import *
from .models import *
from bs4 import BeautifulSoup
import requests

from googletrans import Translator

class GetWeapons(generics.ListAPIView):
    serializer_class = WeaponsSerializer
    queryset = Weapon.objects.all()

class GetCharacteristics(generics.ListAPIView):
    serializer_class = CharacteristicSerializer
    queryset = Characteristic.objects.all()

class GetWeapon(generics.RetrieveAPIView):
    serializer_class = WeaponSerializer

    def get_object(self):
        return Weapon.objects.get(name_slug=self.request.query_params.get('slug'))


class Builds(APIView):
    def post(self, request):
        data = request.data
        print(data)
        name_slug = ''.join(choices(string.ascii_lowercase + string.digits, k=8))
        Build.objects.create(
            weapon1_id=data['weapon1'],
            weapon2_id=data['weapon2'],
            name_slug=name_slug,
            checked_skills_left_w1=data['checked_skills_left_w1'],
            checked_skills_right_w1=data['checked_skills_right_w1'],
            checked_skills_left_w2=data['checked_skills_left_w2'],
            checked_skills_right_w2=data['checked_skills_right_w2'],
            description=data['description'],
            name=data['name'],
            is_private=data['is_private'],
            purpose=data['purpose'],
            role=data['role'],
            characteristics=data['characteristics']
        )
        return Response({'slug':name_slug},status=200)
    def get(self,request):
        print(self.request.query_params.get('for'))
        slug = self.request.query_params.get('slug')
        if self.request.query_params.get('for') == 'build':
            try:
                build = Build.objects.get(name_slug=slug)
                seriarizer = BuildSerializer(build, many=False)
                return Response(seriarizer.data, status=200)
            except:
                return Response(status=404)
        if self.request.query_params.get('for') == 'index':
            build = Build.objects.filter(is_active=True, is_private=False)[:3]
            seriarizer = BuildShortSerializer(build, many=True)
            return Response(seriarizer.data, status=200)
        if self.request.query_params.get('for') == 'all':
            build = Build.objects.filter(is_active=True, is_private=False)[:30]
            seriarizer = BuildShortSerializer(build, many=True)
            return Response(seriarizer.data, status=200)



class ParceHtml(APIView):
    def get(self,request):

        translator = Translator()

        # data = '{"yandexPassportOauthToken":"AgAAAABQDeFrAATuwSGnF2oKw0vmjJeaO4iggoE"}'
        # response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', data=data)
        # key = response.json().get('iamToken')
        # print(key)
        key = 't1.9euelZrOy5eej4ycjYuOyoyOj8-RjO3rnpWazcjMkJbLx5DLnpeYkovOkovl9PdWN3h5-e8Calzc3fT3FmZ1efnvAmpc3A.AFuNddlRWioLJwKFB2tpM3mxJ_QQiZpaJJVS6RamVYdtg-8mZaJm1tCUb70NFNsqYnj8m_-Ee0JbVtFY1uRTDQ'

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {key}",
        }

        with open("t.html", "r") as f:
            contents = f.read()

        page_content = BeautifulSoup(contents, 'lxml')
        trees = page_content.find_all('div','skl-tree')
        for tree in trees:

            tree_name = tree.find('div','tpl-ttl').text

            data = {
                "folder_id": "b1grf2b1imq40far6803",
                "texts": [f"{tree_name}", ],
                "targetLanguageCode": "ru"
            }

            response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                     headers=headers,
                                     data=json.dumps(data))
            print(response.json())
            message_translate = response.json().get('translations')[0]['text']
            print(message_translate)


            skillTree = SkillTree.objects.create(name_en=tree_name,name=message_translate,weapon_id=8)

            rows = tree.find_all('div','skl-row')
            r = 1
            for row in rows:
                cols = row.find_all('div','skl-cell')
                c = 1
                for col in cols:


                    try:
                        img_url = col.find('img').attrs['src']

                        img_name = f'images/skill/{img_url.split("/")[::-1][0]}'
                        skill_name = col.find('span').attrs['data-tip-ttl']
                        skill_descr = col.find('span').attrs['data-tip-txt']

                        data = {
                            "folder_id": "b1grf2b1imq40far6803",
                            "texts": [f"{skill_descr}", ],
                            "targetLanguageCode": "ru"
                        }

                        response = requests.post('https://translate.api.cloud.yandex.net/translate/v2/translate',
                                                 headers=headers,
                                                 data=json.dumps(data))
                        message_translate = response.json().get('translations')[0]['text']
                        print(message_translate)



                        headers_img = {
                            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
                        response = requests.get(img_url,headers=headers_img)

                        with open('temp/' + img_url.split('/')[::-1][0], 'wb') as f:
                            f.write(response.content)

                        Skill.objects.create(
                            tree=skillTree,
                            name_en=skill_name,
                            description=message_translate,
                            description_en=skill_descr,
                            image=img_name,
                            row=r,
                            col=c
                        )
                    except:
                        print('empty', r, c)
                        Skill.objects.create(
                            tree=skillTree,
                            row=r,
                            col=c,
                            is_empty=True
                        )
                    c += 1
                r += 1
        return Response(status=200)


class AddFeedback(APIView):
    def post(self, request):
        data = request.data
        print(data)
        build = Build.objects.get(id=data['build_id'])
        build.total_rating += data['rating']
        build.votes += 1
        build.save()
        BuildFeedback.objects.create(
            user=request.user,
            build=build,
            text=request.data.get('text'),
            value=request.data.get('rating')
        )
        return Response(status=200)

class BuildsCorrect(APIView):
    def get(self, request):
        buids = Build.objects.all()
        for build in buids:
            build.role = 'Не указана'
            build.save()
        return Response(status=200)

class BuildsFilter(APIView):
    def post(self, request):
        data = request.data
        first_weapon = None
        second_weapon = None
        try:
            first_weapon=Weapon.objects.get(name=data.get('build_first_weapon'))
        except:
            pass
        try:
            second_weapon=Weapon.objects.get(name=data.get('build_second_weapon'))
        except:
            pass
        #print(first_weapon)
        #print(second_weapon)
        filter_builds = Build.objects.filter(role=data.get('build_role'),
                                             purpose=data.get('build_purpose'),
                                             is_private=False)

        if first_weapon:
            filter_builds = filter_builds.filter(weapon1=first_weapon)
        if second_weapon:
            filter_builds = filter_builds.filter(weapon2=second_weapon)
        #print(filter_builds)
        seriarizer = BuildShortSerializer(filter_builds, many=True)
        return Response(seriarizer.data, status=200)