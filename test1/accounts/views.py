from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
import jwt
import bcrypt
from django.conf import settings
from .models import CustomUser, Role, BusinessElement, AccessRule
from .authentication import JWTAuthentication
from .permissions import CustomPermission,IsAdminPermission
from .serializers import AccessRuleSerializer, RoleSerializer, BusinessElementSerializer
import uuid

class RegisterView(APIView):
    def post(self, request):
        data = request.data
        if data['password'] != data['password2']:
            return Response({'error': 'Пароли не совпадают'}, status=400)
        
        hashed = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()).decode()
        user = CustomUser.objects.create(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            password=hashed,
            role=Role.objects.get(name='user')
        )
        return Response({'message': 'Пользователь создан'}, status=201)

class LoginView(APIView):
    def post(self, request):
        try:
            user = CustomUser.objects.get(email=request.data['email'])
        except CustomUser.DoesNotExist:
            return Response({'error': 'Неверные данные'}, status=401)
        
        if user.check_password(request.data['password']):
            token = jwt.encode(
                {'user_id': str(user.id)},
                settings.SECRET_KEY,
                algorithm='HS256'
            )
            return Response({'token': token})
        return Response({'error': 'Неверные данные'}, status=401)
    
class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    business_element = 'users'

    def get(self, request):
        return Response([{"id": 1, "email": "user1@example.com"}, {"id": 2, "email": "user2@example.com"}])

class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    business_element = 'orders'

    def get(self, request):
        return Response([{"id": 1, "product": "Телевизор", "status": "доставка"}, {"id": 2, "product": "Смартфон", "status": "обработка"}])

    def post(self, request):
        return Response({"id": 3, "product": request.data.get("product"), "status": "создан"}, status=201)

class ProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [CustomPermission]
    business_element = 'products'

    def get(self, request):
        return Response([{"id": 1, "name": "Телевизор"}, {"id": 2, "name": "Смартфон"}])
    
class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

class BusinessElementListCreateView(generics.ListCreateAPIView):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

class BusinessElementDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BusinessElement.objects.all()
    serializer_class = BusinessElementSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

class AccessRuleListCreateView(generics.ListCreateAPIView):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]

class AccessRuleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AccessRule.objects.all()
    serializer_class = AccessRuleSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminPermission]