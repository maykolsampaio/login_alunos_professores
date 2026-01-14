from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from datetime import datetime
import random
import string
import re
import unicodedata
from firebase_config import init_firestore

db = init_firestore()

def gerar_matricula(tipo):
    if tipo == 'professor':
        return str(random.randint(10000, 99999))
    else:
        ano = datetime.now().year
        sufixo = str(random.randint(0, 9999)).zfill(4)
        return f"{ano}116ISINF{sufixo}"

def dashboard_admin_logic():
    if 'user_id' not in session or session.get('user_tipo') != 'admin':
        return redirect(url_for('login'))

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

def listar_usuarios_logic():
    if session.get('user_tipo') != 'admin':
        return redirect(url_for('dashboard'))

    usuarios_ref = db.collection('usuarios').stream()
    usuarios = [{**u.to_dict(), 'id': u.id} for u in usuarios_ref]

    return render_template('admin/usuarios.html', usuarios=usuarios)

def criar_usuario_logic():
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
        return redirect(url_for('listar_usuarios'))
    
    return render_template('admin/criar_usuario.html')

def toggle_usuario_logic(id_usuario):
    if session.get('user_tipo') != 'admin':
        return redirect(url_for('dashboard'))

    user = db.collection('usuarios').document(id_usuario).get().to_dict()
    db.collection('usuarios').document(id_usuario).update({
        'ativo': not user['ativo']
    })
    return redirect(url_for('listar_usuarios'))

def slugify(text):
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '_', text)

def listar_disciplinas_logic():
    if session.get('user_tipo') != 'admin':
        return redirect(url_for('dashboard'))

    disciplinas_ref = db.collection('disciplinas').stream()
    disciplinas = []
    for d in disciplinas_ref:
        d_data = d.to_dict()
        d_data['id'] = d.id
        
        prof_ref = d_data.get('professorRef')
        if prof_ref:
            prof_id = prof_ref.split('/')[-1]
            prof_doc = db.collection('usuarios').document(prof_id).get()
            if prof_doc.exists:
                d_data['professor_nome'] = prof_doc.to_dict().get('nome')
        
        disciplinas.append(d_data)

    return render_template('admin/disciplinas.html', disciplinas=disciplinas)

def criar_disciplina_logic():
    if session.get('user_tipo') != 'admin':
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nome = request.form.get('nome')
        ementa = request.form.get('ementa')
        professor_id = request.form.get('professor_id')

        if not nome or not professor_id:
            flash("Nome e Professor são obrigatórios!", "error")
            return redirect(url_for('criar_disciplina'))

        disciplina_id = slugify(nome)
        
        # Check if ID already exists
        if db.collection('disciplinas').document(disciplina_id).get().exists:
            # Add a random suffix if it exists
            disciplina_id += "_" + ''.join(random.choices(string.digits, k=4))

        dados = {
            'nome': nome,
            'ementa': ementa,
            'professorRef': f"usuarios/{professor_id}",
            'alunosRefs': []
        }

        db.collection('disciplinas').document(disciplina_id).set(dados)
        flash(f"Disciplina '{nome}' criada com sucesso!", "success")
        return redirect(url_for('admin_listar_disciplinas'))

    professores_ref = db.collection('usuarios').where('tipo', '==', 'professor').stream()
    professores = [{**p.to_dict(), 'id': p.id} for p in professores_ref]

    return render_template('admin/criar_disciplina.html', professores=professores)
