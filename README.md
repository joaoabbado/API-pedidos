# 🚀 API de Pedidos

API desenvolvida com **FastAPI** para autenticação de usuários e gerenciamento de pedidos.

---

## 📌 Funcionalidades

* 🔐 Autenticação com JWT
* 👤 Cadastro e login de usuários
* 🔄 Refresh token
* 📦 Criação e gerenciamento de pedidos
* ➕ Adição e remoção de itens
* ✅ Finalização e cancelamento de pedidos

---

## 🛠️ Tecnologias utilizadas

* Python
* FastAPI
* Uvicorn
* SQLAlchemy
* Alembic
* SQLite
* JWT (python-jose)
* Bcrypt

---

## 📁 Estrutura do projeto

```
PROJETOFastAPI/
│
├── alembic/            # Migrações do banco
├── database/           # Arquivos do banco (SQLite)
├── auth_routes.py      # Rotas de autenticação
├── order_routes.py     # Rotas de pedidos
├── models.py           # Modelos do banco
├── schemas.py          # Schemas (Pydantic)
├── dependencies.py     # Dependências (auth, db, etc)
├── main.py             # Arquivo principal da API
├── requirements.txt    # Dependências do projeto
├── .env                # Variáveis de ambiente (não versionado)
└── .gitignore
```

---

## ⚙️ Como rodar o projeto

### 1️⃣ Clonar ou baixar o projeto

```bash
git clone https://github.com/joaoabbado/API-pedidos.git
cd API-pedidos
```

ou baixe o ZIP pelo GitHub.

---

### 2️⃣ Criar ambiente virtual

```bash
python -m venv venv
```

---

### 3️⃣ Ativar ambiente virtual

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/Mac:**

```bash
source venv/bin/activate
```

---

### 4️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

---

### 5️⃣ Criar arquivo `.env`

Crie um arquivo `.env` na raiz do projeto com:

```
DATABASE_URL=sqlite:///./banco.db
SECRET_KEY=dev-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 6️⃣ Rodar migrações

```bash
alembic upgrade head
```

---

### 7️⃣ Iniciar a API

```bash
uvicorn main:app --reload
```

---

## 🌐 Acessar a API

* API: http://127.0.0.1:8000
* Documentação Swagger: http://127.0.0.1:8000/docs
* Documentação ReDoc: http://127.0.0.1:8000/redoc

---

## 📌 Observações

* O projeto utiliza **SQLite** para facilitar testes locais
* Em produção, recomenda-se utilizar PostgreSQL ou MySQL
* O `.env` não é versionado por segurança

---

## 👨‍💻 Autor

Desenvolvido por João Gabriel 🚀
