import sys
import urllib, json

from django.core.exceptions import PermissionDenied
from django.http import (HttpResponse, HttpResponseNotFound,
    HttpResponseBadRequest, HttpResponseServerError)
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.models import User
from backend.models import *

def login_user(request):
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return HttpResponseRedirect("/login")

class UserView(APIView):
    def post(self, request):
        print "got into user view post request"
        data = dict(request.POST)
        print data
        # create user object
        user = User.objects.create_user(data['first_name'][0], data['email'][0], data['password'][0])
        user.last_name = data['last_name'][0]
        user.save()
        # create userdata and link to user
        user_data = UserData(user=user, google_key=data['g_key'][0], up_key=data['u_key'][0])
        user_data.save()
        # login and redirect to homepage
        user_login = authenticate(username=data['first_name'][0], password=data['password'][0])
        login(request, user_login)
        return HttpResponseRedirect("/")

class ErrorView(View):
    """ HTTP 500: Internal Server Error """
    template_name = '500.html'
    status = 500
    
    def get(self, request):
        return render(request, self.template_name, status=self.status)
    
class PermissionDeniedView(ErrorView):
    """ HTTP 403: Forbidden """
    template_name = '403.html'
    status = 403
    
    
class NotFoundView(ErrorView):
    """ HTTP 404: Not Found """
    template_name = '404.html'
    status = 404

class LoginPage(TemplateView):
    """ The Login Page. """
    template_name = 'login.html'
    
class IndexPage(TemplateView):
    """ The Index Page. """
    template_name = 'index.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(IndexPage, self).dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)

class Register(TemplateView):
    """ The Index Page. """
    template_name = 'register.html'

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(IndexPage, self).dispatch(*args, **kwargs)

    def get(self, request):
        up_code = request.GET.__getitem__('up_code')
        return render(request, self.template_name, {'upcode': up_code})

class JawboneLogin(TemplateView):
    """ The Jawbone Login Page. """
    template_name = 'jawboneLogin.html'

def jawbone1(request):
    code = request.GET.__getitem__('code')
    request = 'https://jawbone.com/auth/oauth2/token?grant_type=authorization_code&client_id=mAl_RHjkugQ&client_secret=a026698826232e451bb06f270023bdd2167a1ed8&code='
    request += code
    f = urllib.urlopen(request,{})
    data = json.loads(f.read())
    token = data["access_token"]
    return HttpResponseRedirect("/register?up_code=%s" % token)
    
    