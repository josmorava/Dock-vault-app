from django.contrib import admin

from .models import Category, Document, Tag

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Document)
