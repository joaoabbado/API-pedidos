from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependecies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema, ResponsePedidoSchema
from models import Pedido, Usuario, ItemPedido
from typing import List

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)]) #definindo o prefixo e a tag para o grupo de rotas, tag usada na documentacao, e adicionando a dependência de verificação de token para todas as rotas do grupo

@order_router.get("/") #decorator 
async def pedidos():
    
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas do pedidos precisam de autenticação.
    """
    return {"mensagem": "Voce acessou a rotas de pedidos"}

@order_router.post("/pedido") 
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)):

    novo_pedido =Pedido(usuario= pedido_schema.usuario) # criando um novo pedido usando a classe Pedido do models.py, passando o id do usuario como parametro
    session.add(novo_pedido) # adicionando o novo pedido na sessão
    session.commit() # confirmando a transação no banco de dados
    return {"mensagem": f"Pedido criado com sucesso, ID do pedido: {novo_pedido.id}"}


# rota para cancelar um pedido, passando o id do pedido como parametro, verificando se o pedido existe, se o usuario é admin ou se é o dono do pedido, se não for, retorna um erro 401, se for, altera o status do pedido para cancelado e retorna uma mensagem de sucesso
@order_router.post("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)): # dependencia de verificar token permite pegar o usuario logado e verificar se ele é admin ou se é o dono do pedido, para permitir cancelar o pedido, passando o id do pedido como parametro
    #usuario.admin = true
    #usuario.id = pedido.usuario_id
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuario não autorizado para cancelar esse pedido")
    pedido.status = "CANCELADO"
    session.commit()
    return {
            "mensagem": f"Pedido número {pedido.id} cancelado com sucesso",
            "pedido": pedido
    } 

# rota para listar todos os pedidos, apenas para usuarios admin, passando a sessão do banco de dados e o usuario logado como dependências, verificando se o usuario é admin, se não for, retorna um erro 401, se for, retorna a lista de pedidos
@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail = "Você não tem permissão para fazer esta operação")
    else:
        pedidos = session.query(Pedido).all()
        return{
            "pedidos": pedidos
        }
# rota para adcionar item em um pedido
@order_router.post("/pedido/adcionar-item/{id_pedido}")
async def adcionar_item_pedido(id_pedido: int,item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail= "pedido não existente")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail= "Usuario não autorizado para adcionar item nesse pedido")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho, item_pedido_schema.preco_unitario, id_pedido) 
    session.add(item_pedido)
    pedido.calcular_preco()
    
    session.commit()
    return{
        "mensage": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }

# rota para remover item de um pedido
@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id == id_item_pedido).first()
    pedido = session.query(Pedido).filter(Pedido.id == item_pedido.pedido).first()
    if not item_pedido:
        raise HTTPException(status_code=400, detail= "Item no pedido não existente")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail= "Usuario não autorizado para remover item nesse pedido")
    session.delete(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "mensage": "Item removido com sucesso",
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido

    }
#rota para finalizar um pedido

@order_router.post("/pedido/finalizar/{id_pedido}")
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)): # dependencia de verificar token permite pegar o usuario logado e verificar se ele é admin ou se é o dono do pedido, para permitir cancelar o pedido, passando o id do pedido como parametro
    #usuario.admin = true
    #usuario.id = pedido.usuario_id
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuario não autorizado para finalizar esse pedido")
    pedido.status = "FINALIZADO"
    session.commit()
    return {
            "mensagem": f"Pedido número {pedido.id} finalizado com sucesso",
            "pedido": pedido
    } 

# rota para vizualizar um pedido

@order_router.get("/pedido/{id_pedido}")
async def vizualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, detail="Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Usuario não autorizado para vizualizar esse pedido")
    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }

# rota para vizualizar todos os pedidos de um usuario

@order_router.get("/listar/pedidos-usuario", response_model=List[ResponsePedidoSchema])
async def listar_pedidos(session: Session = Depends(pegar_sessao),usuario: Usuario = Depends(verificar_token)):
        pedidos = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()
        return pedidos