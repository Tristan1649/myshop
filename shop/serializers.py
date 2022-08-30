from dataclasses import field
from operator import mod
from pyexpat import model
from unicodedata import category
from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'price']