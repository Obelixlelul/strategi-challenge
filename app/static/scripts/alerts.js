// Função para criar alertas

const alertPlaceholder = document.getElementById('liveAlertPlaceholder')

const alert = (message, type) => {
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
        `<div class="alert alert-${type} alert-dismissible" role="alert">`,
        `   <div>${message}</div>`,
        '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
        '</div>'
    ].join('')

    alertPlaceholder.append(wrapper)
}

// To fade out alerts
setTimeout(function() {
    const myDiv = document.getElementById('myAlert');
    myDiv.style.opacity = '0';
    setTimeout(function() {
      myDiv.remove();
    }, 1000); 
}, 3000);