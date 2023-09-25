async function getAlocacaoSelect(data, callback=null) {
    toggleLoading("select alocacao")
    return await $.ajax({
        url: "/alocacaoSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select alocacao")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select alocacao error")
            showFloatingMessage("Erro ao carregar select alocacaos", "alert-danger");
        }
    });
}

async function getFormAlocacaoMembroEquipe(data, callback=null) {
    return await $.ajax({
        url: "/formAlocacaoMembroEquipe",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select alocacao")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select alocacao error")
            showFloatingMessage("Erro ao carregar select alocacaos", "alert-danger");
        }
    });
}

async function updateAlocacao(alocacao_id, data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/editarAlocacao/"+alocacao_id,
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

async function createAlocacao(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/saveAlocacao",
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

async function removeAlocacao(alocacao_id, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/eliminarAlocacao/"+alocacao_id,
        headers: { "X-CSRFToken": XCSRFToken },
        method: "POST",
        success: function (data) {
            if (onSuccess) onSuccess(data);
        },
        error: function (data) {
            if (onError) onError(data);
        }
    });
}


function initializeAlocacaoMembroEquipeForm(alocacao_id, container = null) {
} 