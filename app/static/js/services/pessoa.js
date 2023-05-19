async function getPessoaSelect(data, callback=null) {
    toggleLoading("select pessoa")
    return await $.ajax({
        url: "/pessoasSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get   pessoa")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select pessoa error")
            showFloatingMessage("Erro ao carregar select de pessoas", "alert-danger");
        }
    });
}