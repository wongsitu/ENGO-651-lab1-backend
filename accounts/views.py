from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from django.contrib.auth.forms import AuthenticationForm
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

class CurrentUserView(APIView):
    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'success': isAuthenticated, 'data': model_to_dict(user) })
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
        auth_form = AuthenticationForm(request, data=request.POST)

        if auth_form.is_valid():
            user = auth_form.get_user()
            auth.login(request, user)
            return Response({ 'success': True, 'data': model_to_dict(user) })
        else:
            return Response({ 'success': False, 'errors': auth_form.errors })

class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': True })
        except:
            return Response({ 'success': True, 'errors': ['Something went wrong when logging out'] })