from django.contrib import admin
from .models import State, Product, Equipment

admin.site.register([State, Product, Equipment])