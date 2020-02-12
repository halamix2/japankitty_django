from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers

from .models import Course, Kanji, Vocabulary, Text, User
from .serializers import RegisterSerializer
#registration
from rest_framework.views import APIView
from rest_framework import status, permissions
from oauth2_provider.settings import oauth2_settings
from braces.views import CsrfExemptMixin
from oauth2_provider.views.mixins import OAuthLibMixin
from django.db import transaction
import json
from django.utils.translation import gettext_lazy as _

#stuff
from django.utils.decorators import method_decorator
#from django.http import HttpResponse
#from django.views.generic import View
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import AccessToken
import re

# Create your views here.

def courses(request):
    data = list(Course.objects.values())

    #allow returning non-dict data, an array in our case
    return JsonResponse(data, safe=False)

def kanji(request, id):
    data = list(Kanji.objects.filter(course=id).values())

    #allow returning non-dict data, an array in our case
    return JsonResponse(data, safe=False)
    
def vocabulary(request, id):
    data = list(Vocabulary.objects.filter(course=id).values())

    #allow returning non-dict data, an array in our case
    return JsonResponse(data, safe=False)

def texts(request):
    data = list(Text.objects.values())

    #allow returning non-dict data, an array in our case
    return JsonResponse(data, safe=False)

class UserRegister(CsrfExemptMixin, OAuthLibMixin, APIView):
    permission_classes = (permissions.AllowAny,)

    server_class = oauth2_settings.OAUTH2_SERVER_CLASS
    validator_class = oauth2_settings.OAUTH2_VALIDATOR_CLASS
    oauthlib_backend_class = oauth2_settings.OAUTH2_BACKEND_CLASS

    def post(self, request):
        if request.auth is None:
            data = request.data
            data = data.dict()
            serializer = RegisterSerializer(data=data)
            if serializer.is_valid():
                try:
                    with transaction.atomic():
                        user = serializer.save()

                        url, headers, body, token_status = self.create_token_response(request)

                        if token_status != 200:
                            raise Exception(json.loads(body).get("error_description", body))

                        return JsonResponse(json.loads(body), safe=False, status=token_status)
                except Exception as e:
                    return JsonResponse(data={"error": (str(e))}, safe=False, status=status.HTTP_400_BAD_REQUEST)
            return JsonResponse(data=serializer.errors, safe=False, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse([], safe=False, status=status.HTTP_403_FORBIDDEN)

def getUser(request):
    app_tk = request.META["HTTP_AUTHORIZATION"]
    m = re.search('(Bearer)(\s)(.*)', app_tk)
    app_tk = m.group(3)
    acc_tk = AccessToken.objects.get(token=app_tk)
    user = acc_tk.user

    return user

class Template(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = getUser(request)
        return JsonResponse(user.id, safe=False)

    def post(self, request):
        user = getUser(request)
        
        userLimited = dict()
        userLimited['id'] = user.id
        userLimited['name'] = user.username
        userLimited['email'] = user.email
        userLimited['sex'] = user.sex
        userLimited['surname'] = user.surname
        userLimited['surname'] = user.birthday
        userLimited['role'] = user.role
        userLimited['status'] = user.status

        odp = dict()
        odp['success'] = userLimited

        return JsonResponse(odp, safe=False)


class GetDetails(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = getUser(request)
        
        userLimited = dict()
        userLimited['id'] = user.id
        userLimited['name'] = user.username
        userLimited['email'] = user.email
        userLimited['sex'] = user.sex
        userLimited['surname'] = user.surname
        userLimited['surname'] = user.birthday
        userLimited['role'] = user.role
        userLimited['status'] = user.status

        odp = dict()
        odp['success'] = userLimited

        return JsonResponse(odp, safe=False)
    
    def post(self, request):
        user = getUser(request)
        
        userLimited = dict()
        userLimited['id'] = user.id
        userLimited['name'] = user.username
        userLimited['email'] = user.email
        userLimited['sex'] = user.sex
        userLimited['surname'] = user.surname
        userLimited['surname'] = user.birthday
        userLimited['role'] = user.role
        userLimited['status'] = user.status

        odp = dict()
        odp['success'] = userLimited

        return JsonResponse(odp, safe=False)


'''
        path('get-details', views.GetDetails.as_view()),
        path('edit-account', views.EditAccount.as_view()), #POST only
        path('progress', views.ProgressController.as_view()),
        path('users', views.ListAllUsers.as_view()), #GET only
        path('edit-text', views.EditText.as_view()), #POST only
'''