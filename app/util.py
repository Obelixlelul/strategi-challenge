import re

# Função para mudar de formato de moeda brasileiro para formato aceito pelo db
def clean_currency_string(input_string):
    # remove R$
    digits_only = re.sub(r'R\$', '', input_string)
    # remove dots
    no_dots = digits_only.replace('.', '')
    # replace commas with dots
    clean_string = no_dots.replace(',', '.')
    return clean_string