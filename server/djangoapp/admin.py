from django.contrib import admin
from .models import CarMake, CarModel


# Register your models here.
class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    list_filter = ('name',)
    search_fields = ('name', 'description')


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'year')
    list_filter = ('name', 'type', 'year')
    search_fields = ('name', 'type', 'year')


# Register the models with the admin site
admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here
