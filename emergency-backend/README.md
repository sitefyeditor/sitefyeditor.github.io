# Emergency Backend

Sistema completo de gerenciamento de projetos HTML com autenticação em Python Flask + SQLite.

## 🚀 Características

- **Autenticação Segura**: Cadastro e login com criptografia de senha usando werkzeug.security
- **Gerenciamento de Projetos**: CRUD completo para projetos HTML
- **API RESTful**: Todas as respostas em JSON padronizado
- **Sistema de Tokens**: Autenticação baseada em tokens com expiração
- **Banco SQLite**: Banco de dados local leve e eficiente
- **Arquitetura Modular**: Código organizado em módulos especializados

## 📁 Estrutura do Projeto

```
emergency-backend/
├── main.py                 # Servidor Flask principal
├── requirements.txt        # Dependências Python
├── README.md              # Documentação
├── api/                   # Rotas HTTP da aplicação
│   ├── __init__.py        # Registra blueprints no Flask
│   ├── routes.py          # Rotas públicas e protegidas
│   └── auth.py            # Sistema de autenticação
├── core/                  # Lógica interna do back-end
│   ├── interpreter.py     # Processa comandos JSON
│   └── actions.py         # Funções diretas de CRUD
├── database/              # Comunicação com SQLite
│   ├── db.py              # Conexão e inicialização
│   └── models.py          # Estrutura das tabelas
├── config/                # Configurações do sistema
│   └── settings.py        # Configurações centralizadas
└── utils/                 # Funções auxiliares
    ├── token_utils.py     # Geração e verificação de tokens
    └── session.py         # Validação de sessões
```

## 🛠️ Instalação e Execução

### 1. Instalar Dependências

```bash
cd emergency-backend
pip install -r requirements.txt
```

### 2. Executar o Servidor

```bash
python main.py
```

O servidor iniciará em `http://localhost:8001` (ou `http://0.0.0.0:8001`).

### 3. Variáveis de Ambiente (Opcional)

```bash
export FLASK_DEBUG=true          # Modo debug
export PORT=8001                 # Porta do servidor
export HOST=0.0.0.0             # Host do servidor
export SECRET_KEY=sua-chave-aqui # Chave secreta personalizada
```

## 📚 API Endpoints

### Autenticação

#### POST `/api/cadastro`
Cadastrar novo usuário.

**Request:**
```json
{
  "nome": "João Silva",
  "email": "joao@email.com", 
  "senha": "123456"
}
```

**Response:**
```json
{
  "status": "success",
  "mensagem": "Usuário cadastrado com sucesso",
  "dados": {
    "usuario": {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@email.com"
    },
    "token": "eyJkYXRhIjp7InVzdWFyaW9faWQi..."
  }
}
```

#### POST `/api/login`
Fazer login.

**Request:**
```json
{
  "email": "joao@email.com",
  "senha": "123456"
}
```

**Response:**
```json
{
  "status": "success",
  "mensagem": "Login realizado com sucesso", 
  "dados": {
    "usuario": {
      "id": 1,
      "nome": "João Silva",
      "email": "joao@email.com"
    },
    "token": "eyJkYXRhIjp7InVzdWFyaW9faWQi..."
  }
}
```

### Projetos (Requerem Autenticação)

**Cabeçalho obrigatório:**
```
Authorization: Bearer SEU_TOKEN_AQUI
```

#### POST `/api/salvar_projeto`
Salvar ou atualizar projeto HTML.

**Request:**
```json
{
  "titulo": "Meu Website",
  "conteudo_html": "<!DOCTYPE html><html>...</html>",
  "projeto_id": 1  // Opcional: para atualização
}
```

#### GET `/api/carregar_projeto/<id>`
Carregar projeto específico.

**Response:**
```json
{
  "status": "success",
  "mensagem": "Projeto carregado com sucesso",
  "dados": {
    "id": 1,
    "titulo": "Meu Website",
    "conteudo_html": "<!DOCTYPE html>...",
    "data_criacao": "2024-01-15 10:30:00",
    "data_modificacao": "2024-01-15 14:20:00"
  }
}
```

#### GET `/api/listar_projetos`
Listar todos os projetos do usuário.

**Response:**
```json
{
  "status": "success",
  "mensagem": "Encontrados 2 projetos",
  "dados": [
    {
      "id": 1,
      "titulo": "Meu Website",
      "data_criacao": "2024-01-15 10:30:00",
      "data_modificacao": "2024-01-15 14:20:00",
      "tamanho_html": 2048
    },
    {
      "id": 2,
      "titulo": "Landing Page",
      "data_criacao": "2024-01-16 09:15:00", 
      "data_modificacao": "2024-01-16 11:45:00",
      "tamanho_html": 4096
    }
  ]
}
```

#### DELETE `/api/deletar_projeto/<id>`
Deletar projeto.

**Response:**
```json
{
  "status": "success",
  "mensagem": "Projeto deletado com sucesso"
}
```

#### POST `/api/comando`
Executar comandos via JSON.

**Request:**
```json
{
  "acao": "salvar_projeto",
  "titulo": "Novo Site",
  "conteudo_html": "<!DOCTYPE html>..."
}
```

**Ações disponíveis:**
- `salvar_projeto`
- `carregar_projeto` (requer `projeto_id`)
- `listar_projetos`
- `deletar_projeto` (requer `projeto_id`)
- `estatisticas`
- `status_usuario`

## 💻 Exemplos de Uso com Fetch

### Cadastro de Usuário

```javascript
const cadastrarUsuario = async () => {
  try {
    const response = await fetch('http://localhost:8001/api/cadastro', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nome: 'João Silva',
        email: 'joao@email.com',
        senha: '123456'
      })
    });
    
    const data = await response.json();
    console.log('Usuário cadastrado:', data);
    
    // Salvar token para uso posterior
    localStorage.setItem('token', data.dados.token);
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

### Login

```javascript
const fazerLogin = async () => {
  try {
    const response = await fetch('http://localhost:8001/api/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: 'joao@email.com',
        senha: '123456'
      })
    });
    
    const data = await response.json();
    console.log('Login realizado:', data);
    
    // Salvar token
    localStorage.setItem('token', data.dados.token);
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

### Salvar Projeto HTML

```javascript
const salvarProjeto = async () => {
  const token = localStorage.getItem('token');
  
  const htmlCompleto = `
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Website</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; }
        h1 { color: #333; text-align: center; }
        p { line-height: 1.6; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bem-vindo ao Meu Website</h1>
        <p>Este é um site criado com o Emergency Backend!</p>
        <p>Aqui você pode adicionar todo o conteúdo HTML que desejar.</p>
    </div>
</body>
</html>`;
  
  try {
    const response = await fetch('http://localhost:8001/api/salvar_projeto', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        titulo: 'Meu Website Incrível',
        conteudo_html: htmlCompleto
      })
    });
    
    const data = await response.json();
    console.log('Projeto salvo:', data);
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

### Listar Projetos

```javascript
const listarProjetos = async () => {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch('http://localhost:8001/api/listar_projetos', {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const data = await response.json();
    console.log('Projetos encontrados:', data.dados);
    
    // Exibir projetos na interface
    data.dados.forEach(projeto => {
      console.log(`${projeto.id}: ${projeto.titulo} (${projeto.tamanho_html} bytes)`);
    });
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

### Carregar Projeto Específico

```javascript
const carregarProjeto = async (projetoId) => {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch(`http://localhost:8001/api/carregar_projeto/${projetoId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    });
    
    const data = await response.json();
    console.log('Projeto carregado:', data.dados);
    
    // Usar o HTML do projeto
    const htmlContent = data.dados.conteudo_html;
    console.log('HTML do projeto:', htmlContent);
    
    // Exemplo: abrir em nova janela
    const newWindow = window.open();
    newWindow.document.write(htmlContent);
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

### Usar Rota de Comando

```javascript
const executarComando = async () => {
  const token = localStorage.getItem('token');
  
  try {
    const response = await fetch('http://localhost:8001/api/comando', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        acao: 'estatisticas'
      })
    });
    
    const data = await response.json();
    console.log('Estatísticas:', data.dados);
  } catch (error) {
    console.error('Erro:', error);
  }
};
```

## 🗄️ Banco de Dados

### Tabela `usuarios`
- `id` (INTEGER, PRIMARY KEY)
- `nome` (VARCHAR 100, NOT NULL)
- `email` (VARCHAR 255, NOT NULL, UNIQUE)
- `senha_hash` (VARCHAR 255, NOT NULL)
- `data_criacao` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- `ultima_atividade` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

### Tabela `projetos`
- `id` (INTEGER, PRIMARY KEY)
- `usuario_id` (INTEGER, NOT NULL, FOREIGN KEY)
- `titulo` (VARCHAR 255, NOT NULL)
- `conteudo_html` (TEXT, NOT NULL)
- `data_criacao` (DATETIME, DEFAULT CURRENT_TIMESTAMP)
- `data_modificacao` (DATETIME, DEFAULT CURRENT_TIMESTAMP)

## 🔒 Segurança

- Senhas criptografadas com `werkzeug.security`
- Tokens com expiração de 24 horas
- Verificação de propriedade de projetos
- Validação de entrada em todas as rotas
- Headers CORS configurados
- Logs de auditoria

## 🚀 Deploy no Render

1. Conecte seu repositório no Render
2. Configure como "Web Service"
3. Comando de build: `pip install -r requirements.txt`
4. Comando de start: `python main.py`
5. Configure variáveis de ambiente se necessário

## 📝 Logs e Debug

O sistema registra logs detalhados de todas as operações:

- Autenticação de usuários
- Operações CRUD em projetos
- Erros e exceções
- Validação de tokens
- Atividade de sessões

Para debug, defina `FLASK_DEBUG=true`.

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT.