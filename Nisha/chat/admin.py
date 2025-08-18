from django.contrib import admin
from .models import Message, ChatRoom, UserProfile

# Register your models here.
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('username', 'content', 'timestamp', 'chat_room', 'is_read')
    list_filter = ('timestamp', 'is_read', 'chat_room')
    search_fields = ('username', 'content')
    readonly_fields = ('timestamp',)

@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_by', 'created_at', 'is_group')
    list_filter = ('created_at', 'is_group')
    search_fields = ('name', 'description')
    readonly_fields = ('created_at',)
    filter_horizontal = ('members',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar', 'status', 'is_online', 'last_seen')
    list_filter = ('is_online', 'last_seen')
    search_fields = ('user__username', 'status')
    readonly_fields = ('last_seen',)
