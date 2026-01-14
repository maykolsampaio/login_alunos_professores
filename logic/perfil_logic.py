from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash
from firebase_config import init_firestore

db = init_firestore()

def perfil_logic():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        sexo = request.form.get('sexo')
        senha = request.form.get('senha')

        novos_dados = {
            'nome': nome,
            'email': email,
            'sexo': sexo
        }

        if senha:
            confirmar_senha = request.form.get('confirmar_senha')
            if senha != confirmar_senha:
                flash("As senhas não coincidem!", "error")
                return redirect(url_for('perfil'))
            
            novos_dados['senha'] = generate_password_hash(senha)

        db.collection('usuarios').document(user_id).update(novos_dados)
        session['user_nome'] = nome
        flash("Dados atualizados!", "success")
        return redirect(url_for('perfil'))

    user_doc = db.collection('usuarios').document(user_id).get()
    if not user_doc.exists:
        session.clear()
        return redirect(url_for('login'))

    usuario = user_doc.to_dict()
    usuario['id'] = user_id
    return render_template('perfil/perfil.html', usuario=usuario)

def desativar_conta_logic():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    db.collection('usuarios').document(session['user_id']).update({
        'ativo': False
    })

    session.clear()
    flash("Conta desativada.", "success")
    return redirect(url_for('login'))
