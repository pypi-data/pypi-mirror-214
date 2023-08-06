from dataclasses import dataclass
from typing import Optional


@dataclass
class Prestador:
    cnpj: str
    inscricao_municipal: int
    codigo_municipio: Optional[int] = None


@dataclass
class Endereco:
    logradouro: str
    numero: int
    complemento: Optional[str]
    bairro: str
    uf: str
    cep: int


@dataclass
class Tomador:
    cpf_cnpj: int
    razao_social: Optional[str] = None
    email: Optional[str] = None
    codigo_municipio: Optional[int] = None
    endereco: Optional[Endereco] = None
    inscricao_municipal: Optional[int] = None


@dataclass
class Servico:
    aliquota: int
    discriminacao: str
    iss_retido: bool
    item_lista_servico: int
    codigo_tributario_municipio: int
    valor_servicos: int


@dataclass
class RecepcionarLoteParams:
    data_emissao: str
    prestador: Prestador
    tomador: Tomador
    servico: Servico


@dataclass
class ConsultaLoteParams:
    protocolo: int
    cnpj: int
    inscricao_municipal: int
    codigo_municipio: int


@dataclass
class ConsultaRpsParams:
    numero: int
    serie: int
    tipo: int
    cnpj: int
    inscricao_municipal: int
    codigo_municipio: int


@dataclass
class ConsultaNfseParams:
    numero: int
    codigo_municipio: int
    data_inicial: str
    data_final: str
    prestador: Prestador
    tomador: Tomador


@dataclass
class CancelaNfseParams:
    numero: int
    cnpj: int
    inscricao_municipal: int
    codigo_municipio: int
    codigo_cancelamento: int


@dataclass
class ConsultaUrlVisualizacaoNfseParams:
    numero: int
    cnpj: int
    inscricao_municipal: int
    codigo_municipio: int
    codigo_tributacao_municipio: int
