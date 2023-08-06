__all__ = [
        'VisitType',
]

from dtmodel.dtfield.base_enum import BaseEnum



class VisitType(BaseEnum):
    CI = 'Inicial'
    CO = 'Seguimento'
    CE = 'Encaixe'
    CC = 'Cortesia'
    CP = 'Breve'
    RT = 'Retorno'
    VH = 'Hospitalar'
    VD = 'Domiciliar'
    
