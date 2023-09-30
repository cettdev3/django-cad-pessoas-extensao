async function getSelectMultipleComponent(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/select-multiple-component",
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

async function getMultipleFormComponent(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/multiple-form-component",
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

async function getStatusPropostaProjetoMenu(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/status-proposta-menu",
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

async function getPropostaProjetoComponent(id, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/proposta-projeto-view/"+id,
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

async function getMembroEquipeForm(data = {}, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/membro-equipe-form",
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

async function createPropostaProjeto(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/create-proposta-projeto",
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

async function updatePropostaProjeto(proposta_id, data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/update-proposta-projeto/"+proposta_id,
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

async function createProjetoFromProposta(proposta_id, data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/create-projeto-proposta/"+proposta_id,
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

async function removePropostaProjeto(proposta_projeto_id, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/remove-proposta-projeto/"+proposta_projeto_id,
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

async function getPropostaTable(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/proposta-projeto-table",
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "GET",
        data: data,
        success: function (data) {
            if (onSuccess) onSuccess(data);
        },
        error: function (data) {
            if (onError) onError(data);
        }
    });
}

async function cotecUpdateAtividade(atividade_id, data, onSuccess=null, onError=null) {
    console.log("dentro de update atividade",data)
    return await $.ajax({
        url: "/update-atividade/"+atividade_id,
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

async function createAtividadeCotec(data, onSuccess=null, onError=null) {
    console.log("dentro de create atividade",data)
    return await $.ajax({
        url: "/create-atividade",
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

async function removeAtividade(atividade_id, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/remove-atividade/"+atividade_id,
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