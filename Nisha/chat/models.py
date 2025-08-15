# Import necessary Django modules for database models
from django.db import models  # For creating database models and fields
from django.contrib.auth.models import User  # Built-in Django User model for authentication

class ChatRoom(models.Model):
    """
    Model representing a chat room where multiple users can exchange messages.
    Supports both individual and group conversations.
    
    This model stores chat room metadata and relationships between users.
    """
    
    # Basic room information
    name = models.CharField(max_length=100)  # Display name for the chat room (e.g., "Family Chat", "Work Team")
    description = models.TextField(blank=True)  # Optional description explaining room purpose
    
    # Room ownership and membership
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Delete room if creator is deleted
        related_name='created_rooms'  # Access creator's rooms via user.created_rooms.all()
    )
    
    members = models.ManyToManyField(
        User, 
        related_name='chat_rooms'  # Access user's rooms via user.chat_rooms.all()
    )
    
    # Room metadata
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set creation timestamp
    is_group = models.BooleanField(default=False)  # True for group chats, False for individual conversations

    def __str__(self):
        """
        String representation of the chat room for admin interface and debugging.
        
        Returns:
            The room name as the string representation
        """
        return self.name

    def get_last_message(self):
        """
        Helper method to get the most recent message in this chat room.
        Used for displaying preview text in chat lists.
        
        Returns:
            Message object: The most recent message, or None if no messages exist
        """
        return self.messages.order_by('-timestamp').first()
    """
    Model representing individual chat messages.
    Stores message content, sender information, and timestamps.
    
    Supports both legacy (non-room) messages and modern room-based messages.
    """
    
    # Sender information (supports both authenticated and anonymous users)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,  # Delete messages if user is deleted
        null=True, blank=True  # Allow null for anonymous users or legacy messages
    )
    
    username = models.CharField(max_length=100)  # Store username for display (backward compatibility)
    
    # Message content and metadata
    content = models.TextField()  # The actual message text content
    timestamp = models.DateTimeField(auto_now_add=True)  # Automatically set when message is created
    
    # Room association (optional for backward compatibility)
    chat_room = models.ForeignKey(
        ChatRoom, 
        on_delete=models.CASCADE,  # Delete messages if room is deleted
        related_name='messages',  # Access room messages via chat_room.messages.all()
        null=True, blank=True  # Allow null for legacy messages not associated with rooms
    )
    
    # Message status
    is_read = models.BooleanField(default=False)  # Track if message has been read (for future features)

    def __str__(self):
        """
        String representation of the message for admin interface and debugging.
        
        Returns:
            Formatted string showing sender and message preview
        """
        return f'{self.username}: {self.content[:20]}'  # Show first 20 characters of message

    class Meta:
        """
        Meta options for the Message model.
        Defines default ordering and other model-level options.
        """
        ordering = ['timestamp']  # Order messages chronologically (oldest first)

class UserProfile(models.Model):
    """
    Extended user profile model to store additional user information.
    Linked to Django's built-in User model via OneToOneField.
    
    Stores chat-specific user data like avatar, status, and online presence.
    """
    
    # Link to Django's User model (one profile per user)
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE  # Delete profile if user is deleted
    )
    
    # User display customization
    avatar = models.CharField(
        max_length=10, 
        default='👤'  # Default user emoji avatar (using emoji for simplicity)
    )
    
    status = models.CharField(
        max_length=100, 
        default='Available'  # User status message (e.g., "Busy", "Away", "Available")
    )
    
    # Online presence tracking
    is_online = models.BooleanField(default=False)  # Track if user is currently online
    last_seen = models.DateTimeField(auto_now=True)  # Automatically update when user is active
        """
        String representation of the user profile for admin interface.
        
        Returns:
            Formatted string showing username and "Profile"
        """
        return f'{self.user.username} Profile'