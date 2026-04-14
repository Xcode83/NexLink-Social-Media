# NexLink: Premium Social Networking Platform

NexLink is a high-performance, feature-rich social media platform designed for professional networking and community building. Built with a focus on modern UI/UX principles, such as **Glassmorphism** and **Dynamic Micro-animations**, NexLink provides a seamless experience for sharing insights, building followers, and secure professional messaging.

## 🚀 Key Features

### 🏢 Professional Relationship System
- **Asymmetrical Following**: A sophisticated Follow/Following system (similar to Twitter/Instagram).
- **Dynamic Action Buttons**: UI intelligently switches between **Follow**, **Following**, and **Follow Back** based on mutual relationships.
- **Network Stats**: Real-time tracking of Posts, Followers, and Following counts on user profiles.

### 💬 Secure Professional Messaging
- **Mutual Communication Restriction**: Messaging and Chat access is strictly enforced—users can only talk if they follow each other mutually (Follow Back status).
- **Real-time Chat UI**: A clean, focused interface for direct communication.

### 📝 Dynamic Content Feed
- **Rich Posts**: Support for text content and media uploads.
- **Engagement Loop**: In-built systems for **Liking** (with Instagram-style animations) and **Commenting** on posts.
- **Global Search**: Find and connect with professionals via a high-performance search engine.

### 👤 Premium Profile Management
- **Customizable Identity**: Update headlines, bios, locations, and avatars.
- **Advanced Identity Verification**: Dedicated "Profile Hero" section with premium glassmorphism effects and optimized avatar positioning.

---

## 🛠️ Technical Stack

- **Backend**: Python 3.x, Django 5.x/6.x framework.
- **Database**: SQLite (Development) / PostgreSQL (Production ready).
- **Frontend**: HTML5, Vanilla CSS3 (Custom Design System), FontAwesome 6.
- **UX/UI**: Glassmorphism, CSS Transitions, Staggered Animations, and Responsive Layouts.
- **Architecture**: Monolithic architecture with a clear separation of Models, Views, and Templates (MTV Pattern).

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Xcode83/NexLink-Social-Media.git
   cd NexLink
   ```

2. **Setup virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   *(Generate requirements.txt using `pip freeze > requirements.txt`)*
   ```bash
   pip install django pillow
   ```

4. **Run Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```
   Visit the app at `http://127.0.0.1:8000/`.

---

## 📊 System Architecture
NexLink follows the standard Django MTV (Model-Template-View) pattern:
- **Models**: Defines users, profiles, posts, messages, and social relationships using Django's ORM and specialized ManyToMany fields.
- **Views**: Process business logic, including the restricted messaging security layer and the toggle-follow logic.
- **Templates**: Rendered server-side with optimized CSS for a smooth, app-like frontend experience.

---

## 🎨 Design Philosophy
NexLink is built to be "alive." Every interaction involves subtle micro-animations (the **Heart Pop** for likes, **Staggered Fade-in** for content) paired with a high-contrast, premium aesthetic that ensures professionalism and high text readability.

---
Developed by **Xcode83**
