async function getMembroExecucaoSelect(data, callback=null) {
    toggleLoading("select memebro execucao")
    return await $.ajax({
        url: "/membrosExecucaoSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select membres execucao")
            // showFloatingMessage("Anexo adicionado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select memebro execucao error")
            showFloatingMessage("Erro ao get select membro execucao", "alert-danger");
        }
    });
}