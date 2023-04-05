from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from accInfo.serializer import savedResultSerializer
from accInfo.models import savedResult


@api_view(['POST'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def saveResult(request):
    # Use request.data['data'] instead of request.data
    data = request.data['data']
    data['user'] = request.user.id
    serializer = savedResultSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    else:
        return Response(serializer.errors, status=400)

