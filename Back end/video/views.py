from django.shortcuts import render, get_object_or_404, redirect
from .models import  Category,VIDEO
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import CategorySerializer,VideoSerializer,CreateVideoSerializer
from rest_framework import status

# View for the home page
    
