async function updateItemOrcamento(item_orcamento_id, data, onSuccess=null, onError=null) {
    console.log("dentro de update Item de orcamento",data)
    return await $.ajax({
        url: "/update-item-orcamento/"+item_orcamento_id,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        data: JSON.stringify(data),
        success: function (data) {
            if (onSuccess) onSuccess(data);
        },
        error: function (data) {
            if (onError) onError(data);
        }
    });
}

async function createItemOrcamento(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/create-item-orcamento",
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        data: JSON.stringify(data),
        success: function (data) {
            if (onSuccess) onSuccess(data);
        },
        error: function (data) {
            if (onError) onError(data);
        }
    });
}

async function removeItemOrcamento(item_orcamento_id, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/remove-item-orcamento/"+item_orcamento_id,
        headers: { "X-CSRFToken": XCSRFToken },
        dataType: "json",
        method: "POST",
        success: function (data) {
            if (onSuccess) onSuccess(data);
        },
        error: function (data) {
            if (onError) onError(data);
        }
    });
}

async function getItemOrcamentoForm(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/item-orcamento-form",
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