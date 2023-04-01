import re

def clean_currency_string(input_string):
    # remove R$
    digits_only = re.sub(r'R\$', '', input_string)
    print('digits only = ', digits_only)
    # remove dots
    no_dots = digits_only.replace('.', '')
    print('no_dots = ', no_dots)
    # replace commas with dots
    clean_string = no_dots.replace(',', '.')
    print('no_dots = ', clean_string)
    return clean_string
