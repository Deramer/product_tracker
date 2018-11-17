# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import json
from os.path import join

from django.http import HttpResponseBadRequest, JsonResponse
from django.conf import settings
from django.views.generic import View

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route

from product.serializers import ProductSerializer, UserProductSerializer
from product.models import Product, UserProduct


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    @list_route(methods=('get', ))
    def bar(self, request):
        bar_code = self.request.query_params.get('bar', '')
        if not bar_code:
            return HttpResponseBadRequest('No bar code in get parameters')
        products = Product.objects.filter(bar_code=bar_code)
        if products:
            return Response(ProductSerializer(instance=products[0]).data)
        else:
            url = 'http://goodsmatrix.ru/goods/d/' + bar_code + '.html'
            resp = requests.get(url)
            soup = BeautifulSoup(resp.text)
            if soup.find(id='ctl00_ContentPH_GoodsName'):
                name = soup.find(id='ctl00_ContentPH_GoodsName').text
                description = soup.find(id='ctl00_ContentPH_Comment').text
                composition = soup.find(id='ctl00_ContentPH_Composition').text
                image_url = 'http://goodsmatrix.ru/BigImages/' + bar_code + '.jpg'
                img = requests.get(image_url)
                path = join(settings.MEDIA_ROOT, 'big_images', bar_code + '.jpg')
                with open('/tmp/food_debug', 'w') as outp:
                    outp.write(path)
                with open(path, 'wb') as img_file:
                    img_file.write(img.content)
                product = Product(name=name, bar_code=bar_code, description=description, composition=composition)
                product.image.name = path
                product.save()
                return Response(ProductSerializer(instance=product).data)
            else:
                return HttpResponseBadRequest('No such bar code in database')

class PromocodeView(View):

    def get(self, request, *args, **kwargs):
        resp = requests.get('https://7days.ru/promokodi/perekrestok-promokod')
        soup = BeautifulSoup(resp.text)
        ids = [x['data-gtm-voucher-id'] for x in soup.findAll('div', {'class': 'sevendaysru-new-voucher'})]
        results = []
        for id in ids:
            resp = requests.get('https://7days.ru/promokodi/ajax/voucherpopup?id=' + id)
            data = json.loads(resp.text)
            results.append({
                'url': data['voucher']['affiliate_url'],
                'desc': data['voucher']['description'],
                'title': data['voucher']['title'],
                'code': data['voucher']['code'],
            })
        return JsonResponse({'promocodes': results})
