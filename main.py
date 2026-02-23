from fastapi import FastAPI
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv
import os
from fastapi.responses import HTMLResponse
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI() # criando uma instancia do FastAPI

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
      <html>
        <head>
            <title>API de Pedidos</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 40px;
                    background-color: #f4f6f8;
                }
                h1 { color: #1e3a8a; }
                h2 { margin-top: 30px; }
                ul { line-height: 1.8; }
                .post { color: green; font-weight: bold; }
                .get { color: blue; font-weight: bold; }
            </style>
        </head>
        <body>
            <h1>🚀 API de Pedidos</h1>
            <p>API desenvolvida com FastAPI para autenticação e gerenciamento de pedidos.</p>

            <h2>🔐 Autenticação</h2>
            <ul>
                <li><span class="post">POST</span> /auth/criar_conta - Criar Conta</li>
                <li><span class="post">POST</span> /auth/login - Login</li>
                <li><span class="post">POST</span> /auth/login-form - Login via formulário</li>
                <li><span class="get">GET</span> /auth/refresh - Usar Refresh Token</li>
            </ul>

            <h2>📦 Pedidos</h2>
            <ul>
                <li><span class="get">GET</span> /pedidos/ - Listar pedidos</li>
                <li><span class="post">POST</span> /pedidos/pedido - Criar Pedido</li>
                <li><span class="post">POST</span> /pedidos/pedido/cancelar/{id_pedido} - Cancelar Pedido</li>
                <li><span class="get">GET</span> /pedidos/listar - Listar pedidos</li>
                <li><span class="post">POST</span> /pedidos/pedido/adicionar-item/{id_pedido} - Adicionar Item</li>
                <li><span class="post">POST</span> /pedidos/pedido/remover-item/{id_item_pedido} - Remover Item</li>
                <li><span class="post">POST</span> /pedidos/pedido/finalizar/{id_pedido} - Finalizar Pedido</li>
                <li><span class="get">GET</span> /pedidos/pedido/{id_pedido} - Visualizar Pedido</li>
                <li><span class="get">GET</span> /pedidos/listar/pedidos-usuario - Listar Pedidos do Usuário</li>
            </ul>

            <h2>📘 Documentação</h2>
            <p>
                Swagger: <a href="/docs">/docs</a><br>
                ReDoc: <a href="/redoc">/redoc</a>
            </p>
        </body>
    </html>
    """

bcrypt_context =CryptContext(schemes=["bcrypt"], deprecated="auto") # criando um contexto de criptografia usando bcrypt
oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "/auth/login-form") # criando um esquema de autenticação usando OAuth2, definindo a rota para login onde o token será gerado

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)  # incluindo as rotas de autenticação no app
app.include_router(order_router)
# para rodar  codigo, executar no terminal: uvicorn main:app --reload

# ENDPOINT:
# /ordens (PATH)

# REST APIs
#  Get > leitura
# Post > criar
# Put Alterar
# Delete deletar


#bcrypt para criptografar a senha do usuario, para isso precisamos instalar a biblioteca bcrypt, usando o comando: pip install bcrypt

#migração: alembic revision --autogenerate -m "create orders table"
#migração: alembic upgrade head
