<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:2E3192,100:1BFFFF&height=180&section=header&text=RealTime-Collab-Django&fontSize=38&fontColor=ffffff&animation=fadeIn" alt="Project Banner"/>
</p>

<p align="center">
  <b>A Real-Time Collaboration Platform Built with Django</b>  
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Platform-Web-green?style=flat-square&logo=googlechrome" />
  <img src="https://img.shields.io/badge/Language-Python-blueviolet?style=flat-square&logo=python" />
  <img src="https://img.shields.io/badge/Framework-Django-darkgreen?style=flat-square&logo=django" />
  <img src="https://img.shields.io/badge/Database-MySQL-blue?style=flat-square&logo=mysql" />
  <img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square" />
  <img src="https://img.shields.io/badge/Open%20Source-%E2%9C%94-blue?style=for-the-badge" />
</p>
<hr>
A powerful **Real-Time Collaboration Tool** built with **Django** to streamline project management, task assignment, and collaboration among team members. This app enables seamless task management, file sharing, and real-time interaction between project managers and team members.

<hr>

## 🛠️ Features

- **Admin Panel**:  
  - Create and manage project managers.  
  - View and manage all users and their tasks.  
  - Full control over the system and data.

- **Project Manager Panel**:  
  - Create and assign tasks.  
  - Collaborate with team members.  
  - Manage and track the status of tasks in real time.

- **User Panel**:  
  - View and update assigned tasks.  
  - Collaborate with other users.  
  - Upload, download, and delete files (with proper access).

- **File Management**:  
  - Integration with a drive to upload and manage files.  
  - Only authorized users can upload and delete files.

## 🚀 Getting Started

These instructions will help you get the app up and running on your local machine for development and testing purposes.

### Prerequisites

1. **Python** (Version 3.8 or higher)
2. **Django** (Version 3.0 or higher)
3. **XAMPP** (for database)
4. **Git** (to clone the repo)

### Installation Steps

#### 1. Clone the repository

```bash
git clone https://github.com/aayush61203/Real-Time-Collaboration-Tool.git
```

#### 2. Navigate to the project directory

```bash
cd Real-Time-Collaboration-Tool
```

#### 3. Create a virtual environment

```bash
python -m venv env
```

#### 4. Activate the virtual environment

- **For Windows**:

```bash
.\env\Scripts\activate
```

- **For macOS/Linux**:

```bash
source env/bin/activate
```

#### 5. Install dependencies

```bash
pip install -r requirements.txt
```

#### 6. Set up the database

```bash
python manage.py migrate
```

#### 7. Create a superuser (Admin account)

```bash
python manage.py createsuperuser
```

#### 8. Run the development server

```bash
python manage.py runserver
```

## 👥 User Guide

### For Regular Users

1. **Sign Up/Login**:  
   - Navigate to the login page and enter your credentials to access the panel.  
   - If you don't have an account, contact the Admin to create one.

2. **View and Update Tasks**:  
   - Once logged in, navigate to your dashboard to see all your tasks.  
   - Click on a task to update its status, add comments, or mark it as complete.

3. **Collaborate with Team**:  
   - You can chat and share files with your team members directly on the platform.

4. **File Management**:  
   - If you have upload access, use the "Files" section to upload files.  
   - You can also delete files if you have the necessary permissions.

### For Developers

1. **Clone the Repository**:  
   Use the GitHub link to clone the repository and make local changes.

2. **Set up the Development Environment**:  
   Follow the steps mentioned under "Getting Started" to set up the environment.

3. **Add New Features**:  
   - You can add new features by modifying the `views.py`, `models.py`, and `templates` directory.  
   - Use Django’s ORM to interact with the database.

4. **Push Changes to GitHub**:  
   After making changes, push them back to your GitHub repository to keep the project updated.



## 🎨 UI & UX

- Designed with **simplicity** and **usability** in mind.  
- **Responsive** interface for a seamless experience on both desktop and mobile.  
- **Real-time updates** for task management and collaboration, providing instant feedback and status changes.

## 📂 Documents and PPT

- [**Documents**](./Documents): Detailed documentation for understanding the app's setup, usage, and technical aspects.

## 📧 Contact Details

- **Email**: [contactaayushshah@gmail.com](mailto:contactaayushshah@gmail.com)
- **GitHub**: [@aayush61203](https://github.com/aayush61203)

---

Feel free to reach out if you have any questions or need assistance!
