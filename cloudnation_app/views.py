from django.http import JsonResponse
from .serializers import *
from .models import *
from rest_framework import generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.middleware import csrf
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated


class RegistrationView(generics.GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = serializer.data
            
            user_data['tokens'].pop('refresh')
            response = Response({'success':True,"data":user_data}, status=status.HTTP_201_CREATED)
            # Set the JWT token in the cookie
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], 
                value=user.tokens["refresh"],
                max_age=2592000,
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'], 
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'], 
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'], 
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                domain="127.0.0.1"
            )
            # Get CSRF token
            csrf.get_token(request)
            return response
        return Response({'success':False,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # return Response(serializer.data,status=status.HTTP_200_OK)
            data = serializer.data.copy()  # Create a copy to avoid modifying the original serializer.data
            tokens = data.get("tokens", {})
            refresh_token = tokens.pop("refresh", None)
            response = Response(data, status=status.HTTP_200_OK)
            
            # Set the JWT token in the cookie
            response.set_cookie(
                key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'], 
                value=refresh_token,
                max_age=2592000,
                expires=settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'], 
                secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'], 
                httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'], 
                samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE'],
                domain="127.0.0.1"
            )

            # Get CSRF token
            csrf.get_token(request)
            
            return response
        return Response({'sucess':False,"data":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

ERROR_TYPE = {
    'INVALID_CREDENTIALS':{'message':'email or password does mot match'},
    'INVALID_REFRESH':{'message':'invalid refresh Token, Login in Again'}
}

class CustomTokenRefreshView(APIView):
    '''
    Gets COOKIE data from request generate new token
    from the refresh token and returns an access token
    '''
    def get(self,request):
        try:
            token = request.COOKIES['refresh_token']
            token = RefreshToken(token)
            return JsonResponse({"sucess":True,"data":{"access": str(token.access_token)}}, status=status.HTTP_201_CREATED)
        except Exception:
            return JsonResponse({'success':False,'data': ERROR_TYPE['INVALID_REFRESH']}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    '''
    Logout API blacklists the refresh tooken and deletes the cookies
    make sure to send cookies in request from frontend
    '''
    def post(self,request):
        try:
            token = RefreshToken(request.COOKIES['refresh_token'])
            token.blacklist()
            res=JsonResponse({"data": {'message': 'Logged-Out Sucessfully'}}, status=status.HTTP_200_OK)
            res.delete_cookie(key='refresh_token')
            return res
        except Exception:
            return JsonResponse({'data': ERROR_TYPE['INVALID_REFRESH']}, status=status.HTTP_401_UNAUTHORIZED)
        

class GithubDetailsViewSet(viewsets.ModelViewSet):
    queryset = githubdetails.objects.all()
    serializer_class = githubdetailsSerializer
    permission_classes = [IsAuthenticated]

class AppDetailsViewSet(viewsets.ModelViewSet):
    queryset = appdetails.objects.all()
    serializer_class = appdetailsSerializer
    permission_classes = [IsAuthenticated]

class AppPlansViewSet(viewsets.ModelViewSet):
    queryset = appplans.objects.all()
    serializer_class = appdetailsSerializer
    permission_classes = [IsAuthenticated]

class DatabaseDetailsViewSet(viewsets.ModelViewSet):
    queryset = databasedetails.objects.all()
    serializer_class = databasedetailsSerializer
    permission_classes = [IsAuthenticated]

class DbPlansViewSet(viewsets.ModelViewSet):
    queryset = dbplans.objects.all()
    serializer_class = dbplansSerializer
    permission_classes = [IsAuthenticated]

class EnvVariablesViewSet(viewsets.ModelViewSet):
    queryset = envvariables.objects.all()
    serializer_class = envvariablesSerializer
    permission_classes = [IsAuthenticated]

