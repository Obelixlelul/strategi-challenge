// Mascara para telefone

const handlePhone = (event) => {
    let input = event.target
    input.value = phoneMask(input.value)
}

const phoneMask = (value) => {
if (!value) return ""
value = value.replace(/\D/g,'')
value = value.replace(/(\d{2})(\d)/,"($1) $2")
value = value.replace(/(\d)(\d{4})$/,"$1-$2")
return value
}


// Mascara para cpf

function cpfMascara(){
    let cpf = document.getElementById('cpf')
    if(cpf.value.length == 3 || cpf.value.length == 7){
        cpf.value += '.'
    }else if(cpf.value.length == 11){
        cpf.value += '-'
    }
}

function mascaraMoeda(event) {
    const onlyDigits = event.target.value
        .split("")
        .filter(s => /\d/.test(s))
        .join("")
        .padStart(3, "0")
    const digitsFloat = onlyDigits.slice(0, -2) + "." + onlyDigits.slice(-2)
    event.target.value = maskCurrency(digitsFloat)
}

function maskCurrency(valor, locale = 'pt-BR', currency = 'BRL') {
    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency
    }).format(valor)
}