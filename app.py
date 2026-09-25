from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "portfolio-dev-secret")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///portfolio.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    tech = db.Column(db.String(300), nullable=False)
    github = db.Column(db.String(300), default="#")
    demo = db.Column(db.String(300), default="#")
    featured = db.Column(db.Boolean, default=False)

PROJECTS = [
    {
        "title": "Smart Event Management System",
        "description": "A full-stack event platform for creating events, managing capacity, registering attendees and tracking statistics.",
        "tech": "Python • Flask • SQLite • Bootstrap • JavaScript",
        "github": "https://github.com/",
        "demo": "#",
        "featured": True
    },
    {
        "title": "Multi-Agent Shopping Assistant",
        "description": "An AI-oriented shopping assistant concept that separates product discovery, comparison and recommendation tasks into specialized agents.",
        "tech": "Python • AI Agents • APIs • Data Processing",
        "github": "https://github.com/",
        "demo": "#",
        "featured": True
    },
    {
        "title": "Smart Attendance & Engagement Scout",
        "description": "A student analytics project that combines attendance, quizzes, assignments and participation to identify learning patterns.",
        "tech": "Python • Data Analysis • Machine Learning",
        "github": "https://github.com/",
        "demo": "#",
        "featured": True
    }
]

@app.route("/")
def home():
    projects = Project.query.order_by(Project.id.desc()).all()
    return render_template("index.html", projects=projects)

@app.route("/contact", methods=["POST"])
def contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    subject = request.form.get("subject", "").strip()
    message = request.form.get("message", "").strip()
    if not all([name, email, subject, message]):
        flash("Please fill in all contact fields.", "danger")
        return redirect(url_for("home") + "#contact")
    db.session.add(Message(name=name, email=email, subject=subject, message=message))
    db.session.commit()
    flash("Thanks! Your message has been saved successfully.", "success")
    return redirect(url_for("home") + "#contact")

@app.route("/api/projects")
def api_projects():
    projects = Project.query.all()
    return jsonify([
        {"id": p.id, "title": p.title, "description": p.description,
         "tech": p.tech, "github": p.github, "demo": p.demo}
        for p in projects
    ])

@app.route("/admin/messages")
def messages():
    items = Message.query.order_by(Message.created_at.desc()).all()
    return render_template("messages.html", messages=items)

@app.route("/admin/messages/<int:message_id>/delete", methods=["POST"])
def delete_message(message_id):
    item = Message.query.get_or_404(message_id)
    db.session.delete(item)
    db.session.commit()
    flash("Message deleted.", "success")
    return redirect(url_for("messages"))

def seed_projects():
    if Project.query.count() == 0:
        for item in PROJECTS:
            db.session.add(Project(**item))
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_projects()

if __name__ == "__main__":
    app.run(debug=True)
