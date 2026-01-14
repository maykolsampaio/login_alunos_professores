from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from firebase_config import init_firestore
from firebase_admin import firestore

aluno_bp = Blueprint('aluno', __name__)
db = init_firestore()

@aluno_bp.route('/aluno/dashboard')
def dashboard():
    if 'user_id' not in session or session.get('user_tipo') != 'aluno':
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    user_nome = session.get('user_nome')
    user_tipo = session['user_tipo']

    # Carregar disciplinas onde o aluno está matriculado
    user_path = f"usuarios/{user_id}"
    disciplinas_query = db.collection('disciplinas').where('alunosRefs', 'array_contains', user_path).stream()
    
    disciplinas_do_aluno = []
    disc_ids = []
    for d in disciplinas_query:
        d_data = d.to_dict()
        d_data['id'] = d.id
        disc_ids.append(d.id)
        
        # Buscar dados do professor
        prof_ref = d_data.get('professorRef')
        if prof_ref:
            prof_id = prof_ref.split('/')[-1]
            prof_doc = db.collection('usuarios').document(prof_id).get()
            if prof_doc.exists:
                d_data['professor'] = prof_doc.to_dict()
        
        disciplinas_do_aluno.append(d_data)
    
    # Carregar todas as disciplinas disponíveis
    todas_disciplinas_ref = db.collection('disciplinas').stream()
    todas_disciplinas = []
    for d in todas_disciplinas_ref:
        if d.id not in disc_ids:
            d_data = d.to_dict()
            d_data['id'] = d.id
            todas_disciplinas.append(d_data)

    return render_template('aluno/dashboard_aluno.html', 
                         nome=user_nome, 
                         disciplinas=disciplinas_do_aluno,
                         todas_disciplinas=todas_disciplinas,
                         tipo=user_tipo)

@aluno_bp.route('/aluno/add_disciplina', methods=['POST'])
def add_disciplina():
    if session.get('user_tipo') != 'aluno':
        return redirect(url_for('dashboard'))

    user_id = session['user_id']
    disciplina_id = request.form.get('disciplina_id')

    if not disciplina_id:
        flash("Nenhuma disciplina selecionada!", "error")
        return redirect(url_for('aluno.dashboard'))

    user_path = f"usuarios/{user_id}"
    disc_ref = db.collection('disciplinas').document(disciplina_id)
    disc_doc = disc_ref.get()

    if disc_doc.exists:
        alunos = disc_doc.to_dict().get('alunosRefs', [])
        if user_path not in alunos:
            disc_ref.update({
                'alunosRefs': firestore.ArrayUnion([user_path])
            })
            flash("Matrícula realizada com sucesso!", "success")
        else:
            flash("Você já está matriculado nesta disciplina!", "warning")
    else:
        flash("Disciplina não encontrada!", "error")
    
    return redirect(url_for('aluno.dashboard'))

@aluno_bp.route('/aluno/remover_disciplina/<disciplina_id>', methods=['POST'])
def remover_disciplina(disciplina_id):
    if session.get('user_tipo') != 'aluno':
        return redirect(url_for('dashboard'))

    user_id = session['user_id']
    user_path = f"usuarios/{user_id}"
    disc_ref = db.collection('disciplinas').document(disciplina_id)
    
    disc_ref.update({
        'alunosRefs': firestore.ArrayRemove([user_path])
    })
    
    flash("Disciplina removida com sucesso!", "success")
    return redirect(url_for('aluno.dashboard'))
