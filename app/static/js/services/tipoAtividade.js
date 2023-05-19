async function getTipoAtividadeSelect(data, callback=null) {
    toggleLoading("select tipo atividade")
    return await $.ajax({
        url: "/tiposAtividadesSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select tipo atividade")
            // showFloatingMessage("Anexo adicionado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select tipo atividade error")
            showFloatingMessage("Erro ao carregar tipo atividade", "alert-danger");
        }
    });
}