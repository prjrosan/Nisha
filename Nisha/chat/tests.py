from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Message, ChatRoom, UserProfile
import json

# Create your tests here.

class ChatModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.profile = UserProfile.objects.create(user=self.user)
        self.room = ChatRoom.objects.create(
            name='Test Room',
            created_by=self.user,
            is_group=True
        )
        self.room.members.add(self.user)

    def test_chat_room_creation(self):
        self.assertEqual(self.room.name, 'Test Room')
        self.assertEqual(self.room.created_by, self.user)
        self.assertTrue(self.room.is_group)
        self.assertIn(self.user, self.room.members.all())

    def test_message_creation(self):
        message = Message.objects.create(
            user=self.user,
            username=self.user.username,
            content='Test message',
            chat_room=self.room
        )
        self.assertEqual(message.content, 'Test message')
        self.assertEqual(message.user, self.user)
        self.assertEqual(message.chat_room, self.room)

    def test_user_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
        self.assertEqual(self.profile.avatar, '👤')
        self.assertEqual(self.profile.status, 'Available')

class ChatViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_chat_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('chat:chat'))
        self.assertEqual(response.status_code, 200)

    def test_whatsapp_view_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('chat:whatsapp'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post(self):
        data = {
            'username': 'newuser',
            'password1': 'newpass123',
            'password2': 'newpass123'
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 200)
        # Check if user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
