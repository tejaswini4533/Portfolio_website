from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "portfolio-dev-secret-key-2026")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech = db.Column(db.String(300), nullable=False)
    github = db.Column(db.String(300), default="https://github.com/tejaswini4533")
    demo = db.Column(db.String(300), default="#")
    featured = db.Column(db.Boolean, default=True)

PROJECTS = [
    {
        "title": "Smart Event Management System",
        "description": "A comprehensive full-stack event platform engineered with Flask and SQLite. Features automated attendee registration, dynamic seat/capacity tracking, real-time analytics dashboard, and administrative management.",
        "tech": "Python • Flask • SQLite • SQLAlchemy • Bootstrap 5 • Jinja2",
        "github": "https://github.com/tejaswini4533",
        "demo": "#",
        "featured": True
    },
    {
        "title": "Multi-Agent AI Shopping Assistant",
        "description": "An autonomous multi-agent system architecture that decomposes e-commerce workflows into dedicated agents for real-time product discovery, cross-store comparison, price tracking, and intelligent recommendations.",
        "tech": "Python • AI Agents • REST APIs • Prompt Engineering",
        "github": "https://github.com/tejaswini4533",
        "demo": "#",
        "featured": True
    },
    {
        "title": "Smart Attendance & Engagement Analytics",
        "description": "An academic intelligence project analyzing attendance data, quiz results, and assignment submissions to detect learning patterns, identify at-risk students, and deliver actionable engagement metrics.",
        "tech": "Python • Data Analysis • SQLite • Machine Learning Concepts",
        "github": "https://github.com/tejaswini4533",
        "demo": "#",
        "featured": True
    },
    {
        "title": "CodeChef Problem Solving & Algorithmic Suite",
        "description": "A verified collection of 500+ competitive programming challenges solved on CodeChef covering core data structures, algorithms, mathematical logic, and clean Python implementations.",
        "tech": "Python 3 • Algorithms • Data Structures • CodeChef",
        "github": "https://github.com/tejaswini4533",
        "demo": "https://www.codechef.com/users/tejaswini_313",
        "featured": True
    }
]

@app.route("/")
def home():
    projects = Project.query.order_by(Project.id.asc()).all()
    return render_template("index.html", projects=projects)

@app.route("/resume")
def view_resume():
    return send_from_directory("static", "resume.pdf", mimetype="application/pdf")

@app.route("/download-resume")
def download_resume():
    return send_from_directory("static", "resume.pdf", as_attachment=True, download_name="Bezawada_Hema_Tejaswini_Resume.pdf")

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()
    if not all([name, email, subject, message]):
        flash("Please fill in all contact fields before submitting.", "danger")
        return redirect(url_for("home") + "#contact")
    
    db.session.add(Message(name=name, email=email, subject=subject, message=message))
    db.session.commit()
    flash("Thank you! Your message has been received successfully. I will get back to you soon.", "success")
    return redirect(url_for("home") + "#contact")

@app.route("/api/projects")
def api_projects():
    projects = Project.query.all()
    return jsonify([
        {
            "id": p.id,
            "title": p.title,
            "description": p.description,
            "tech": p.tech,
            "github": p.github,
            "demo": p.demo,
            "featured": p.featured
        }
        for p in projects
    ])

@app.route("/admin/messages")
def messages():
    items = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("messages.html", messages=items)

@app.route("/admin/messages/<int:message_id>/delete", methods=["POST"])
def delete_message(message_id):
    item = db.session.get(Message, message_id)
    if not item:
        abort(404)
    db.session.delete(item)
    db.session.commit()
    flash("Message deleted successfully.", "success")
    return redirect(url_for("messages"))

def seed_projects():
    existing = {p.title: p for p in Project.query.all()}
    for item in PROJECTS:
        if item["title"] in existing:
            p = existing[item["title"]]
            p.description = item["description"]
            p.tech = item["tech"]
            p.github = item["github"]
            p.demo = item["demo"]
            p.featured = item["featured"]
        else:
            db.session.add(Project(**item))
    db.session.commit()

with app.app_context():
    db.create_all()
    seed_projects()

if __name__ == "__main__":
    app.run(debug=True)
