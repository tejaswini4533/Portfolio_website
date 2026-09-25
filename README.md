# Portfolio Website — Python + Flask

A professional, responsive, resume-ready portfolio website built with Python Flask, SQLite, HTML, CSS and JavaScript.

## Features

- Modern responsive portfolio UI
- Hero section with profile summary
- About, skills, education and experience sections
- Featured projects loaded from SQLite
- Project cards with GitHub/Demo links
- Contact form stored in SQLite
- Admin-style message inbox at `/admin/messages`
- Delete messages from inbox
- JSON API at `/api/projects`
- Mobile navigation
- Scroll reveal animations
- Download CV button placeholder
- Easy customization

## Tech Stack

Frontend:
- HTML5
- CSS3
- Bootstrap 5 CDN
- JavaScript

Backend:
- Python
- Flask
- Flask-SQLAlchemy

Database:
- SQLite

## VS Code / Windows Setup

Open the extracted project folder in VS Code.

### 1. Create virtual environment

```powershell
python -m venv .venv
```

### 2. Activate it

PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:
```cmd
.venv\Scripts\activate.bat
```

### 3. Install packages

```powershell
python -m pip install -r requirements.txt
```

### 4. Run

```powershell
python app.py
```

### 5. Open

http://127.0.0.1:5000

Admin messages:
http://127.0.0.1:5000/admin/messages

API:
http://127.0.0.1:5000/api/projects

## Stop Server

Press:
```text
CTRL + C
```

## Customize

Edit `templates/index.html` for your:
- name
- bio
- skills
- education
- experience
- social links
- resume link

Edit `app.py` to change the default projects.

## Add Your Resume

Place your PDF inside `static/` as:
`resume.pdf`

The Download CV button will then work.

## GitHub Upload

```powershell
git init
git add .
git commit -m "Create Python portfolio website"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

Do not commit `.venv/` or `instance/portfolio.db` if you don't want local environment/database files in GitHub.
