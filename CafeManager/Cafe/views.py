from django.shortcuts import render
from rest_framework import viewsets, permissions
from .models import State, Product, Equipment
from .serializers import StateSerializer, ProductSerializer, EquipmentSerializer

class StateViewSet(viewsets.ModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    permission_classes = [permissions.AllowAny]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

class EquipmentViewSet(viewsets.ModelViewSet):
    queryset = Equipment.objects.all()
    serializer_class = EquipmentSerializer
    permission_classes = [permissions.AllowAny]

def home(request):
    products = Product.objects.all()
    equipments = Equipment.objects.all()
    data = {
        'products': products,
        'equipments': equipments
    }
    return render(request, "home.html", data)


