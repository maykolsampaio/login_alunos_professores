from flask import Flask, redirect, url_for, session, flash
from firebase_config import init_firestore

# Logic imports
from logic.auth_logic import login_logic, logout_logic, trocar_senha_logic
from logic.admin_logic import dashboard_admin_logic, listar_usuarios_logic, criar_usuario_logic, toggle_usuario_logic, listar_disciplinas_logic, criar_disciplina_logic
from logic.aluno_logic import dashboard_aluno_logic, add_disciplina_logic, remover_disciplina_logic
from logic.professor_logic import dashboard_professor_logic
from logic.perfil_logic import perfil_logic, desativar_conta_logic
from utils.batch_import import importar_dados_em_lote

app = Flask(__name__)
app.secret_key = "a1b2c3d4e5"

# Initialize Firestore
db = init_firestore()

# --- Auth Routes ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    return login_logic()

@app.route('/logout')
def logout():
    return logout_logic()

@app.route('/trocar_senha', methods=['GET', 'POST'])
def trocar_senha():
    return trocar_senha_logic()

# --- Dashboard Router ---
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user_tipo = session.get('user_tipo')
    if user_tipo == 'aluno':
        return redirect(url_for('aluno_dashboard'))
    elif user_tipo == 'professor':
        return redirect(url_for('professor_dashboard'))
    elif user_tipo == 'admin':
        return redirect(url_for('admin_dashboard'))
    
    return redirect(url_for('login'))

# --- Admin Routes ---
@app.route('/admin/dashboard')
def admin_dashboard():
    return dashboard_admin_logic()

@app.route('/usuarios')
def listar_usuarios():
    return listar_usuarios_logic()

@app.route('/admin/criar_usuario', methods=['GET', 'POST'])
def criar_usuario():
    return criar_usuario_logic()

@app.route('/admin/toggle/<id_usuario>')
def toggle_usuario(id_usuario):
    return toggle_usuario_logic(id_usuario)

@app.route('/admin/disciplinas')
def admin_listar_disciplinas():
    return listar_disciplinas_logic()

@app.route('/admin/criar_disciplina', methods=['GET', 'POST'])
def criar_disciplina():
    return criar_disciplina_logic()

# --- Aluno Routes ---
@app.route('/aluno/dashboard')
def aluno_dashboard():
    return dashboard_aluno_logic()

@app.route('/aluno/add_disciplina', methods=['POST'])
def add_disciplina():
    return add_disciplina_logic()

@app.route('/aluno/remover_disciplina/<disciplina_id>', methods=['POST'])
def remover_disciplina(disciplina_id):
    return remover_disciplina_logic(disciplina_id)

# --- Professor Routes ---
@app.route('/professor/dashboard')
def professor_dashboard():
    return dashboard_professor_logic()

# --- Perfil Routes ---
@app.route('/perfil', methods=['GET', 'POST'])
def perfil():
    return perfil_logic()

@app.route('/perfil/desativar_conta')
def desativar_conta():
    return desativar_conta_logic()

# --- Utils Routes ---
@app.route("/add-dados-lote")
def adicionar_dados_em_lote():
    admins = db.collection('usuarios').where('tipo', '==', 'admin').limit(1).stream()
    if any(admins) and session.get('user_tipo') != 'admin':
        flash("Acesso não autorizado.", "error")
        return redirect(url_for('dashboard'))

    num_u, num_d = importar_dados_em_lote()
    flash(f"Importação concluída: {num_u} usuários e {num_d} disciplinas.", "success")
    return redirect(url_for('listar_usuarios'))

# Filters
from datetime import datetime
@app.template_filter('datetime_format')
def datetime_format(value):
    if not value: return ""
    try:
        return datetime.fromisoformat(value).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return value

if __name__ == '__main__':
    app.run(debug=True)
