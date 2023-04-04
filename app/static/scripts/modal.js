$(document).ready(function () {

    // Abrir modal de simulação no dashboard
    $('.userinfo').click(function () {
        var imovel_id = $(this).data('id');
        // Informações dinâmicas dentro do modal
        $.ajax({
            url: '/simulacao',
            type: 'post',
            data: { imovel_id: imovel_id },
            success: function (data) {
                $('.modal-body').html({});
                $('.modal-body').append(data.htmlresponse);
                $('#simularModal').modal('show');
            }
        });

        $('#simularModal').modal('show')
    });

    // Ação quando clicar no botão "vender" dentro do modal de venda no dashboard
    $('.vender').click(function () {

        var data = $("form").serialize();

        $.ajax({
            url: '/vender',
            type: "POST",
            data: data,
            success: function (data) {
                //fechar modal e redirecionar para imoveis vendidos
                $('#simularModal').modal('hide');
                window.location.replace('/vendidos')
            },
            error: function () {
                $('#simularModal').modal('hide');
                alert('Ocorreu algum problema com a venda!', 'danger')
            }
        });
    });

    

});