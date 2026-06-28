from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    full_name = db.Column(db.String(150), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    resumes = db.relationship('Resume', backref='user', lazy=True, cascade='all, delete-orphan')
    analyses = db.relationship('AnalysisResult', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.username}>'


class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text, nullable=True)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Resume {self.filename}>'


class JobDescription(db.Model):
    __tablename__ = 'job_descriptions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(255), nullable=True)
    company = db.Column(db.String(255), nullable=True)
    description_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<JobDescription {self.title}>'


class AnalysisResult(db.Model):
    __tablename__ = 'analysis_results'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    job_description_id = db.Column(db.Integer, db.ForeignKey('job_descriptions.id'), nullable=False)

    # Scores
    compatibility_score = db.Column(db.Float, nullable=False)
    ats_score = db.Column(db.Float, nullable=True)
    skill_match_score = db.Column(db.Float, nullable=True)
    experience_relevance_score = db.Column(db.Float, nullable=True)

    # JSON data
    matched_skills = db.Column(db.Text, nullable=True)
    missing_skills = db.Column(db.Text, nullable=True)
    resume_skills = db.Column(db.Text, nullable=True)
    jd_skills = db.Column(db.Text, nullable=True)
    recommendations = db.Column(db.Text, nullable=True)
    weak_areas = db.Column(db.Text, nullable=True)
    ats_feedback = db.Column(db.Text, nullable=True)
    score_breakdown = db.Column(db.Text, nullable=True)

    analyzed_at = db.Column(db.DateTime, default=datetime.utcnow)

    resume = db.relationship('Resume', backref='analyses')
    job_description = db.relationship('JobDescription', backref='analyses')

    def __repr__(self):
        return f'<AnalysisResult {self.id} score={self.compatibility_score}>'