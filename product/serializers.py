# -*- coding: utf8 -*-

from rest_framework import serializers
from product.models import Product, UserProduct


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'bar_code', 'name', 'description', 'composition', 


class UserProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProduct
        fields = 'user', 'product', 'due_to', 'consumed', 
