import json

from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination

import requests
from .models import *
from .serializers import *
import os
import uuid

class ItemsPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 10000

    def get_paginated_response(self, data):
        return Response({
            'links':{
                'next': self.get_next_link(),
                'prev': self.get_previous_link(),
            },
            'page_count':self.page.paginator.num_pages,
            'results':data
        })


class Del(APIView):
    def get(self,request):
        list=self.request.query_params.get('list').split(',')
        print(list)
        for i in list:
            ii = int(i)
            try:
                Perk.objects.get(id=ii).delete()
            except:
                pass
        return Response(status=200)


class GetItem(generics.RetrieveAPIView):
    serializer_class = ItemSerializer
    def get_object(self):
        try:
            item = Item.objects.filter(name_slug=self.request.query_params.get('slug'))[0]
        except:
            item = Item.objects.filter(name_slug=self.request.query_params.get('slug'))
        return item
class GetItems(APIView):
    pagination_class = ItemsPagination

    def get(self, request):
        items = None

        if request.GET.get('type') == 'a':
            items = Item.objects.all()

        if request.GET.get('type') == 's':
            items = Item.objects.filter(subcategory__name_slug=request.GET.get('s'))

        page = self.paginate_queryset(items)
        if page is not None:
            serializer = ItemSerializer(page, many=True, context={'request': request})

            return self.get_paginated_response(serializer.data)

    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)


class GetCategory(generics.ListAPIView):
    serializer_class = ItemCategorySerializer
    queryset = ItemCategory.objects.all()


class GetSubCategory(generics.ListAPIView):
    serializer_class = ItemSubCategorySerializer
    queryset = ItemSubCategory.objects.all()


# item icon https://cdn.nwdb.info/db/v2/icons/items/weapon/1hlongsword_widowmakert5.png
# item image https://cdn.nwdb.info/db/v2/icons/items_hires/1hlongsword_widowmakert5.png
# item info https://nwdb.info/db/item/1hlongsword_corallasht5.json
# perk info https://nwdb.info/db/perk/perkid_gem_voiddmg4.json

def get_image(url,path,filename):
    headers_img = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    response = requests.get(url, headers=headers_img)
    try:
        os.mkdir(f'media/{path}')
    except:
        print('dir exist')

    with open(f'media/{path}/{filename}', 'wb') as f:
        f.write(response.content)


def get_perk_info(id):
    url = f'https://nwdb.info/db/perk/{id}.json'
    responce = requests.get(url)
    item = Item.objects.all().first()
    perk=responce.json()['data']
    perk_type, created_type = PerkType.objects.get_or_create(name=perk['PerkType'], name_en=perk['PerkType'],
                                                             internal_id=perk['PerkType'])
    perk_item, created_perk = Perk.objects.get_or_create(
        type=perk_type,
        name=perk['name'],
        name_en=perk['name'],
        description=perk['description'],
        description_en=perk['description'],
        tier=perk['tier'],
        rarity=perk['rarity'],
        scalingPerGearScore=perk['ScalingPerGearScore'],
        # fishRarityRollModifier=perk['FishRarityRollModifier'],
        # fishSizeRollModifier=perk['FishSizeRollModifier'],
        dayPhases=perk['DayPhases'],
        fishingWaterType=perk['FishingWaterType'],
        defaults={'internal_id': perk['id']})

    return perk_item, created_perk


def get_item_info(id,hasRandomPerks,can_be_crafted,quest_reward,category):
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
    url = f'https://nwdb.info/db/item/{id}.json'
    responce = requests.get(url,headers)
    data = responce.json()['data']
    item_subcategory, created = ItemSubCategory.objects.get_or_create(name=data['typeName'], name_en=data['typeName'],
                                                                      internal_id=data['typeName'])
    weightClass = None
    baseDamage = None
    staggerDamage = None
    critChance = None
    critDamageMultiplier = None
    blockStaminaDamage = None
    blockStability = None

    try:
        weightClass=data['weightClass']
    except:
        print('weightClass not exist')

    try:
        baseDamage = data['baseDamage']
    except:
        print('baseDamage not exist')

    try:
        staggerDamage = data['staggerDamage']
    except:
        print('staggerDamage not exist')

    try:
        critChance = data['CritChance']
    except:
        print('CritChance not exist')

    try:
        critDamageMultiplier = data['CritDamageMultiplier']
    except:
        print('CritDamageMultiplier not exist')

    try:
        blockStaminaDamage = data['BlockStaminaDamage']
    except:
        print('BlockStaminaDamage not exist')

    try:
        blockStability = data['BlockStability']
    except:
        print('BlockStability not exist')



    item,created = Item.objects.get_or_create(
        category=category,
        subcategory=item_subcategory,
        name=data['name'],
        name_en=data['name'],
        internal_id=data['id'],
        icon_id=data['icon'],
        description=data['description'],
        description_en=data['description'],
        tier=data['tier'],
        rarity=data['rarity'],
        namedItem=data['namedItem'],
        gearScore=data['gearScore'],
        gearScoreMin=data['gearScoreMin'],
        gearScoreMax=data['gearScoreMax'],
        baseDamage=baseDamage,
        staggerDamage=staggerDamage,
        critChance=critChance,
        critDamageMultiplier=critDamageMultiplier,
        blockStaminaDamage=blockStaminaDamage,
        blockStability=blockStability,
        weight=data['weight'],
        level=data['level'] if data['level'] else 0,
        bindOnPickup=data['bindOnPickup'] if data['bindOnPickup'] else False,
        bindOnEquip=data['bindOnEquip'] if data['bindOnEquip'] else False,
        durability=data['durability'],
        hasRandomPerks=hasRandomPerks,
        can_be_crafted=can_be_crafted,
        quest_reward=quest_reward,
        weightClass=weightClass,
        defaults={'internal_id': data['id']}
    )
    if created:
        print('item created')
        item_icon = uuid.uuid4()
        item_full = uuid.uuid4()
        get_image(f'https://cdn.nwdb.info/db/v2/icons/items/{data["itemType"]}/{data["icon"].lower()}.png',
                  f'images/items/icons', f'{item_icon}.png')
        get_image(f'https://cdn.nwdb.info/db/v2/icons/items_hires/{data["icon"].lower()}.png', f'images/items/full',
                  f'{item_full}.png')
        item.icon = f'images/items/icons/{item_icon}.png'
        item.image = f'images/items/full/{item_full}.png'
        item.save()
        try:
            for attr in data['AttributeScale']:
                ItemAttributeScale.objects.create(
                    item=item,
                    attribute=attr['attribute'],
                    value=attr['scale']
                )
        except:
            print('AttributeScale not exist')

    if created:
        for perk in data['perks']:
            print(perk['type'])
            perk_item, created_perk = get_perk_info(perk['id'])
            if perk['type'] == 'Inherent':
                if created_perk:
                    get_image(f'https://nwdb.info/images/db/icon_attribute_arrow.png', f'images/items/perks',
                              f'icon_attribute_arrow.png')
                    perk_item.icon = f'images/items/perks/icon_attribute_arrow.png'
                    perk_item.is_perk_with_attributes = True
                    for attr in perk['attributes']:
                        # https://nwdb.info/images/db/icon_attribute_arrow.png
                        # https://cdn.nwdb.info/db/v2/icons/items/resource/topazcutt3.png
                        # https://cdn.nwdb.info/db/v2/icons/perks/rally1.png
                        # value = attr['value'] if attr['value'].isdecimal() else None,
                        # values = attr['value'] if not attr['value'].isdecimal() else None
                        try:
                            PerkAttribute.objects.create(
                                perk=perk_item,
                                attribute=attr['id'],
                                value=attr['value'],
                                values=attr['value']
                            )
                        except:
                            pass
            if perk['type'] == 'Generated':
                if created_perk:
                    icon = uuid.uuid4()
                    perk_filename = perk['icon'].split('/')[::-1][0].lower()
                    get_image(f'https://cdn.nwdb.info/db/v2/icons/perks/{perk_filename}.png', f'images/items/perks',
                              f'{icon}.png')
                    perk_item.icon = f'images/items/perks/{icon}.png'
            if perk['type'] == 'Gem':
                if created_perk:
                    icon = uuid.uuid4()
                    perk_filename = perk['icon'].split('/')[::-1][0].lower()
                    get_image(f'https://cdn.nwdb.info/db/v2/icons/items/resource/{perk_filename}.png',
                              f'images/items/perks',
                              f'{icon}.png')
                    perk_item.icon = f'images/items/perks/{icon}.png'
            perk_item.save()
            item.perks.add(perk_item)





    print(data['id'])


class ParseItems(APIView):
    def get(self,request):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        category = 'resources'
        #category = 'armors'
        item_category, created = ItemCategory.objects.get_or_create(name='Resources', name_en='resources', internal_id='resources')

        url = f'https://nwdb.info/db/items/{category}/page/1.json'
        responce_page_count = requests.get(url,headers=headers)
        pages = responce_page_count.json()['pageCount']


        for page in range(1,pages+1):
            print(f'-----------------------------page {page} -------------------')
            url = f'https://nwdb.info/db/items/{category}/page/{page}.json'
            responce = requests.get(url,headers=headers)
            pageData = responce.json()['data']
            for data in pageData:
                get_item_info(data['id'],data['hasRandomPerks'],data['flagCanBeCrafted'],data['flagQuestReward'],item_category)
        return Response(status=200)
