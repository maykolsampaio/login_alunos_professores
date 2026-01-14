from flask import Flask, redirect, url_for, session
from dotenv import load_dotenv
import os
from firebase_config import init_firestore

# Local imports of blueprints
from blueprints.auth import auth_bp
from blueprints.admin import admin_bp
from blueprints.aluno import aluno_bp
from blueprints.professor import professor_bp
from blueprints.perfil import perfil_bp
from blueprints.utils import utils_bp

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(professor_bp)
app.register_blueprint(perfil_bp)
app.register_blueprint(utils_bp)

# Initialize Firestore
db = init_firestore()

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_tipo = session.get('user_tipo')
    
    if user_tipo == 'aluno':
        return redirect(url_for('aluno.dashboard'))
    elif user_tipo == 'professor':
        return redirect(url_for('professor.dashboard'))
    elif user_tipo == 'admin':
        return redirect(url_for('admin.dashboard'))
    
    return redirect(url_for('auth.login'))

# Keep custom filters if needed
from datetime import datetime
@app.template_filter('datetime_format')
def datetime_format(value):
    if not value: return ""
    try:
        date_obj = datetime.fromisoformat(value)
        return date_obj.strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value

if __name__ == '__main__':
    app.run(debug=True)
