from django.shortcuts import render
from .serializers import *
from .models import *
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login

#Rest Imports
from rest_framework import generics, permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from rest_framework.response import Response
# parsing data from the client
from rest_framework.parsers import JSONParser

from knox.views import LoginView as KnoxLoginView


# To bypass having a CSRF token
from django.views.decorators.csrf import csrf_exempt



# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })
    

#login
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


class UserDataList(generics.ListCreateAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer


class UserDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserData.objects.all()
    serializer_class = UserDataSerializer


@csrf_exempt
def user(request):
    if request.method == 'GET':
        emp = UserData.objects.all()
        emp_serializer = UserDataSerializer(emp, many=True)
        return JsonResponse(emp_serializer.data, safe=False)
  
    elif request.method == 'POST':
        emp_data = JSONParser().parse(request)
        emp_serializer = UserDataSerializer(data=emp_data)
          
        if emp_serializer.is_valid():
            emp_serializer.save()
            return JsonResponse(emp_serializer.data,  status=201)
        return JsonResponse(emp_serializer.errors, status=400)  



from knox.auth import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

class ExampleView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):
        content = {
            'foo': 'bar'
        }
        return Response(content)
    