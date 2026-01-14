Gerenciamento de Usuários com Flask + Firestore

Aluno • Professor • Administrador

1️⃣ Modelo de Usuário (Firestore)

Todos os usuários ficam na coleção usuarios.

📌 Estrutura do Documento
{
  "nome": "Maria Silva",
  "email": "maria@ifpi.edu.br",
  "matricula": "202401",
  "senha": "hash_da_senha",
  "tipo": "aluno | professor | admin",
  "ativo": true,
  "primeiro_login": true
}

📌 Significado dos campos

tipo: define o perfil do usuário

ativo: usuário ativo ou desativado

primeiro_login: força troca de senha no primeiro acesso

2️⃣ Regras Gerais do Sistema
🔐 Perfis
Perfil	Pode fazer
Aluno	Ver professores + sua própria conta
Professor	Ver todos os alunos
Administrador	Ver todos os usuários
Administrador	Criar usuários
Administrador	Ativar/desativar usuários
Administrador	Alterar tipo (aluno ↔ professor)
🚫 Restrições Importantes

❌ Administrador não altera nome/email/senha de outros usuários

✔ Cada usuário só altera seus próprios dados

✔ Usuário pode desativar a própria conta

✔ Usuário não pode reativar conta desativada

3️⃣ Criação de Usuários (ADMIN ONLY)

📌 Somente o administrador cria usuários

📄 Regra de senha inicial

Senha inicial = matrícula

Usuário é obrigado a trocar a senha no primeiro login