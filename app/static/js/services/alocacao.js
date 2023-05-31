async function getAlocacaoSelect(data, callback=null) {
    toggleLoading("select alocacao")
    return await $.ajax({
        url: "/alocacaoSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select alocacao")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select alocacao error")
            showFloatingMessage("Erro ao carregar select alocacaos", "alert-danger");
        }
    });
}