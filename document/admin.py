from django.contrib import admin
from .models import Document, Category, ServiceConfig
from django.contrib.admin import StackedInline
from django.core.exceptions import ValidationError
import importlib


class CategoryInline(admin.StackedInline):
    model = Document.categories.through


class DocumentAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]


class ServiceConfigAdmin(admin.ModelAdmin):
    list_display = ("service_type", "implementation")


admin.site.register(Document, DocumentAdmin)
admin.site.register(ServiceConfig, ServiceConfigAdmin)
admin.site.register(Category)
