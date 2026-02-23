from pydantic import BaseModel
from typing import Optional


class UsuarioSchema(BaseModel):
    nome: str
    email: str
    senha: str
    ativo: Optional[bool] 
    admin: Optional[bool] 

    class Config:
        from_attributes = True # parametro para vim no formato de classe e não dicionário


class PedidoSchema(BaseModel):
   
    usuario: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    senha: str

    class Config:
        from_atributes = True

class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    
    class Config:
        from_attributes = True

#schema para recebimento de dados
class ResponsePedidoSchema(BaseModel):
    id: int
    status: str
    preco: float
    
    class Config:
        from_attributes = True




# quamdo tenho uma estrutura a seguir de como enviar dados para uma rota, eu crio um schema, para validar os dados que são enviados para a rota, garantindo que os dados estão no formato correto, e também para facilitar a documentação da API, pois o schema é usado para gerar a documentação da API, mostrando quais são os campos esperados e quais são os tipos de dados esperados.