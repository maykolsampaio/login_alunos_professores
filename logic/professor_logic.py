from flask import render_template, redirect, url_for, session
from firebase_config import init_firestore

db = init_firestore()

def dashboard_professor_logic():
    if 'user_id' not in session or session.get('user_tipo') != 'professor':
        return redirect(url_for('login'))

    user_id = session['user_id']
    user_nome = session.get('user_nome')
    user_tipo = session['user_tipo']

    prof_id_str = f"usuarios/{user_id}"
    disciplinas_query = db.collection('disciplinas').where('professorRef', '==', prof_id_str).stream()
    
    minhas_disciplinas = []
    for d in disciplinas_query:
        d_data = d.to_dict()
        d_data['id'] = d.id
        
        alunos_matriculados = []
        alunos_refs = d_data.get('alunosRefs', [])
        for alu_path in alunos_refs:
            alu_id = alu_path.split('/')[-1]
            alu_doc = db.collection('usuarios').document(alu_id).get()
            if alu_doc.exists:
                alunos_matriculados.append(alu_doc.to_dict())
        
        d_data['alunos'] = alunos_matriculados
        minhas_disciplinas.append(d_data)
        
    return render_template('professor/dashboard_professor.html', 
                         nome=user_nome, 
                         disciplinas=minhas_disciplinas,
                         tipo=user_tipo)
