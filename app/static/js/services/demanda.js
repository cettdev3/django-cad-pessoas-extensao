async function createDemanda(route="/ticket_form_collapsable", data, callback=null) {
    toggleLoading("show")
    return await $.ajax({
        url: route,
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

async function modalImportDemanda(formData, callback=null) {
    console.log(formData)
    toggleLoading("modal import demanda")
    return await $.ajax({
        url: "/importDemandaModal",
        processData: false,  // importante para enviar como arquivo
        contentType: false,  // importante para enviar como arquivo
        data: formData,
        headers: { "X-CSRFToken":  XCSRFToken },
        method: "POST",
        success: function (data) {
            toggleLoading("after modal import demanda")
            if (callback) callback(data);
        },
        error: function (data) {
            console.log(data)
            toggleLoading("modal import demanda error")
            showFloatingMessage("Erro ao carregar modal para importar demanda", "alert-danger");
        }
    });
}

async function saveBatchDemanda(data, callback=null) {
    console.log(data)
    toggleLoading("save batch demandas")
    return await $.ajax({
        url: "/saveBatchDemanda",
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        method: "POST",
        contentType: 'application/json',
        processData: false,
        success: function (data) {
            toggleLoading("after save batch demandas")
            if (callback) callback(data);
        },
        error: function (data) {
            console.log(data)
            toggleLoading("save batch demandas error")
            showFloatingMessage("Erro ao carregar modal para importar demanda", "alert-danger");
        }
    });
}
