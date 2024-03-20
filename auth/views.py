from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.contrib.auth.models import User
from django.contrib.auth import authenticate


# Foydalanuvchi yaratiladi, ro`yhatdan o`tadi va tokenni qaytaradi
@api_view(['POST'])
def sign_up(request):
    username = request.data.get('username')
    password = request.data.get('password')
    password_confirm = request.data.get('password_confirm')  
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    else: 
        if password == password_confirm:
            user = User.objects.create_user(username=username, password=password)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})


# Foydalanuvchi ma`lumotlarni tekshiradi va tokenni qaytaradi
@api_view(['POST'])
def sign_in(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
    

# Foydalanuvchi ma`lumotlari yangilanadi
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request):
    user = request.user
    new_username = request.data.get('new_username')
    new_password = request.data.get('new_password')
    
    if new_username and new_password:
        user.username = new_username
        user.save()
        user.set_password(new_password)        
        return Response({'message': 'Data user updated successfully.'})
    else:
        return Response({'error': 'New data user not provided.'}, status=status.HTTP_400_BAD_REQUEST) 


# Foydalanuvchini tokenini o`chirib yuboradi
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def sign_out(request):
    request.user.auth_token.delete()
    return Response({'message': 'Successfully signed out'})