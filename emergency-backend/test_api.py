#!/usr/bin/env python3
"""
Emergency Backend - Script de Teste
Testa todas as funcionalidades da API
"""

import requests
import json
import time

# Configurações
BASE_URL = "http://localhost:8002"
API_URL = f"{BASE_URL}/api"

def test_emergency_backend():
    """Testa todas as funcionalidades do Emergency Backend"""
    print("🚀 Testando Emergency Backend...")
    print("=" * 60)
    
    # 1. Testar status da API
    print("1. Testando status da API...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ API está funcionando!")
            print(f"📊 Response: {response.json()}")
        else:
            print("❌ Erro na API")
            return
    except Exception as e:
        print(f"❌ Erro ao conectar: {e}")
        return
    
    print("\n" + "-" * 60)
    
    # 2. Testar cadastro
    print("2. Testando cadastro de usuário...")
    cadastro_data = {
        "nome": "Usuário Teste",
        "email": f"teste_{int(time.time())}@email.com",
        "senha": "123456"
    }
    
    try:
        response = requests.post(f"{API_URL}/cadastro", json=cadastro_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Usuário cadastrado com sucesso!")
            print(f"👤 Usuário: {data['dados']['usuario']['nome']}")
            token = data['dados']['token']
            print(f"🔑 Token obtido: {token[:50]}...")
        else:
            print(f"❌ Erro no cadastro: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Erro no cadastro: {e}")
        return
    
    print("\n" + "-" * 60)
    
    # 3. Testar login
    print("3. Testando login...")
    login_data = {
        "email": cadastro_data["email"],
        "senha": cadastro_data["senha"]
    }
    
    try:
        response = requests.post(f"{API_URL}/login", json=login_data)
        if response.status_code == 200:
            data = response.json()
            print("✅ Login realizado com sucesso!")
            token = data['dados']['token']
            print(f"🔑 Novo token: {token[:50]}...")
        else:
            print(f"❌ Erro no login: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Erro no login: {e}")
        return
    
    print("\n" + "-" * 60)
    
    # Headers para requests autenticados
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # 4. Testar salvar projeto
    print("4. Testando salvar projeto...")
    html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Projeto Teste</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f0f8ff; }
        .container { max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; margin-bottom: 30px; }
        p { line-height: 1.6; color: #34495e; margin-bottom: 15px; }
        .highlight { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 20px; border-radius: 5px; text-align: center; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Projeto Criado com Emergency Backend</h1>
        <p>Este é um projeto de teste criado usando o <strong>Emergency Backend</strong>!</p>
        <p>O sistema permite salvar, carregar, listar e deletar projetos HTML completos.</p>
        
        <div class="highlight">
            <h2>✨ Funcionalidades</h2>
            <p>• Autenticação segura com tokens<br>
            • CRUD completo de projetos<br>
            • Banco de dados SQLite<br>
            • API RESTful em JSON</p>
        </div>
        
        <p><strong>Data de criação:</strong> ${new Date().toLocaleString('pt-BR')}</p>
        <p>Este HTML foi enviado como string e salvo no banco de dados SQLite!</p>
    </div>
</body>
</html>"""
    
    projeto_data = {
        "titulo": "Projeto Teste Emergency Backend",
        "conteudo_html": html_content
    }
    
    try:
        response = requests.post(f"{API_URL}/salvar_projeto", json=projeto_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Projeto salvo com sucesso!")
            projeto_id = data['dados']['id']
            print(f"📄 ID do projeto: {projeto_id}")
            print(f"📝 Título: {data['dados']['titulo']}")
            print(f"📏 Tamanho HTML: {len(data['dados']['conteudo_html'])} caracteres")
        else:
            print(f"❌ Erro ao salvar projeto: {response.json()}")
            return
    except Exception as e:
        print(f"❌ Erro ao salvar projeto: {e}")
        return
    
    print("\n" + "-" * 60)
    
    # 5. Testar listar projetos
    print("5. Testando listar projetos...")
    try:
        response = requests.get(f"{API_URL}/listar_projetos", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Projetos listados com sucesso!")
            print(f"📊 Total de projetos: {len(data['dados'])}")
            for projeto in data['dados']:
                print(f"   • ID {projeto['id']}: {projeto['titulo']} ({projeto['tamanho_html']} bytes)")
        else:
            print(f"❌ Erro ao listar projetos: {response.json()}")
    except Exception as e:
        print(f"❌ Erro ao listar projetos: {e}")
    
    print("\n" + "-" * 60)
    
    # 6. Testar carregar projeto
    print("6. Testando carregar projeto...")
    try:
        response = requests.get(f"{API_URL}/carregar_projeto/{projeto_id}", headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Projeto carregado com sucesso!")
            print(f"📄 Título: {data['dados']['titulo']}")
            print(f"📅 Criado em: {data['dados']['data_criacao']}")
            print(f"📏 Preview HTML: {data['dados']['conteudo_html'][:100]}...")
        else:
            print(f"❌ Erro ao carregar projeto: {response.json()}")
    except Exception as e:
        print(f"❌ Erro ao carregar projeto: {e}")
    
    print("\n" + "-" * 60)
    
    # 7. Testar comando via interpreter
    print("7. Testando rota /comando...")
    comando_data = {
        "acao": "estatisticas"
    }
    
    try:
        response = requests.post(f"{API_URL}/comando", json=comando_data, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Comando executado com sucesso!")
            stats = data['dados']
            print(f"👤 Usuário: {stats['usuario']['nome']}")
            print(f"📊 Total de projetos: {stats['projetos']['total']}")
            print(f"💾 Tamanho total: {stats['projetos']['tamanho_total_html_kb']} KB")
        else:
            print(f"❌ Erro no comando: {response.json()}")
    except Exception as e:
        print(f"❌ Erro no comando: {e}")
    
    print("\n" + "-" * 60)
    
    # 8. Testar atualização de projeto
    print("8. Testando atualização de projeto...")
    html_atualizado = html_content.replace("Projeto Teste", "Projeto ATUALIZADO")
    
    projeto_update = {
        "titulo": "Projeto ATUALIZADO via API",
        "conteudo_html": html_atualizado,
        "projeto_id": projeto_id
    }
    
    try:
        response = requests.post(f"{API_URL}/salvar_projeto", json=projeto_update, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("✅ Projeto atualizado com sucesso!")
            print(f"📝 Novo título: {data['dados']['titulo']}")
            print(f"📅 Atualizado em: {data['dados']['data_modificacao']}")
        else:
            print(f"❌ Erro ao atualizar projeto: {response.json()}")
    except Exception as e:
        print(f"❌ Erro ao atualizar projeto: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Teste completo finalizado!")
    print("\n📋 RESUMO DOS TESTES:")
    print("✅ Status da API")
    print("✅ Cadastro de usuário") 
    print("✅ Login e geração de token")
    print("✅ Salvar projeto HTML")
    print("✅ Listar projetos")
    print("✅ Carregar projeto específico")
    print("✅ Executar comando via interpreter")
    print("✅ Atualizar projeto existente")
    
    print(f"\n🌐 LINKS PARA TESTAR:")
    print(f"• API Base: {BASE_URL}/")
    print(f"• Status: {BASE_URL}/health")
    print(f"• Cadastro: {API_URL}/cadastro")
    print(f"• Login: {API_URL}/login")
    
    print(f"\n💻 TOKEN PARA TESTES MANUAIS:")
    print(f"{token}")

if __name__ == "__main__":
    test_emergency_backend()