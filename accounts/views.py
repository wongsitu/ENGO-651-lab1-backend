from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework import permissions
from django.contrib import auth
from rest_framework.response import Response
from .forms import UserForm
from .serializers import UserSerializer
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.utils.decorators import method_decorator

@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return Response({ 'success': True, 'data': 'CSRF cookie set' })

class CheckAuthenticatedView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'success': isAuthenticated, 'data': 'success' })
            else:
                return Response({ 'success': isAuthenticated })
        except:
            return Response({ 'success': isAuthenticated, 'errors': ['Something went wrong when checking authentication status'] })

@method_decorator(csrf_protect, name='dispatch')
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        registered = False
        user_form = UserForm(data=request.POST)
        serializer = UserSerializer(data=request.data)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            return Response({ 'success': registered, 'data': serializer.initial_data })
        else:
            return Response({ 'success': False, 'errors': user_form.errors })

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = self.request.data
        username = data['username']
        password = data['password']

        try:
            user = auth.authenticate(username=username, password=password)

            if user:
                if user.is_active:
                    auth.login(request, user)
                    return Response({ 'success': True })
                else:
                    return Response({ 'success': False, 'errors': ["Your account was inactive."] })
            else:
                return Response({ 'success': False, 'errors': ["Invalid login details given"] })
        except:
            return Response({ 'success': False, 'errors': ['Something went wrong when logging in'] })

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': True })
        except:
            return Response({ 'success': True, 'errors': ['Something went wrong when logging out'] })