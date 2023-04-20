from django.shortcuts import render

# Create your views here.
from django.conf import settings
from django.contrib.auth.models import User
from django.http import Http404

from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from accInfo.serializer import savedResultSerializer, MyHistorySerializer
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
    
class historyList(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        history = savedResult.objects.filter(user=request.user)
        serializer = MyHistorySerializer(history, many=True)
        print(serializer.data)
        return Response(serializer.data)
    

class historyDetails(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        id = self.kwargs['id']
        history = savedResult.objects.filter(user=request.user,id=id)
        serializer = MyHistorySerializer(history, many=True)
        return Response(serializer.data)
    
    def delete(self, request, *args, **kwargs):
        id = self.kwargs['id']
        history = savedResult.objects.filter(user=request.user, id=id)
        if history.exists():
            history.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request, *args, **kwargs):
        id = self.kwargs['id']
        history = savedResult.objects.filter(user=request.user, id=id)
        if history.exists():
            serializer = MyHistorySerializer(
                history.first(), data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

