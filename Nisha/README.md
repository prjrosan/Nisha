# 🚀 Nisha Chat App

A modern, responsive chat application built with Django featuring real-time messaging, user authentication, and a beautiful homepage.

## ✨ Features

- **💬 Real-time Chat**: Interactive chat interface with message history
- **🔐 User Authentication**: Complete signup, login, and logout system
- **📱 Mobile Responsive**: Beautiful design that works on all devices
- **🗺️ Osaka Map Integration**: Interactive map panel on homepage
- **🌤️ Weather API**: Real-time weather information
- **🎨 Modern UI**: Clean, gradient-based design with smooth animations

## 🛠️ Tech Stack

- **Backend**: Django 5.1.5
- **Database**: SQLite (easily configurable for production)
- **Frontend**: HTML5, CSS3, JavaScript
- **Static Files**: WhiteNoise for production serving
- **Authentication**: Django built-in user system

## 🚀 Quick Start

### Prerequisites
- Python 3.12+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/prjrosan/Nisha.git
   cd Nisha
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the server**
   ```bash
   python manage.py runserver
   ```

6. **Open your browser**
   Navigate to `http://127.0.0.1:8000/home/`

## 📁 Project Structure

```
Nisha/
├── chat/                 # Chat app with messaging functionality
├── home/                 # Homepage app with weather and map
├── Nisha/               # Main project settings
├── templates/           # Global templates
├── static/              # Static files (CSS, JS, images)
├── manage.py            # Django management script
└── requirements.txt     # Python dependencies
```

## 🌟 Key Features Explained

### Chat System
- **Anonymous Access**: View chat without logging in
- **User Registration**: Create account to send messages
- **Message History**: Persistent chat conversations
- **Real-time Updates**: Instant message delivery

### Homepage
- **Dynamic Content**: Different views for logged-in vs anonymous users
- **Osaka Map**: Interactive Google Maps integration
- **Weather Widget**: Real-time weather data
- **Responsive Design**: Optimized for all screen sizes

### Authentication
- **Secure Login**: CSRF-protected forms
- **User Registration**: Easy account creation
- **Session Management**: Persistent login state
- **Logout Confirmation**: User-friendly logout process

## 🎨 Customization

### Changing the Profile Photo
Replace `home/static/home/mygf.jpg` with your own image

### Modifying the Map
Update the Google Maps iframe in `home/templates/home/home.html`

### Styling
Customize colors and themes in the CSS files

## 🚀 Deployment

This project is designed to be easily deployable on any platform:

- **Railway**: Add `Procfile` and `runtime.txt`
- **Render**: Use `gunicorn` with proper port binding
- **Heroku**: Add `Procfile` and configure buildpacks
- **Vercel**: Use `vercel.json` configuration
- **PythonAnywhere**: Direct Django deployment

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 👨‍💻 Creator

**PRAJA ROSAN** - Built with ❤️ for the Nisha community

---

⭐ **Star this repository if you found it helpful!**
