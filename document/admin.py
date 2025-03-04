from django.contrib import admin
from .models import Document, Category
from django.contrib.admin import StackedInline

class CategoryInline(admin.StackedInline):
    model = Document.categories.through

class DocumentAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
    
admin.site.register(Document, DocumentAdmin)
admin.site.register(Category)
