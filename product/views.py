# -*- coding: utf-8 -*-

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
        products = Product.objects.filter(bar_code=self.request.query_params.get('bar', ''))
        if products:
            return Response(ProductSerializer(instance=products[0]).data)
