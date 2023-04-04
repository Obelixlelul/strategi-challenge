from app.models import *


# To populate database
def populate():
    # Populate corretores
    corretores = [Corretor(nome='gabriel', senha='123456')]
    for corretor in corretores:
        db.session.add(corretor)
    
    # Populate tipo (apartamento ou lote) 
    tipos = [Tipo(nome='lote'), Tipo(nome='apartamento')]
    for tipo in tipos:
        db.session.add(tipo)

    # Populate clientes 
    clientes = [Cliente(nome='neto', cpf='08999725430', email='netao@gmail.com', telefone='84998471133'), 
                Cliente(nome='tubiba', cpf='08999725431', email='tubiba@gmail.com', telefone='84998471134'),
                Cliente(nome='ayrton', cpf='08999725432', email='airton@gmail.com', telefone='84998471135'),
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
                    'natal', '1798', 'd104', 180000.95, 5),
                    Imovel("quatro estações", TipoTypes.apartamento.value, '59064720', 
                    'av.brancas dunas', 'candelária', 
                    'natal', '65', 'primavera 304', 220000.95, 5),
                    Imovel("cond. resid. panamericano", TipoTypes.apartamento.value, '59151903', 
                    'av. maria lacerda montenegro', 'parnamirim', 
                    'natal', '515', 'a602', 140000.45, 5),
                    Imovel("residencial monte carlo", TipoTypes.apartamento.value, '59151180', 
                    'av. me. teresa de calcutá', 'parque dos eucaliptos', 
                    'natal', '836', 'e303', 175000.95, 5),
                    Imovel("westPark boulevard", TipoTypes.lote.value, '59054280', 
                    'r. raimundo chaves', 'candelária', 
                    'natal', '1652', 'l14', 360000.95, 5),
                    Imovel("greenwoods", TipoTypes.lote.value, '59030500', 
                    'av. jaguarari', 'candelária', 
                    'natal', '1798', 'l98', 360000.95, 5),
                    Imovel("Corais de Ponta Negra", TipoTypes.apartamento.value, '59090500', 
                    'r. da lagoa', 'ponta negra', 
                    'natal', '466', 'f404', 360000.95, 5),
                    Imovel("Alphavile", TipoTypes.apartamento.value, '59066042', 
                    'av.alphaville', 'parnamirim', 
                    'natal', 's/n', 'l55', 360000.95, 5),]
    for imovel in imoveis:    
        db.session.add(imovel)

    # Populate venda
    venda1 = Venda(1,1,1,1, 35000.55)
    db.session.add(venda1)

    db.session.commit()
