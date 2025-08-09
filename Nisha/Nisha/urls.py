# Main project URL configuration for Nisha chat application
# This is the root URL configuration that routes requests to appropriate apps
# It defines the main navigation structure of the entire website

from django.contrib import admin  # Django admin interface
from django.urls import path, include  # URL routing functions
from django.views.generic import RedirectView  # For redirecting requests
from django.contrib.auth import views as auth_views  # Built-in authentication views

# Main URL patterns for the entire Nisha project
# These patterns define the top-level navigation structure
urlpatterns = [
    # Django administration interface
    # Accessible at /admin/ - provides database management interface
    path('admin/', admin.site.urls),
    
    # Root URL redirect to home page
    # When users visit the homepage, show the home page with weather and info first
    # permanent=False means this is a temporary redirect (302 status code)
    path('', RedirectView.as_view(url='/home/', permanent=False)),
    
    # Chat application URLs
    # All URLs starting with /chat/ are handled by the chat app
    # This includes: /chat/, /chat/whatsapp/, /chat/send/, etc.
    path('chat/', include('chat.urls')),
    
    # User authentication URLs
    # Built-in Django authentication views for login/logout
    
    # Login page at /login/
    # redirect_authenticated_user=True redirects already logged-in users
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    
    # Logout functionality at /logout/
    # next_page='/login/' redirects to login page after logout
    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),
    
    # Home application URLs
    # All URLs starting with /home/ are handled by the home app
    # This includes the weather dashboard and landing page
    path('home/', include('home.urls')),
]

# URL Structure Overview:
# 
# / (root) → Redirects to /home/ (HOME PAGE FIRST)
# /admin/ → Django admin interface
# /chat/ → Chat application (includes multiple sub-URLs)
# /login/ → User login page
# /logout/ → User logout (redirects to login)
# /home/ → Home application with weather dashboard
#
# Navigation Flow:
# 1. User visits site → Redirected to HOME PAGE with weather info
# 2. From home page, user can navigate to chat via links
# 3. If accessing chat without auth → Redirected to login
# 4. After login → Can access both home and chat features
