async function getCidadeSelect(data, callback=null) {
    toggleLoading("select cidade")
    return await $.ajax({
        url: "/cidadesSelect",
        data: data,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        success: function (data) {
            toggleLoading("after get select cidade")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("select cidade error")
            showFloatingMessage("Erro ao carregar cidade", "alert-danger");
        }
    });
}

async function cidadeForm(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: '/cidadeForm',
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

async function cidadeCreate(data, onSuccess, onError) {
    return await $.ajax({
        url: '/saveCidade',
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        data: JSON.stringify({"data":data}),
        success: function(response) {
            if (onSuccess) onSuccess(response);
        },
        error: function(response) {
            if (onError) onError(response);
            console.log(response);
        }
    });
};

async function getCidades(data, onSuccess, onError) {
    return await $.ajax({
        url: '/getCidades',
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