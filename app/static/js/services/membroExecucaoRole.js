async function getMembroExecucaoRoles(data = {teste: "testes"}, onSuccess, onError) {
    return await $.ajax({
        url: '/getMembroExecucaoRoles',
        contentType: 'application/json',
        method: "GET",
        data: data,
        success: function(response) {
            if (onSuccess) onSuccess(response);
        },
        error: function(response) {
            if (onError) onError(response);
        }
    });
}


async function membroExecucaoRoleForm(data = {}, onSuccess=null, onError=null) {
    return await $.ajax({
        url: '/membro-execucao-role-form',
        contentType: 'application/json',
        method: "GET",
        data: data,
        success: function(response) {
            if (onSuccess) onSuccess(response);
        },
        error: function(response) {
            if (onError) onError(response);
        }
    });
}

async function membroExecucaoRoleCreate(data = {}, onSuccess, onError) {
    return await $.ajax({
        url: '/membro-execucao-role-create',
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        data: JSON.stringify(data),
        success: function(response) {
            if (onSuccess) onSuccess(response);
        },
        error: function(response) {
            if (onError) onError(response);
            console.log(response);
        }
    });
};
