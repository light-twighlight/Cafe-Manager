from django.shortcuts import render
from .models import State, Product, Equipment
from .serializers import StateSerializer, ProductSerializer, EquipmentSerializer, RegisterSerializer
from django.contrib.auth import get_user_model
from rest_framework import viewsets, generics, permissions
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django import forms
# models already imported above



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


def login_page(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            error = 'Invalid credentials'
    return render(request, 'login.html', {'error': error})


def register_page(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        User = get_user_model()
        if User.objects.filter(username=username).exists():
            error = 'Username already exists'
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('home')
    return render(request, 'register.html', {'error': error})


def logout_view(request):
    logout(request)
    return redirect('home')


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'quantity', 'expiration_date']
        widgets = {
            'expiration_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description', 'state', 'date']
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.owner = request.user
            prod.last_modified_by = request.user
            prod.save()
            return redirect('home')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form, 'action': 'Create Product'})


@login_required
def product_edit(request, pk):
    prod = Product.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=prod)
        if form.is_valid():
            p = form.save(commit=False)
            p.last_modified_by = request.user
            p.save()
            return redirect('home')
    else:
        # Format the existing expiration_date to match datetime-local input
        if prod.expiration_date:
            try:
                initial = {'expiration_date': prod.expiration_date.strftime('%Y-%m-%dT%H:%M')}
            except Exception:
                initial = {}
            form = ProductForm(instance=prod, initial=initial)
        else:
            form = ProductForm(instance=prod)
    return render(request, 'product_form.html', {'form': form, 'action': 'Edit Product'})


@login_required
def product_delete(request, pk):
    prod = Product.objects.get(pk=pk)
    if request.method == 'POST':
        prod.delete()
        return redirect('home')
    return render(request, 'confirm_delete.html', {'obj': prod, 'type': 'Product'})


@login_required
def equipment_create(request):
    if request.method == 'POST':
        form = EquipmentForm(request.POST)
        if form.is_valid():
            eq = form.save(commit=False)
            eq.owner = request.user
            eq.last_modified_by = request.user
            eq.save()
            return redirect('home')
    else:
        form = EquipmentForm()
    return render(request, 'equipment_form.html', {'form': form, 'action': 'Create Equipment'})


@login_required
def equipment_edit(request, pk):
    eq = Equipment.objects.get(pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=eq)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_modified_by = request.user
            e.save()
            return redirect('home')
    else:
        form = EquipmentForm(instance=eq)
    return render(request, 'equipment_form.html', {'form': form, 'action': 'Edit Equipment'})


@login_required
def equipment_delete(request, pk):
    eq = Equipment.objects.get(pk=pk)
    if request.method == 'POST':
        form = EquipmentForm(request.POST, instance=eq)
        if form.is_valid():
            e = form.save(commit=False)
            e.last_modified_by = request.user
            e.save()
            return redirect('home')
    else:
        # Format existing date to match datetime-local input
        if eq.date:
            try:
                initial = {'date': eq.date.strftime('%Y-%m-%dT%H:%M')}
            except Exception:
                initial = {}
            form = EquipmentForm(instance=eq, initial=initial)
        else:
            form = EquipmentForm(instance=eq)
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


class RegisterView(generics.CreateAPIView):
    User = get_user_model()
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


