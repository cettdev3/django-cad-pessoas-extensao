async function getPessoaSelect(data, callback=null) {
    toggleLoading("select pessoa")
    return await $.ajax({
        url: "/pessoasSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get   pessoa")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select pessoa error")
            showFloatingMessage("Erro ao carregar select de pessoas", "alert-danger");
        }
    });
}


async function pessoaForm(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: '/pessoa-modal',
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

async function pessoaCreate(data, onSuccess, onError) {
    return await $.ajax({
        url: '/pessoa-create',
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

async function getPessoas(data, onSuccess, onError) {
    return await $.ajax({
        url: '/getPessoas',
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