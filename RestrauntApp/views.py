from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from RestrauntApp.models import Restraunt,RestrauntBranch, RestrauntMenuHead
from RestrauntApp.serializers import RestrauntSerializer,RestrauntMenuHeadSerializer
# Create your views here.

class RestrauntsListAPI(ListAPIView):
    queryset = Restraunt.objects.all()
    serializer_class = RestrauntSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = {
        'rating': ['gte', 'lte']
    }

class RestrauntsDetailAPI(RetrieveAPIView):
    queryset = Restraunt.objects.all()
    serializer_class = RestrauntSerializer
    permission_classes = [permissions.AllowAny]
    



class RestrauntMenuHeadListAPI(ListAPIView):
    queryset = RestrauntMenuHead.objects.all()
    serializer_class = RestrauntMenuHeadSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['restraunt']
  