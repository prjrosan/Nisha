# Import necessary Django modules and Python libraries
from django.shortcuts import render, get_object_or_404  # For rendering templates and safe object retrieval
from django.http import JsonResponse  # For sending JSON responses to AJAX requests
from django.views.decorators.csrf import csrf_exempt  # To exempt views from CSRF protection (not used)
from django.views.decorators.http import require_POST  # To ensure view only accepts POST requests
from django.contrib.auth.decorators import login_required  # To require user authentication
from django.contrib.auth.models import User  # Built-in Django User model
from django.contrib.auth import login, authenticate  # For user authentication functions
from django.contrib.auth.forms import UserCreationForm  # Built-in user registration form
import json  # For handling JSON data
from .models import Message, ChatRoom, UserProfile  # Import our custom models
    """
    Legacy chat view for the original simple chat interface.
    Displays messages in a basic chat room format.
    
    Args:
        request: HTTP request object
        room_name: Name of the chat room (defaults to 'global')
        
    Returns:
        Rendered chat template with messages and user context
    """
    # Get all messages ordered by timestamp (oldest first)
    # This creates a chronological conversation flow
    messages = Message.objects.order_by('timestamp')
    
    # Render the original chat template with context data
        'messages': messages,    # All chat messages for display
        'room_name': room_name,  # Current room name
        'user': request.user,    # Current user information
    })

def whatsapp_view(request):
    """
    Main WhatsApp-like interface view.
    Displays the modern chat interface with sidebar and chat rooms.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered WhatsApp-style template with user's chat rooms
    """
    # Check if user is authenticated to show personalized content
    if request.user.is_authenticated:
        # Get or create user profile for additional user data
        # This ensures every authenticated user has a profile
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Get all chat rooms where the user is a member
        # Ordered by creation date (newest first) for better UX
        chat_rooms = request.user.chat_rooms.all().order_by('-created_at')
    else:
        # For anonymous users, show empty chat room list
        chat_rooms = ChatRoom.objects.none()

    # Render the WhatsApp-style interface
    return render(request, 'chat/whatsapp.html', {
        'chat_rooms': chat_rooms,  # User's chat rooms for sidebar
        'user': request.user,      # Current user info
    })

@login_required  # Require authentication to send messages
@require_POST  # Decorator ensures this view only accepts POST requests
def send_message(request):
    """
    AJAX endpoint for sending chat messages.
    Handles message creation and storage in database.
    
    Args:
        request: HTTP POST request with message data
        
    Returns:
        JSON response indicating success/failure
    """
    try:
        # Extract message content from POST data and remove whitespace
        message_content = request.POST.get('message', '').strip()
        
        # Extract chat room ID if message is for specific room
        chat_room_id = request.POST.get('chat_room_id')

        # Only process non-empty messages
        if message_content:
            # Determine username: authenticated user's name or 'Anonymous'
            username = request.user.username if request.user.is_authenticated else 'Anonymous'

            # Get chat room object if room ID provided
            chat_room = None
            if chat_room_id:
                try:
                    chat_room = ChatRoom.objects.get(id=chat_room_id)
                except ChatRoom.DoesNotExist:
                    # If room doesn't exist, continue without room (legacy support)
                    pass

            # Create and save new message to database
            Message.objects.create(
                user=request.user if request.user.is_authenticated else None,  # Link to user if authenticated
                username=username,        # Store username for display
                content=message_content,  # Message text
                chat_room=chat_room      # Link to specific chat room if applicable
            )

            # Return success response for AJAX handler
            return JsonResponse({'success': True, 'message': 'Message sent'})
        else:
            # Return error if message is empty
            return JsonResponse({'success': False, 'error': 'Empty message'})
            
    except Exception as e:
        # Handle any unexpected errors gracefully
        return JsonResponse({'success': False, 'error': str(e)})

def get_messages(request):
    """
    AJAX endpoint for retrieving messages from the legacy chat system.
    Returns messages not associated with specific chat rooms.
    
    Args:
        request: HTTP request object
        
    Returns:
        JSON response with message data
    """
    try:
        # Get messages not linked to specific chat rooms (legacy system)
        # Ordered by timestamp for chronological display
        messages = Message.objects.filter(chat_room__isnull=True).order_by('timestamp')
        
        # Convert message objects to JSON-serializable format
        messages_data = []
        for msg in messages:
            messages_data.append({
                'username': msg.username,                    # Sender's username
                'content': msg.content,                      # Message text
                'timestamp': msg.timestamp.isoformat()       # ISO format timestamp for JavaScript
            })

        # Return messages as JSON for AJAX polling
        return JsonResponse({'messages': messages_data})
        
    except Exception as e:
        # Handle errors gracefully
        return JsonResponse({'error': str(e)})

def get_room_messages(request, room_id):
    """
    AJAX endpoint for retrieving messages from a specific chat room.
    Used by the WhatsApp-style interface for real-time message loading.
    
    Args:
        request: HTTP request object
        room_id: ID of the chat room to get messages from
        
    Returns:
        JSON response with room-specific message data
    """
    try:
        # Get chat room object or return 404 if not found
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        
        # Get all messages for this specific room, ordered by time
        messages = chat_room.messages.order_by('timestamp')
        
        # Convert messages to JSON format
        messages_data = []
        for msg in messages:
            messages_data.append({
                'username': msg.username,                    # Sender's display name
                'content': msg.content,                      # Message content
                'timestamp': msg.timestamp.isoformat(),      # ISO timestamp
                'user_id': msg.user.id if msg.user else None  # User ID for styling own messages
            })

        # Return room messages as JSON
        return JsonResponse({'messages': messages_data})
        
    except Exception as e:
        # Handle errors gracefully
        return JsonResponse({'error': str(e)})

@require_POST  # Only accept POST requests for security
def create_chat_room(request):
    """
    AJAX endpoint for creating new chat rooms.
    Allows users to create both individual and group chats.
    
    Args:
        request: HTTP POST request with room creation data
        
    Returns:
        JSON response with creation status and room ID
    """
    try:
        # Ensure user is authenticated to create rooms
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'})

        # Extract room details from POST data
        name = request.POST.get('name', '').strip()           # Room name
        description = request.POST.get('description', '').strip()  # Optional description
        is_group = request.POST.get('is_group') == 'true'     # Group vs individual chat

        # Validate required fields
        if not name:
            return JsonResponse({'success': False, 'error': 'Chat name is required'})

        # Create new chat room with provided details
        chat_room = ChatRoom.objects.create(
            name=name,                    # Room display name
            description=description,      # Optional room description
            created_by=request.user,     # User who created the room
            is_group=is_group           # Whether it's a group chat
        )

        # Add the creator as the first member of the room
        chat_room.members.add(request.user)

        # Return success response with room details
        return JsonResponse({
            'success': True,
            'room_id': chat_room.id,                         # New room ID for frontend
            'message': 'Chat room created successfully'
        })

    except Exception as e:
        # Handle any creation errors
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST  # Only accept POST requests
def join_chat_room(request, room_id):
    """
    AJAX endpoint for joining existing chat rooms.
    Adds the current user to a chat room's member list.
    
    Args:
        request: HTTP POST request
        room_id: ID of the room to join
        
    Returns:
        JSON response indicating join status
    """
    try:
        # Ensure user is authenticated to join rooms
        if not request.user.is_authenticated:
            return JsonResponse({'success': False, 'error': 'Authentication required'})

        # Get the chat room or return 404 if not found
        chat_room = get_object_or_404(ChatRoom, id=room_id)
        
        # Add current user to room's member list
        # Django's ManyToManyField automatically handles duplicates
        chat_room.members.add(request.user)

        # Return success confirmation
        return JsonResponse({'success': True, 'message': 'Joined chat room successfully'})

    except Exception as e:
        # Handle join errors
        return JsonResponse({'success': False, 'error': str(e)})

def register_view(request):
    """
    User registration view supporting both regular form submission and AJAX.
    Creates new user accounts and automatically logs them in.
    
    Args:
        request: HTTP request (GET for form display, POST for registration)
        
    Returns:
        For GET: Rendered registration template
        For POST: JSON response (AJAX) or redirect (regular form)
    """
    if request.method == 'POST':
        # Handle registration form submission
        form = UserCreationForm(request.POST)
        
        # Validate form data
        if form.is_valid():
            # Save new user to database
            user = form.save()
            
            # Create associated user profile for additional data
            UserProfile.objects.create(user=user)
            
            # Extract credentials for automatic login
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            
            # Authenticate and log in the new user
            user = authenticate(username=username, password=password)
            login(request, user)
            
            # Return JSON response for AJAX requests
            return JsonResponse({'success': True, 'redirect': '/chat/whatsapp/'})
        else:
            # Return form errors for AJAX handling
            return JsonResponse({'success': False, 'errors': form.errors})

    # For GET requests, display the registration form
    return render(request, 'registration/register.html', {'form': UserCreationForm()})

def get_users(request):
    """
    AJAX endpoint for retrieving list of users.
    Used for adding users to chat rooms or displaying user lists.
    
    Args:
        request: HTTP request object
        
    Returns:
        JSON response with user data
    """
    try:
        # Get all users except the current user (if authenticated)
        # This prevents users from seeing themselves in selection lists
        users = User.objects.exclude(id=request.user.id if request.user.is_authenticated else None)
        
        # Convert user objects to JSON format
        users_data = []
        for user in users:
            # Get user profile if it exists
            profile = getattr(user, 'userprofile', None)
            
            users_data.append({
                'id': user.id,                                           # User ID
                'username': user.username,                               # Username
                'full_name': user.get_full_name() or user.username,     # Full name or username fallback
                'avatar': profile.avatar if profile else '👤',          # User avatar or default emoji
                'is_online': profile.is_online if profile else False    # Online status
            })

        # Return user list as JSON
        return JsonResponse({'users': users_data})

    except Exception as e:
        # Handle any errors
        return JsonResponse({'error': str(e)})
