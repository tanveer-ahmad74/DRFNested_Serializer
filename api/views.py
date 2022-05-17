from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import Profile, Hobby, Job
from rest_framework import viewsets
from .serializers import ProfileSerializer, HobbySerializer, JobSerializer
from rest_framework.permissions import AllowAny
from rest_framework.parsers import JSONParser
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
from api.recaptcha import FormWithCaptcha


def home(request):
    context = {
    'Captcha': FormWithCaptcha
    }
    return render(request, 'admin/home.html', context)

class ProfileViewSet(viewsets.ModelViewSet):
    authentication_classes = [BasicAuthentication, SessionAuthentication]
    parser_classes = [JSONParser]
    permission_classes = [AllowAny]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'post', 'retrieve', 'put', 'patch']
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = ['name', 'email', 'status']
    search_fields = ['name', 'email', 'status']
    filterset_fields = ['name']
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get(self, request):
        content = {
            'user': str(request.user),  # `django.contrib.auth.User` instance.
            'auth': str(request.auth),  # None
        }
        print(Response)
        return Response(content)


class HobbyViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Hobby.objects.all()
    serializer_class = HobbySerializer
    http_method_names = ['get']


class JobViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class SpecificJobViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSerializer
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_queryset(self):
        return Job.objects.all().filter(name__startswith='Teacher')


