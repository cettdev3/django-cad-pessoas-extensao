async function getEscolaSelect(data, callback=null) {
    toggleLoading("select escola")
    return await $.ajax({
        url: "/escolasSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select escola")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select escola error")
            showFloatingMessage("Erro ao carregar escola", "alert-danger");
        }
    });
}