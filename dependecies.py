from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_scheme
from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from jose import jwt, JWTError


def pegar_sessao(): # função para pegar a sessão do banco de dados, usada como dependência nas rotas para acessar o banco de dados
    try:
        Session = sessionmaker(bind=db) # criando uma sessão de banco de dados
        session = Session() # instanciando a sessão
        yield session
    finally:
        session.close() # fechando a sessão após o uso, garantindo que os recursos sejam liberados adequadamente

def verificar_token(token: str = Depends(oauth2_scheme), session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = int(dic_info.get("sub"))    
    except JWTError:
        raise HTTPException(status_code=401, detail="ACESSO NEGADO, verifique a validade do token ")
    # verificar se token e valido
    #extrair o id do usuario do token
    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status_code=401, detail="ACESSO NEGADO")
    return usuario