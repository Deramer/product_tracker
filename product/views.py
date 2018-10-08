# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests

from django.http import HttpResponseBadRequest

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
            if soup.find(id='ctl00_ContentPH_GoodsName').text:
                name = soup.find(id='ctl00_ContentPH_GoodsName').text
                description = soup.find(id='ctl00_ContentPH_Comment').text
                composition = soup.find(id='ctl00_ContentPH_Composition').text
                product = Product(name=name, bar_code=bar_code, description=description, composition=composition)
                product.save()
                return Response(ProductSerializer(instance=product).data)
            else:
                return HttpResponseBadRequest('No such bar code in database')

