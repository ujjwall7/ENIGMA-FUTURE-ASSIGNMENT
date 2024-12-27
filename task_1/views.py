from django.shortcuts import render
from rest_framework.views import APIView
from.serializers import *
from.models import *
from rest_framework.response import Response
from rest_framework import status


class ServiceRecordView(APIView):

    def get(self,request):    
        data = ServiceRecord.objects.all()
        serializer = ServiceRecordSerializer(data, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ServiceRecordSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg' : 'Service Record Sumbitted Successfully',
                'status': status.HTTP_201_CREATED
            })
