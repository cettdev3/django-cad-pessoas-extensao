async function createDemanda(data, callback=null) {
    toggleLoading("show")
    return await $.ajax({
        url: "/ticket_form_collapsable",
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            console.log("demanda after")
            toggleLoading("hide")
            showFloatingMessage("Demanda adicionado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            console.log("demanda error")
            toggleLoading("hide")
            showFloatingMessage("Erro ao cadastrar demanda", "alert-danger");
        }
    });
}

async function deleteDemanda(ticket_id, callback=null) {
    toggleLoading("deletar ticket")
    return await $.ajax({
        url: "/eliminarTicket/"+ticket_id,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after deletar ticket")
            showFloatingMessage("Demanda deletada com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("deletar ticket error")
            showFloatingMessage("Erro ao deletar demanda", "alert-danger");
        }
    });
}

async function updateDemanda(ticket_id, data, callback=null) {
    toggleLoading("update demanda")
    return await $.ajax({
        url: "/updateTicket/"+ticket_id,
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("after update demanda")
            showFloatingMessage("Demanda editada com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            console.log(data)
            toggleLoading("update demanda error")
            showFloatingMessage("Erro ao cadastrar demanda", "alert-danger");
        }
    });
}
