from flask import render_template, request, redirect, url_for, session, flash
from werkzeug.security import check_password_hash, generate_password_hash
from firebase_config import init_firestore

db = init_firestore()

def login_logic():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuarios = db.collection('usuarios') \
                     .where('email', '==', email) \
                     .stream()

        for u in usuarios:
            user = u.to_dict()

            if not user['ativo']:
                flash("Usuário desativado. Procure a administração.", "error")
                return redirect(url_for('login'))

            if check_password_hash(user['senha'], senha):
                session['user_id'] = u.id
                session['user_tipo'] = user['tipo']
                session['primeiro_login'] = user['primeiro_login']
                session['user_nome'] = user['nome']

                if user['primeiro_login']:
                    return redirect(url_for('trocar_senha'))

                return redirect(url_for('dashboard'))

        flash("Credenciais inválidas!", "error")
        return redirect(url_for('login'))
        
    return render_template('auth/login.html')

def logout_logic():
    session.clear()
    return redirect(url_for('login'))

def trocar_senha_logic():
    if not session.get('primeiro_login'):
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        nova_senha = request.form.get('senha')

        db.collection('usuarios').document(session['user_id']).update({
            'senha': generate_password_hash(nova_senha),
            'primeiro_login': False
        })

        session['primeiro_login'] = False
        flash("Senha alterada com sucesso!", "success")
        return redirect(url_for('dashboard'))

    return render_template('auth/trocar_senha.html')
