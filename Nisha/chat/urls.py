# Chat app URL configuration
# This file defines all URL patterns for the chat application
# Each pattern maps a URL to a specific view function

from django.urls import path  # For defining URL patterns
from .views import (  # Import all view functions from the current app
    chat_view, send_message, get_messages, whatsapp_view,
    get_room_messages, create_chat_room, join_chat_room,
    register_view, get_users
)

# URL patterns for the chat application
# Each path() defines a route: path(route, view_function, name)
    # Legacy chat interface (original simple chat)
    path('', chat_view, name='chat'),  # Root chat URL - displays basic chat interface
    
    # Modern WhatsApp-style interface
    path('whatsapp/', whatsapp_view, name='whatsapp'),  # Main modern chat interface with sidebar
    
    # AJAX endpoints for message handling
    path('send/', send_message, name='send_message'),  # POST endpoint to send new messages
    path('messages/', get_messages, name='get_messages'),  # GET endpoint to retrieve legacy messages
    
    # Room-specific message endpoints
    path('room/<int:room_id>/messages/', get_room_messages, name='get_room_messages'),  # GET messages for specific room
    
    # Chat room management endpoints
    path('create-room/', create_chat_room, name='create_chat_room'),  # POST endpoint to create new chat rooms
    path('join-room/<int:room_id>/', join_chat_room, name='join_chat_room'),  # POST endpoint to join existing rooms
    
    # User management endpoints
    path('register/', register_view, name='register'),  # User registration page and handler
    path('users/', get_users, name='get_users'),  # GET endpoint to retrieve user list for room invitations
    
    # Dynamic room access (legacy support)
    path('<str:room_name>/', chat_view, name='room'),  # Access specific room by name (e.g., /chat/general/)

# URL Pattern Explanations:
# 
# 1. '' (empty string) - Maps to chat_view for basic chat interface
# 2. 'whatsapp/' - Maps to whatsapp_view for modern interface
# 3. 'send/' - AJAX endpoint for sending messages
# 4. 'messages/' - AJAX endpoint for getting messages (polling)
# 5. 'room/<int:room_id>/messages/' - Get messages for specific room by ID
# 6. 'create-room/' - Create new chat rooms
# 7. 'join-room/<int:room_id>/' - Join existing room by ID
# 8. 'register/' - User registration functionality
# 9. 'users/' - Get list of users for room management
# 10. '<str:room_name>/' - Access rooms by name (catch-all pattern)