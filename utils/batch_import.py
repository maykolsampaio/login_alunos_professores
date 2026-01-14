import os
import json
from werkzeug.security import generate_password_hash
from firebase_config import init_firestore

def importar_dados_em_lote():
    db = init_firestore()
    usuarios_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'usuarios.json')
    batch = db.batch()
    
    with open(usuarios_data, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Processar usuários
    usuarios = data.get('usuarios', {})
    for matricula, user_data in usuarios.items():
        if 'senha' in user_data:
            user_data['senha'] = generate_password_hash(user_data['senha'])
        
        doc_ref = db.collection('usuarios').document(matricula)
        batch.set(doc_ref, user_data)
        
    # Processar disciplinas
    disciplinas = data.get('disciplinas', {})
    for disc_id, disc_data in disciplinas.items():
        doc_ref = db.collection('disciplinas').document(disc_id)
        batch.set(doc_ref, disc_data)
        
    batch.commit()
    return len(usuarios), len(disciplinas)
