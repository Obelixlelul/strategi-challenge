from flask import Blueprint

bpf = Blueprint('filters', __name__)

# Filtros para renderização das views pelo Jimja2

@bpf.app_template_filter()
def filterCurrency(numero):
    # Converte o número para uma string
    numero_str = str(numero)

    # Separa a parte inteira da parte decimal
    partes = numero_str.split('.')
    inteiro = partes[0]
    decimal = partes[1] if len(partes) > 1 else '00'

    # Adiciona os separadores de milhares
    if len(inteiro) > 3:
        partes_inteiro = []
        while inteiro:
            partes_inteiro.append(inteiro[-3:])
            inteiro = inteiro[:-3]
        inteiro = '.'.join(partes_inteiro[::-1])

    # Formata a parte decimal
    decimal = decimal[:2].ljust(2, '0')

    # Junta a parte inteira e a parte decimal
    moeda = f"R$ {inteiro},{decimal}"

    return moeda

@bpf.app_template_filter()
def filterPhone(value):
	telFormatado = '({}) {}-{}-{}'.format(value[0:2], value[2] ,value[3:7], value[7:])
	return telFormatado

@bpf.app_template_filter()
def filterCpf(value):
	telFormatado = '{}.{}.{}-{}'.format(value[0:3], value[3:6] ,value[6:9], value[9:])
	return telFormatado

@bpf.app_template_filter()
def filterDate(date):
	formatedDate = date.strftime("%d/%m/%Y")
	return formatedDate

@bpf.app_template_filter()
def filterCep(cep):
	formatedCep = '{}-{}'.format(cep[0:5], cep[5:])
	return formatedCep

