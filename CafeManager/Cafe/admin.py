from django.contrib import admin
from .models import State, Product, Equipment


class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'quantity', 'expiration_date', 'owner', 'last_modified_by', 'last_modified_date')
	list_filter = ('expiration_date', 'last_modified_date')
	search_fields = ('name', 'description')

	def save_model(self, request, obj, form, change):
		# Set owner on create
		if not change and not obj.owner:
			obj.owner = request.user
		# Always update last_modified_by
		obj.last_modified_by = request.user
		super().save_model(request, obj, form, change)


class EquipmentAdmin(admin.ModelAdmin):
	list_display = ('name', 'state', 'owner', 'responsible_user', 'last_modified_by', 'last_modified_date')
	list_filter = ('state', 'responsible_user')
	search_fields = ('name', 'description')

	def save_model(self, request, obj, form, change):
		if not change and not obj.owner:
			obj.owner = request.user
		obj.last_modified_by = request.user
		super().save_model(request, obj, form, change)


admin.site.register(State)
admin.site.register(Product, ProductAdmin)
admin.site.register(Equipment, EquipmentAdmin)