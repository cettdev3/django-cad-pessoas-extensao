async function getCidadeSelect(data, callback=null) {
    toggleLoading("select cidade")
    return await $.ajax({
        url: "/cidadesSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select cidade")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select cidade error")
            showFloatingMessage("Erro ao carregar cidade", "alert-danger");
        }
    });
}