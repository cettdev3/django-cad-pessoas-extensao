async function getOrcamentoTable(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/orcamento-table",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            if (onSuccess) onSuccess(data);
        },
        error: function (data) {
            if (onError) onError(data);
        }
    });
}