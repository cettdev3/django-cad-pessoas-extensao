async function getDepartamentoSelect(data, callback=null) {
    toggleLoading("select departamento")
    return await $.ajax({
        url: "/departamentosSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select departamentos")
            // showFloatingMessage("Anexo adicionado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select departamento error")
            showFloatingMessage("Erro ao carregar departamentos", "alert-danger");
        }
    });
}