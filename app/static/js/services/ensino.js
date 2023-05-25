async function createEventoFromEnsino(ensino_id, data, callback = null) {
    toggleLoading("creaet evento from ação de ensino")
    return await $.ajax({
        url: "/createEventoFromEnsino/"+ensino_id,
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("creaet evento from ação de ensino after")
            showFloatingMessage("Evento criado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("creaet evento from ação de ensino error")
            showFloatingMessage(data.responseJSON.error, "alert-danger");
            if (callback) callback(null);
        }
    });
}