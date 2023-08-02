async function getMembroExecucaoSelect(data, callback=null) {
    toggleLoading("select memebro execucao")
    return await $.ajax({
        url: "/membrosExecucaoSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select membres execucao")
            // showFloatingMessage("Anexo adicionado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select memebro execucao error")
            showFloatingMessage("Erro ao get select membro execucao", "alert-danger");
        }
    });
}

async function updateMembroEquipe(membro_equipe_id, data, onSuccess=null, onError=null) {
    console.log("dentro de update atividade",data)
    return await $.ajax({
        url: "/update-membro-equipe/"+membro_equipe_id,
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

async function createMembroEquipe(data, onSuccess=null, onError=null) {
    console.log("dentro de create atividade",data)
    return await $.ajax({
        url: "/create-membro-equipe",
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

async function removeMembroEquipe(membro_equipe_id, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/remove-membro-equipe/"+membro_equipe_id,
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