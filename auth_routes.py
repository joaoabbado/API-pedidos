from fastapi import APIRouter, Depends, HTTPException
from models import Usuario
from dependecies import pegar_sessao, verificar_token
from main import bcrypt_context, ALGORITHM,  ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(prefix="/auth", tags=["auth"]) #definindo o prefixo e a tag para o grupo de rotas, tag usada na documentacao

#criar token
def criar_token(id_usuario, duracao_token= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):  # funcao para criar token de autenticação
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_codificado = jwt.encode(dic_info,SECRET_KEY, ALGORITHM )
    return jwt_codificado





#autenciação de usuario
def autenticar_usuario(email,senha, session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first() # verificando se o email existe no banco de dados, usando a sessão para fazer uma consulta na tabela de usuarios, filtrando pelo email e pegando o primeiro resultado
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha): # verificando se a senha digitada é igual a senha criptografada no banco de dados, usando o contexto de criptografia criado anteriormente
        return False
    return usuario 

# endpoints


@auth_router.post("/criar_conta") #endpoint para criar conta, usando o metodo POST

async def criar_conta(usuario_schema:UsuarioSchema, session:Session = Depends(pegar_sessao) ): # definindo os parametros que a funcao vai receber, email, senha e nome, todos do tipo string
    
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first() # verificando se o email já existe no banco de dados, usando a sessão para fazer uma consulta na tabela de usuarios, filtrando pelo email e pegando o primeiro resultado
    if usuario: 
       raise HTTPException(status_code=400, detail="Email do usuário ja cadastrado")
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha) # criptografando a senha usando o contexto de criptografia criado anteriormente
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada,usuario_schema.ativo, usuario_schema.admin) # criando um novo usuario usando a classe Usuario do models.py
        session.add(novo_usuario) # adicionando o novo usuario na sessão
        session.commit() # confirmando a transação no banco de dados
        return {"mensagem": "Usuario criado com sucesso", "email": usuario_schema.email, "nome": usuario_schema.nome}
    

    # login > email e senha > token jwt 

@auth_router.post("/login")
async def login(login_schema:LoginSchema,session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session) # autenticando o usuario usando a funcao de autenticação criada anteriormente, passando o email, senha e a sessão como parametros
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado ou credenciais invalidas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token= timedelta(days=7))
        return{
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"}

@auth_router.post("/login-form")
async def login_form(dados_formulario: OAuth2PasswordRequestForm = Depends(),session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session) 
    
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuario nao encontrado ou credenciais invalidas")
    else:
        access_token = criar_token(usuario.id)
        return{
            "access_token": access_token,
            "token_type": "Bearer"}
 
@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)
    return{
        "access_token": access_token,
        "token_type": "Bearer"}
