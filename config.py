from app.models import *


# To populate database
def populate():
    # Populate corretores
    corretores = [Corretor(nome='rafael', senha='123456'), 
                  Corretor(nome='alcides', senha='123456'), 
                  Corretor(nome='cookie', senha='123456')]
    for corretor in corretores:
        db.session.add(corretor)
    
    # Populate tipo (apartamento ou lote) 
    tipos = [Tipo(nome='lote'), Tipo(nome='apartamento')]
    for tipo in tipos:
        db.session.add(tipo)

    # Populate clientes 
    clientes = [Cliente(nome='neto', cpf='08999725430', email='netao@gmail.com', telefone='84998471133'), 
                Cliente(nome='tubiba', cpf='08999725431', email='tubiba@gmail.com', telefone='84998471134'),
                Cliente(nome='airton', cpf='08999725432', email='airton@gmail.com', telefone='84998471135'),
                Cliente(nome='thiago', cpf='08999725433', email='thiago@gmail.com', telefone='84998471136'),
                Cliente(nome='nilson', cpf='08999725434', email='nilson@gmail.com', telefone='84998471137')]           
    for cliente in clientes:
        db.session.add(cliente)

    # Populate condição de pagamento
    condicoes = [Condicao(nome='a vista'), Condicao(nome='180 parcelas')]
    for condicao in condicoes:
        db.session.add(condicao)

    # Populate imovel

    imoveis = [Imovel("residencial integração", TipoTypes.apartamento.value, '59066035', 
                    'av.governador tarcísio de vasconcelos maia', 'candelária', 
                    'natal', '1798', 'd104', 360000.95, 5),
                    Imovel("quatro estações", TipoTypes.apartamento.value, '59066036', 
                    'av.governador tarcísio de vasconcelos maia', 'candelária', 
                    'natal', '1798', 'd104', 360000.95, 5),
                    Imovel("residencial villa pitangueiras", TipoTypes.apartamento.value, '59066037', 
                    'av.governador tarcísio de vasconcelos maia', 'candelária', 
                    'natal', '1798', 'd104', 360000.95, 5),
                    Imovel("Alameda das mansões", TipoTypes.apartamento.value, '59066038', 
                    'av.governador tarcísio de vasconcelos maia', 'candelária', 
                    'natal', '1798', 'd104', 360000.95, 5),
                    Imovel("westPark boulevard", TipoTypes.lote.value, '59066039', 
                    'av.governador tarcísio de vasconcelos maia', 'candelária', 
                    'natal', '1798', 'd104', 360000.95, 5),
                    Imovel("greenwoods", TipoTypes.lote.value, '59066040', 
                    'av.governador tarcísio de vasconcelos maia', 'candelária', 
                    'natal', '1798', 'd104', 360000.95, 5),
                    Imovel("Corais de Ponta Negra", TipoTypes.apartamento.value, '59066041', 
                    'av.governador tarcísio de vasconcelos maia', 'candelária', 
                    'natal', '1798', 'd104', 360000.95, 5),
                    Imovel("Alphavile", TipoTypes.apartamento.value, '59066042', 
                    'av.governador tarcísio de vasconcelos maia', 'candelária', 
                    'natal', '1798', 'd104', 360000.95, 5),]
    for imovel in imoveis:    
        db.session.add(imovel)

    # Populate venda
    venda1 = Venda(1,1,1,1, 35000.55)
    db.session.add(venda1)

    db.session.commit()
