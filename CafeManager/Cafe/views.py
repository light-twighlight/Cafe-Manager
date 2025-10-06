from django.shortcuts import render
from .models import State, Product, Equipment
from .serializers import StateSerializer, ProductSerializer, EquipmentSerializer, RegisterSerializer, UserSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login



class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # set owner and last_modified_by from the authenticated user if available
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            serializer.save(owner=user, last_modified_by=user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            serializer.save(last_modified_by=user)
        else:
            serializer.save()

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            serializer.save(owner=user, last_modified_by=user)
        else:
            serializer.save()

    def perform_update(self, serializer):
        user = getattr(self.request, 'user', None)
        if user and user.is_authenticated:
            serializer.save(last_modified_by=user)
        else:
            serializer.save()

def home(request):
    products = Product.objects.all()
    equipments = Equipment.objects.all()
    data = {
        'products': products,
        'equipments': equipments
    }
    return render(request, "home.html", data)

class RegisterView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})
        else:
            return Response({'error': 'Nieprawidłowe dane logowania'}, status=400)


