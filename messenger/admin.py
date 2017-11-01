from django.contrib import admin

from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.db.models import QuerySet

from .models import Message, Chat


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    pass


@admin.register(Chat)
class ChatAdmin(ModelAdmin):
    pass
