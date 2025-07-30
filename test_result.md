#====================================================================================================
# START - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================

# THIS SECTION CONTAINS CRITICAL TESTING INSTRUCTIONS FOR BOTH AGENTS
# BOTH MAIN_AGENT AND TESTING_AGENT MUST PRESERVE THIS ENTIRE BLOCK

# Communication Protocol:
# If the `testing_agent` is available, main agent should delegate all testing tasks to it.
#
# You have access to a file called `test_result.md`. This file contains the complete testing state
# and history, and is the primary means of communication between main and the testing agent.
#
# Main and testing agents must follow this exact format to maintain testing data. 
# The testing data must be entered in yaml format Below is the data structure:
# 
## user_problem_statement: {problem_statement}
## backend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.py"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## frontend:
##   - task: "Task name"
##     implemented: true
##     working: true  # or false or "NA"
##     file: "file_path.js"
##     stuck_count: 0
##     priority: "high"  # or "medium" or "low"
##     needs_retesting: false
##     status_history:
##         -working: true  # or false or "NA"
##         -agent: "main"  # or "testing" or "user"
##         -comment: "Detailed comment about status"
##
## metadata:
##   created_by: "main_agent"
##   version: "1.0"
##   test_sequence: 0
##   run_ui: false
##
## test_plan:
##   current_focus:
##     - "Task name 1"
##     - "Task name 2"
##   stuck_tasks:
##     - "Task name with persistent issues"
##   test_all: false
##   test_priority: "high_first"  # or "sequential" or "stuck_first"
##
## agent_communication:
##     -agent: "main"  # or "testing" or "user"
##     -message: "Communication message between agents"

# Protocol Guidelines for Main agent
#
# 1. Update Test Result File Before Testing:
#    - Main agent must always update the `test_result.md` file before calling the testing agent
#    - Add implementation details to the status_history
#    - Set `needs_retesting` to true for tasks that need testing
#    - Update the `test_plan` section to guide testing priorities
#    - Add a message to `agent_communication` explaining what you've done
#
# 2. Incorporate User Feedback:
#    - When a user provides feedback that something is or isn't working, add this information to the relevant task's status_history
#    - Update the working status based on user feedback
#    - If a user reports an issue with a task that was marked as working, increment the stuck_count
#    - Whenever user reports issue in the app, if we have testing agent and task_result.md file so find the appropriate task for that and append in status_history of that task to contain the user concern and problem as well 
#
# 3. Track Stuck Tasks:
#    - Monitor which tasks have high stuck_count values or where you are fixing same issue again and again, analyze that when you read task_result.md
#    - For persistent issues, use websearch tool to find solutions
#    - Pay special attention to tasks in the stuck_tasks list
#    - When you fix an issue with a stuck task, don't reset the stuck_count until the testing agent confirms it's working
#
# 4. Provide Context to Testing Agent:
#    - When calling the testing agent, provide clear instructions about:
#      - Which tasks need testing (reference the test_plan)
#      - Any authentication details or configuration needed
#      - Specific test scenarios to focus on
#      - Any known issues or edge cases to verify
#
# 5. Call the testing agent with specific instructions referring to test_result.md
#
# IMPORTANT: Main agent must ALWAYS update test_result.md BEFORE calling the testing agent, as it relies on this file to understand what to test next.

#====================================================================================================
# END - Testing Protocol - DO NOT EDIT OR REMOVE THIS SECTION
#====================================================================================================



#====================================================================================================
# Testing Data - Main Agent and testing sub agent both should log testing data below this section
#====================================================================================================

user_problem_statement: "Criar um servidor back-end completo em python chamado emergency-backend com estrutura de pastas organizada: pasta api contendo init.py que registra o blueprint do flask, routes.py com todas as rotas como login, cadastro, salvar_projeto, carregar_projeto, deletar_projeto e listar_projetos, e auth.py que implementa o sistema de autenticação usando email e senha com criptografia manual utilizando werkzeug.security, pasta core com interpreter.py que recebe json com o campo acao e redireciona para functions no arquivo actions.py, este por sua vez executa funções como salvar_projeto que salva o conteúdo html enviado no banco de dados, deletar_projeto, carregar_projeto e listar_projetos por usuário, pasta database com db.py que conecta ao banco sqlite3 e inicializa as tabelas se não existirem, e models.py que define a tabela usuarios com id, nome, email e senha_hash, e tabela projetos com id, usuario_id, titulo e conteudo_html tipo text, pasta config contendo settings.py com a SECRET_KEY do flask e configs gerais como path do banco, pasta utils contendo token_utils.py para gerar tokens simples baseados no id do usuário com timestamp e verificação, e session.py para validar tokens recebidos no header das rotas privadas, além disso inclua main.py na raiz que inicia o flask, registra os blueprints e roda o servidor, requirements.txt com flask, werkzeug e outras dependências, readme.md explicando como iniciar o projeto e exemplos de requisições com fetch, todas as respostas da api devem ser em json com campos como status, mensagem e dados, os projetos enviados serão arquivos html inteiros dentro de um campo conteudo_html e devem ser armazenados no banco e retornados como texto puro quando o usuário quiser abrir, também crie uma rota /comando que recebe um post com json contendo acao e dados e chama a função correspondente via interpreter, todas as rotas privadas devem exigir token de autenticação enviado pelo front-end no header Authorization, e no final me retorne o link da api flask iniciada e um exemplo de como usar fetch para enviar html completo como string e recuperar projetos salvos."

backend:
  - task: "Estrutura de pastas emergency-backend"
    implemented: true
    working: true
    file: "/app/emergency-backend/"
    stuck_count: 0
    priority: "high"
    needs_retesting: false
    status_history:
      - working: true
        agent: "main"
        comment: "Estrutura de pastas criada conforme especificação: api/, core/, database/, config/, utils/, main.py, requirements.txt, README.md"

  - task: "Sistema de autenticação com werkzeug.security"
    implemented: true
    working: true
    file: "/app/emergency-backend/api/auth.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Sistema completo implementado: cadastro, login, criptografia de senha, geração de tokens"

  - task: "Modelos de banco SQLite (usuarios e projetos)"
    implemented: true
    working: true
    file: "/app/emergency-backend/database/models.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Tabelas usuarios (id, nome, email, senha_hash) e projetos (id, usuario_id, titulo, conteudo_html) implementadas"

  - task: "Conexão e inicialização do banco SQLite"
    implemented: true
    working: true
    file: "/app/emergency-backend/database/db.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Conexão com SQLite, criação automática de tabelas, thread-safe connection management"

  - task: "Sistema de tokens com timestamp e verificação"
    implemented: true
    working: true
    file: "/app/emergency-backend/utils/token_utils.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Tokens baseados em hashlib, time, base64 com expiração de 24h e verificação de hash"

  - task: "Validação de sessões com tokens"
    implemented: true
    working: true
    file: "/app/emergency-backend/utils/session.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Validação de sessão ativa, verificação de tokens nos headers Authorization"

  - task: "Rotas da API (login, cadastro, CRUD projetos)"
    implemented: true
    working: true
    file: "/app/emergency-backend/api/routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Todas as rotas implementadas: /api/cadastro, /api/login, /api/salvar_projeto, /api/carregar_projeto, /api/listar_projetos, /api/deletar_projeto"

  - task: "Sistema interpreter e actions"
    implemented: true
    working: true
    file: "/app/emergency-backend/core/interpreter.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Interpreter recebe JSON com campo 'acao' e redireciona para functions em actions.py"

  - task: "Funções CRUD em actions.py"
    implemented: true
    working: true
    file: "/app/emergency-backend/core/actions.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Funções salvar_projeto, carregar_projeto, listar_projetos, deletar_projeto implementadas"

  - task: "Rota /comando com interpreter"
    implemented: true
    working: true
    file: "/app/emergency-backend/api/routes.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Rota /api/comando implementada, recebe JSON com 'acao' e chama interpreter"

  - task: "Configurações centralizadas"
    implemented: true
    working: true
    file: "/app/emergency-backend/config/settings.py"
    stuck_count: 0
    priority: "medium"
    needs_retesting: false
    status_history:
      - working: true
        agent: "main"
        comment: "SECRET_KEY, configurações do banco, tokens, CORS centralizadas"

  - task: "Servidor Flask principal"
    implemented: true
    working: true
    file: "/app/emergency-backend/main.py"
    stuck_count: 0
    priority: "high"
    needs_retesting: true
    status_history:
      - working: true
        agent: "main"
        comment: "Flask app com CORS, blueprints registrados, inicialização do banco"

  - task: "Documentação completa"
    implemented: true
    working: true
    file: "/app/emergency-backend/README.md"
    stuck_count: 0
    priority: "medium"
    needs_retesting: false
    status_history:
      - working: true
        agent: "main"
        comment: "README.md completo com exemplos de fetch, documentação de todas as rotas"

frontend:
  - task: "Integração com emergency-backend"
    implemented: false
    working: "NA"
    file: "frontend HTML files"
    stuck_count: 0
    priority: "low"
    needs_retesting: false
    status_history:
      - working: "NA"
        agent: "main"
        comment: "Frontend existente usa Firebase, pode ser integrado posteriormente"

metadata:
  created_by: "main_agent"
  version: "1.0"
  test_sequence: 1
  run_ui: false

test_plan:
  current_focus:
    - "Sistema de autenticação com werkzeug.security"
    - "Rotas da API (login, cadastro, CRUD projetos)"
    - "Sistema interpreter e actions"
    - "Servidor Flask principal"
  stuck_tasks: []
  test_all: true
  test_priority: "high_first"

agent_communication:
  - agent: "main"
    message: "Emergency Backend implementado completamente conforme especificação. Todas as funcionalidades principais estão funcionando: autenticação, CRUD de projetos, sistema de tokens, banco SQLite, interpreter de comandos. Servidor testado na porta 8002, todas as rotas respondendo corretamente. Pronto para testes completos."