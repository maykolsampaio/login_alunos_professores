from flask import Blueprint, session, flash, redirect, url_for
from firebase_config import init_firestore
from utils.batch_import import importar_dados_em_lote

utils_bp = Blueprint('utils', __name__)
db = init_firestore()

@utils_bp.route("/add-dados-lote")
def adicionar_dados_em_lote():
    # Verifica se existe algum admin no banco
    admins = db.collection('usuarios').where('tipo', '==', 'admin').limit(1).stream()
    existe_admin = any(admins)

    # Se existe admin, exige que o usuário logado seja admin
    if existe_admin:
        if session.get('user_tipo') != 'admin':
            flash("Acesso não autorizado.", "error")
            return redirect(url_for('dashboard'))

    num_usuarios, num_disciplinas = importar_dados_em_lote()
    msg = f"Importação concluída: {num_usuarios} usuários e {num_disciplinas} disciplinas adicionados."
    flash(msg, "success")
    return redirect(url_for('admin.listar_usuarios'))
