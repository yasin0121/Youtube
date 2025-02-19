from django.shortcuts import render, get_object_or_404, redirect
from video.models import  Category,VIDEO
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import CategorySerializer,VideoSerializer,CreateVideoSerializer
from rest_framework import status

# View for the home page
@api_view(['GET','POST'])
def home_video(request):
  if request.method == "GET":
    data = VIDEO.objects.all()
    Video_Serializer =  VideoSerializer(data,many=True)
    return Response(Video_Serializer.data)
  if request.method == "POST":
    REQ_data  = request.data
    Serializer = CreateVideoSerializer(data=REQ_data)
    Serializer.is_valid(raise_exception=True)
    Serializer.seve()
    return Response(Serializer.data,status=201)
    
@api_view(['PUT'])
def update_video(request,id):
  video_obj = VIDEO.objects.get(id=id)

  Serializer = VideoSerializer(
    isinstance=video_obj,
    data=request.data,
    )
  Serializer.is_valid(raise_exception=True)

  Serializer.save()

  return Response(Serializer.data,status=200) 
