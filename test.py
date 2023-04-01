from enum import Enum

class TipoTypes(Enum):
    lote = 1
    apartamento = 2


print(type(TipoTypes.lote.value))    