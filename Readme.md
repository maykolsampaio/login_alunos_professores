# 🎓 LAPEC - Sistema de Gerenciamento de Usuários

Sistema modular desenvolvido com **Flask** e **Firebase Firestore** para gestão de alunos, professores e administradores. O projeto utiliza uma arquitetura baseada em lógica separada e templates organizados por contexto.

---

## 🚀 Funcionalidades por Perfil

### 🛡️ Administrador
- **Dashboard Estatístico**: Visualização de métricas de usuários e disciplinas.
- **Gestão de Usuários**: Criação, ativação/desativação e alteração de privilégios.
- **Gestão de Disciplinas**: Cadastro e listagem de matérias disponíveis.
- **Importação em Lote**: Utilitário para carga inicial de dados via JSON.

### 👨‍🏫 Professor
- **Dashboard do Professor**: Visão geral de suas atividades.
- **Listagem de Alunos**: Acesso à lista de estudantes cadastrados no sistema.

### 👨‍🎓 Aluno
- **Dashboard do Aluno**: Gestão de matrículas em disciplinas.
- **Disciplinas**: Matrícula e cancelamento em matérias ofertadas.
- **Listagem de Professores**: Consulta aos docentes do sistema.

### 🔑 Geral
- **Autenticação Segura**: Login com hash de senha e controle de sessão.
- **Perfil do Usuário**: Alteração de dados pessoais e troca de senha obrigatória no primeiro acesso.
- **Auto-Desativação**: Opção para que qualquer usuário desative sua própria conta.

---

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.10+ / [Flask](https://flask.palletsprojects.com/)
- **Banco de Dados**: [Firebase Firestore](https://firebase.google.com/docs/firestore)
- **Frontend**: HTML5, Vanilla CSS, JavaScript (ES6+)
- **Estrutura**: Lógica de negócio modularizada e Blueprints

---

## 📂 Estrutura do Projeto

```text
├── app.py                # Entrada principal da aplicação e rotas
├── firebase_config.py    # Configuração da conexão com Firestore
├── logic/                # Módulos de lógica de negócio
│   ├── admin_logic.py
│   ├── aluno_logic.py
│   ├── auth_logic.py
│   └── ...
├── static/               # Arquivos estáticos (CSS, JS, Imagens)
├── templates/            # Templates Jinja2 organizados por pastas
└── utils/                # Utilitários (Importação em lote, etc.)
```

---

## ⚙️ Configuração e Instalação

### 1. Clonar o Repositório
```bash
git clone <url-do-repositorio>
cd login_alunos_professores
```

### 2. Ambiente Virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 3. Dependências
```bash
pip install -r requirements.txt
```

### 4. Configuração Firebase
1. **Console do Firebase**: No console do Firebase, vá em "Configurações do Projeto" > "Contas de Serviço".
2. **Chave Privada**: Clique em "Gerar nova chave privada" para baixar o arquivo JSON de credenciais.
3. **Arquivo Local**: Renomeie o arquivo baixado para `firebase.json` e coloque-o na raiz do projeto.
4. **Script de Inicialização**: O arquivo `firebase_config.py` utiliza esse JSON para estabelecer a conexão via `firebase-admin`.

> [!WARNING]
> Nunca adicione o arquivo `firebase.json` ao controle de versão (git). Ele já está incluído no `.gitignore`.

---

## 📊 Estrutura de Dados (Firestore)

### Coleção `usuarios`
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `nome` | String | Nome completo do usuário |
| `email` | String | E-mail institucional |
| `matricula`| String | Identificador único (E-mail ou ID numérico) |
| `tipo` | String | `aluno`, `professor` ou `admin` |
| `sexo` | String | `M` ou `F` |
| `ativo` | Boolean| Status da conta (Ativa/Desativada) |
| `primeiro_login` | Boolean | Controle para troca de senha obrigatória |
| `criado_em` | Timestamp | Data e hora da criação do perfil |

### Coleção `disciplinas`
| Campo | Tipo | Descrição |
| :--- | :--- | :--- |
| `nome` | String | Nome da disciplina |
| `ementa` | String | Descrição resumida do conteúdo |
| `professorRef` | DocumentReference | Referência ao documento do professor (`usuarios/ID`) |
| `alunosRefs` | Array of References | Lista de referências dos alunos matriculados |

---

## 📥 Importação de Dados
Para realizar uma carga inicial de teste, acesse a rota `/add-dados-lote` logado como administrador (ou antes de criar o primeiro admin). O sistema processará o arquivo `usuarios.json` e populará as coleções.

---

## 📝 Licença
Este sistema foi desenvolvido para fins educacionais e de pesquisa no **LAPEC**.