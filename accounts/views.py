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

@method_decorator(csrf_protect, name='dispatch')
class RegisterView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        registered = False
        user_form = UserForm(data=request.data)

        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            registered = True
            auth.login(request, user)
            return Response({ 'success': registered, 'data': model_to_dict(user) })
        else:
            return Response({ 'success': False, 'errors': user_form.errors })

@method_decorator(csrf_protect, name='dispatch')
class LoginView(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        auth_form = AuthenticationForm(request, data=request.data)

        if auth_form.is_valid():
            user = auth_form.get_user()
            auth.login(request, user)
            return Response({ 'success': True, 'data': model_to_dict(user) })
        else:
            return Response({ 'success': False, 'errors': auth_form.errors })

class LogoutView(APIView):
    def delete(self, request, format=None):
        try:
            auth.logout(request)
            return Response({ 'success': True })
        except:
            return Response({ 'success': True, 'errors': ['Something went wrong when logging out'] })

class CurrentUserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, format=None):
        user = self.request.user

        try:
            isAuthenticated = user.is_authenticated

            if isAuthenticated:
                return Response({ 'success': True, 'data': model_to_dict(user) })
            else:
                return Response({ 'success': True, 'data': None })
        except:
            return Response({ 'success': False, 'errors': ['Something went wrong when checking authentication status'] })