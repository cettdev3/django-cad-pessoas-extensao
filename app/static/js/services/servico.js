function getServicos(data, callback = null) {
    toggleLoading("servicos")
    return $.ajax({
        url: "/getAtividadeDrawer/"+atividade_id,
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("servicos after")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("servicos error")
            showFloatingMessage("Erro ao carregar atividade", "alert-danger");
        }
    });
}

async function createServico(data, callback=null) {
    toggleLoading("show")
    return await $.ajax({
        url: "/saveServico",
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("hide")
            showFloatingMessage("Serviço adicionado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("hide")
            showFloatingMessage("Erro ao cadastrar serviço", "alert-danger");
        }
    });
}

async function updateServico(servico_id, data, callback=null) {
    toggleLoading("update servico")
    return await $.ajax({
        url: "/editarServico/"+servico_id,
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("after update servico")
            showFloatingMessage("Serviço editado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("update servico error")
            showFloatingMessage("Erro ao cadastrar serviço", "alert-danger");
        }
    });
}

function deleteServico(servico_id, callback = null) {
    toggleLoading("servico")
    return $.ajax({
        url: "/eliminarServico/"+servico_id,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("servico after")
            showFloatingMessage("Serviço deletado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("servico error")
            showFloatingMessage("Erro ao deletar serviço", "alert-danger");
        }
    });
}