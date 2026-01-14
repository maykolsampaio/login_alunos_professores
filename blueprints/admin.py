from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from datetime import datetime
import random
import string
from firebase_config import init_firestore

admin_bp = Blueprint('admin', __name__)
db = init_firestore()

def gerar_matricula(tipo):
    if tipo == 'professor':
        return str(random.randint(10000, 99999))
    else:
        caracteres = string.ascii_uppercase + string.digits
        return ''.join(random.choices(caracteres, k=8))

@admin_bp.route('/admin/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('user_tipo') != 'admin':
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_nome = session.get('user_nome')
    user_tipo = session['user_tipo']

    todos_usuarios_ref = db.collection('usuarios').stream()
    todos_usuarios = [{**u.to_dict(), 'id': u.id} for u in todos_usuarios_ref]

    total_usuarios = len(todos_usuarios)
    total_alunos = sum(1 for u in todos_usuarios if u.get('tipo') == 'aluno')
    total_professores = sum(1 for u in todos_usuarios if u.get('tipo') == 'professor')
    
    alunos_masc = sum(1 for u in todos_usuarios if u.get('tipo') == 'aluno' and u.get('sexo') == 'M')
    alunos_fem = sum(1 for u in todos_usuarios if u.get('tipo') == 'aluno' and u.get('sexo') == 'F')

    todos_usuarios.sort(key=lambda x: x.get('criado_em', ''), reverse=True)
    recents = todos_usuarios[:5]

    return render_template(
        'admin/dashboard_admin.html',
        recents=recents,
        total_usuarios=total_usuarios,
        total_alunos=total_alunos,
        total_professores=total_professores,
        alunos_masc=alunos_masc,
        alunos_fem=alunos_fem,
        tipo=user_tipo,
        nome=user_nome
    )

@admin_bp.route('/admin/listar_usuarios')
def listar_usuarios():
    if session.get('user_tipo') != 'admin':
        return redirect(url_for('dashboard'))

    usuarios_ref = db.collection('usuarios').stream()
    usuarios = [{**u.to_dict(), 'id': u.id} for u in usuarios_ref]

    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/admin/criar_usuario', methods=['GET', 'POST'])
def criar_usuario():
    if session.get('user_tipo') != 'admin':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        tipo = request.form.get('tipo')
        sexo = request.form.get('sexo')
        area = request.form.get('area')
        disciplinas = request.form.getlist('disciplinas')

        while True:
            matricula = gerar_matricula(tipo)
            if not db.collection('usuarios').document(matricula).get().exists:
                break

        dados = {
            'nome': nome,
            'email': email,
            'matricula': matricula,
            'senha': generate_password_hash(matricula),
            'tipo': tipo,
            'sexo': sexo,
            'ativo': True,
            'primeiro_login': True,
            'criado_em': datetime.now().astimezone().isoformat()
        }
        
        if tipo == 'professor' and area:
            dados['area'] = area
        
        if tipo == 'aluno' and disciplinas:
            dados['disciplinas'] = disciplinas

        db.collection('usuarios').document(matricula).set(dados)
        flash(f"Usuário criado com sucesso! Matrícula: {matricula}", "success")
        return redirect(url_for('admin.listar_usuarios'))
    
    return render_template('admin/criar_usuario.html')

@admin_bp.route('/admin/toggle/<id_usuario>')
def toggle_usuario(id_usuario):
    if session.get('user_tipo') != 'admin':
        return redirect(url_for('dashboard'))

    user = db.collection('usuarios').document(id_usuario).get().to_dict()
    db.collection('usuarios').document(id_usuario).update({
        'ativo': not user['ativo']
    })
    return redirect(url_for('admin.listar_usuarios'))
