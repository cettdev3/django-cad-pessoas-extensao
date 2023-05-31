async function getEventoSelect(data, callback=null) {
    toggleLoading("select evento")
    return await $.ajax({
        url: "/dp_eventosSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select evento")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select evento error")
            showFloatingMessage("Erro ao carregar evento", "alert-danger");
        }
    });
}