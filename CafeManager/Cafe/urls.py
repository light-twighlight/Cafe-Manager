from django.urls import path, include
from . import views
# from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'states', views.StateViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'equipment', views.EquipmentViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('api/', include((router.urls, 'api'))),
    path('api/auth/register/', views.RegisterView.as_view(), name='api-register'),
    path('api/auth/login/', views.LoginView.as_view(), name='api-login'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('logout/', views.logout_view, name='logout'),
]