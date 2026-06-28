"""
Intelligent Resume Screening & Job Compatibility Analysis System
Main Flask Application
"""
import os
import json
from datetime import datetime
from urllib.parse import urlsplit
# pyrefly: ignore [missing-import]
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
# pyrefly: ignore [missing-import]
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# pyrefly: ignore [missing-import]
from werkzeug.security import generate_password_hash, check_password_hash
# pyrefly: ignore [missing-import]
from werkzeug.utils import secure_filename

from config import Config
from models.database import db, User, Resume, JobDescription, AnalysisResult
from nlp_engine.text_extractor import extract_text
from nlp_engine.skill_extractor import extract_skills_from_text
from nlp_engine.similarity import calculate_compatibility_score
from nlp_engine.gap_analyzer import analyze_gaps
from nlp_engine.recommender import generate_recommendations
from nlp_engine.ats_scorer import calculate_ats_score

# ═══════════════════════════════════════════════════════════════
# App Factory
# ═══════════════════════════════════════════════════════════════
app = Flask(__name__)
app.config.from_object(Config)
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def safe_next_url(target):
    if not target:
        return None
    parsed = urlsplit(target)
    if parsed.scheme or parsed.netloc:
        return None
    return target if target.startswith('/') else None


def remove_file_safely(path):
    if path and os.path.exists(path):
        try:
            os.remove(path)
        except OSError:
            app.logger.warning("Could not remove temporary file: %s", path)


# ═══════════════════════════════════════════════════════════════
# Routes — Auth
# ═══════════════════════════════════════════════════════════════

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip().lower()
        full_name = request.form.get('full_name', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        errors = []
        if not username or not email or not password:
            errors.append('All fields are required.')
        if password != confirm:
            errors.append('Passwords do not match.')
        if len(password) < 6:
            errors.append('Password must be at least 6 characters.')
        if User.query.filter_by(username=username).first():
            errors.append('Username already taken.')
        if User.query.filter_by(email=email).first():
            errors.append('Email already registered.')

        if errors:
            for e in errors:
                flash(e, 'danger')
            return render_template('register.html')

        user = User(username=username, email=email, full_name=full_name,
                    password_hash=generate_password_hash(password))
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Welcome back!', 'success')
            return redirect(safe_next_url(request.args.get('next')) or url_for('dashboard'))
        flash('Invalid email or password.', 'danger')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'info')
    return redirect(url_for('index'))


# ═══════════════════════════════════════════════════════════════
# Routes — Dashboard
# ═══════════════════════════════════════════════════════════════

@app.route('/dashboard')
@login_required
def dashboard():
    analyses = AnalysisResult.query.filter_by(user_id=current_user.id)\
        .order_by(AnalysisResult.analyzed_at.desc()).all()

    total = len(analyses)
    avg_score = round(sum(a.compatibility_score for a in analyses) / total, 1) if total else 0
    avg_ats = round(sum((a.ats_score or 0) for a in analyses) / total, 1) if total else 0
    best_score = max((a.compatibility_score for a in analyses), default=0)

    # Score trend data (last 10)
    recent = analyses[:10][::-1]
    trend_labels = [a.analyzed_at.strftime('%d %b') for a in recent]
    trend_scores = [a.compatibility_score for a in recent]

    return render_template('dashboard.html',
                           analyses=analyses[:5],
                           total=total, avg_score=avg_score,
                           avg_ats=avg_ats, best_score=best_score,
                           trend_labels=json.dumps(trend_labels),
                           trend_scores=json.dumps(trend_scores))


# ═══════════════════════════════════════════════════════════════
# Routes — Upload & Analysis
# ═══════════════════════════════════════════════════════════════

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        resume_file = request.files.get('resume')
        if not resume_file or resume_file.filename == '':
            flash('Please upload a resume file.', 'danger')
            return render_template('upload.html')
        if not allowed_file(resume_file.filename):
            flash('Invalid file type. Upload PDF or DOCX.', 'danger')
            return render_template('upload.html')

        # Job description
        jd_text = request.form.get('jd_text', '').strip()
        jd_file = request.files.get('jd_file')
        jd_title = request.form.get('jd_title', '').strip() or 'Untitled Job'
        jd_company = request.form.get('jd_company', '').strip()

        if jd_file and jd_file.filename and not allowed_file(jd_file.filename):
            flash('Invalid job description file type. Upload PDF or DOCX.', 'danger')
            return render_template('upload.html')

        if jd_file and jd_file.filename and allowed_file(jd_file.filename):
            jd_fname = secure_filename(jd_file.filename)
            jd_path = os.path.join(app.config['UPLOAD_FOLDER'], f"jd_{current_user.id}_{jd_fname}")
            try:
                jd_file.save(jd_path)
                jd_text = extract_text(jd_path)
            except Exception as e:
                app.logger.exception("Job description extraction failed")
                flash(f'Error reading job description: {e}', 'danger')
                return render_template('upload.html')
            finally:
                remove_file_safely(jd_path)

        if not jd_text:
            flash('Provide a job description (text or file).', 'danger')
            return render_template('upload.html')

        # Save resume
        fname = secure_filename(resume_file.filename)
        ts = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        saved_name = f"{current_user.id}_{ts}_{fname}"
        fpath = os.path.join(app.config['UPLOAD_FOLDER'], saved_name)
        resume_file.save(fpath)

        try:
            resume_text = extract_text(fpath)
        except Exception as e:
            remove_file_safely(fpath)
            app.logger.exception("Resume extraction failed")
            flash(f'Error reading resume: {e}', 'danger')
            return render_template('upload.html')

        if not resume_text.strip():
            remove_file_safely(fpath)
            flash('Could not extract text. Try another file.', 'danger')
            return render_template('upload.html')

        # ── NLP Pipeline ──
        try:
            resume_skills = extract_skills_from_text(resume_text)
            jd_skills = extract_skills_from_text(jd_text)

            scores = calculate_compatibility_score(resume_text, jd_text,
                                                   resume_skills, jd_skills)
            gaps = analyze_gaps(resume_skills, jd_skills)
            ats = calculate_ats_score(resume_text, jd_text, resume_skills, jd_skills)
            recs = generate_recommendations(gaps['missing_skills'],
                                            gaps['weak_areas'],
                                            scores['overall'])
        except Exception as e:
            remove_file_safely(fpath)
            app.logger.exception("Analysis pipeline failed")
            flash('Could not analyze the uploaded files. Please check the files and try again.', 'danger')
            return render_template('upload.html')

        # ── Save to DB ──
        resume_rec = Resume(user_id=current_user.id, filename=fname,
                            file_path=fpath, extracted_text=resume_text)
        try:
            db.session.add(resume_rec)
            db.session.flush()

            jd_rec = JobDescription(user_id=current_user.id, title=jd_title,
                                    company=jd_company, description_text=jd_text)
            db.session.add(jd_rec)
            db.session.flush()

            analysis = AnalysisResult(
                user_id=current_user.id,
                resume_id=resume_rec.id,
                job_description_id=jd_rec.id,
                compatibility_score=scores['overall'],
                ats_score=ats['score'],
                skill_match_score=scores['skill_score'],
                experience_relevance_score=scores['tfidf_score'],
                matched_skills=json.dumps(gaps['matched_skills']),
                missing_skills=json.dumps(gaps['missing_skills']),
                resume_skills=json.dumps(resume_skills),
                jd_skills=json.dumps(jd_skills),
                recommendations=json.dumps(recs),
                weak_areas=json.dumps(gaps['weak_areas']),
                ats_feedback=json.dumps(ats),
                score_breakdown=json.dumps(scores),
            )
            db.session.add(analysis)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            remove_file_safely(fpath)
            app.logger.exception("Saving analysis failed")
            flash('Could not save the analysis. Please confirm the database is running and try again.', 'danger')
            return render_template('upload.html')

        flash('Analysis complete!', 'success')
        return redirect(url_for('results', analysis_id=analysis.id))

    return render_template('upload.html')


# ═══════════════════════════════════════════════════════════════
# Routes — Results
# ═══════════════════════════════════════════════════════════════

@app.route('/results/<int:analysis_id>')
@login_required
def results(analysis_id):
    a = AnalysisResult.query.get_or_404(analysis_id)
    if a.user_id != current_user.id:
        flash('Unauthorized.', 'danger')
        return redirect(url_for('dashboard'))

    data = {
        'analysis': a,
        'matched_skills': json.loads(a.matched_skills or '{}'),
        'missing_skills': json.loads(a.missing_skills or '{}'),
        'resume_skills': json.loads(a.resume_skills or '{}'),
        'jd_skills': json.loads(a.jd_skills or '{}'),
        'recommendations': json.loads(a.recommendations or '{}'),
        'weak_areas': json.loads(a.weak_areas or '[]'),
        'ats_feedback': json.loads(a.ats_feedback or '{}'),
        'score_breakdown': json.loads(a.score_breakdown or '{}'),
    }
    return render_template('results.html', **data)


# ═══════════════════════════════════════════════════════════════
# Routes — History
# ═══════════════════════════════════════════════════════════════

@app.route('/history')
@login_required
def history():
    analyses = AnalysisResult.query.filter_by(user_id=current_user.id)\
        .order_by(AnalysisResult.analyzed_at.desc()).all()
    return render_template('history.html', analyses=analyses)


# ═══════════════════════════════════════════════════════════════
# REST API Endpoints (bonus — shows API design skill)
# ═══════════════════════════════════════════════════════════════

@app.route('/api/analysis/<int:analysis_id>', methods=['GET'])
@login_required
def api_analysis(analysis_id):
    a = AnalysisResult.query.get_or_404(analysis_id)
    if a.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify({
        'id': a.id,
        'compatibility_score': a.compatibility_score,
        'ats_score': a.ats_score,
        'skill_match_score': a.skill_match_score,
        'tfidf_score': a.experience_relevance_score,
        'matched_skills': json.loads(a.matched_skills or '{}'),
        'missing_skills': json.loads(a.missing_skills or '{}'),
        'recommendations': json.loads(a.recommendations or '{}'),
        'analyzed_at': a.analyzed_at.isoformat(),
    })


@app.route('/api/history', methods=['GET'])
@login_required
def api_history():
    analyses = AnalysisResult.query.filter_by(user_id=current_user.id)\
        .order_by(AnalysisResult.analyzed_at.desc()).all()
    return jsonify([{
        'id': a.id,
        'job_title': a.job_description.title,
        'score': a.compatibility_score,
        'ats_score': a.ats_score,
        'date': a.analyzed_at.isoformat(),
    } for a in analyses])


# ═══════════════════════════════════════════════════════════════
# Init DB & Run
# ═══════════════════════════════════════════════════════════════

with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"[WARNING] Could not connect to or initialize database: {e}")
        print("Check your database configuration or permissions.")
        print("Run 'python setup_db.py' to initialize the database.")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
