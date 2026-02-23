from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import ChoiceType

db =  create_engine("sqlite:///database/banco.db ") # cria conexao do banco de dados

# cria a base do banco
Base = declarative_base() # instanciando a base de modelos ORM

#criar as classe/tabelas do banco de dados
#usuario
#pedidos
#itensPedido

class Usuario(Base): # subclasse de Base que quem traduz uma classe para tabela no banco
    __tablename__ = "usuarios" # nome da tabela no banco de dados

    id = Column("id", Integer, primary_key=True, autoincrement=True)  #variavel e o nome do atributo da classe usuario e o id entre parenteses e o nome da coluna no banco
    nome= Column("nome",String)
    email= Column("email",String, nullable= False)
    senha=  Column("senha",String)
    ativo= Column("ativo", Boolean)
    admin= Column("admin", Boolean, default=False)

    def __init__(self, nome, email, senha, ativo= True, admin= False):

        self.nome = nome
        self.email = email
        self.senha = senha      
        self.ativo = ativo
        self.admin = admin
        
class Pedido(Base):
    __tablename__ = "pedidos"

    # STATUS_PEDIDOS = (
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ('FINALIZADO', 'FINALIZADO'),


    # )

    id =  Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # pendente, cancelado, finaluzado
    usuario = Column ("usuario", ForeignKey("usuarios.id")) # chave estrangeira para a tabela de usuarios
    preco = Column ("preco", Float)
    itens = relationship("ItemPedido",cascade="all, delete" )

    def __init__(self, usuario, status= "PENDENTE", preco = 0): 
        self.status = status
        self.usuario = usuario
        self.preco = preco
        
    def calcular_preco(self):
        
        self.preco = sum(item.preco_unitario * item.quantidade for item in self.itens)




class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedidos.id")) # chave estrangeira para a tabela de pedidos

    def __init__ (self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido
#executa a criação dos metadados do banco

#criar migração: alembic revision --autogenerate -m "create orders table"
# executar migração: alembic upgrade head