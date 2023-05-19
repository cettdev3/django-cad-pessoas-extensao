async function createAtividade(data, callback=null) {
    toggleLoading("createAtividadeSection")
    console.log(data)
    return await $.ajax({
        url: "/saveAtividade",
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("after create atividade")
            showFloatingMessage("Atividade adicionada com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("createAtividadeSection error")
            showFloatingMessage("Erro ao cadastrar seção", "alert-danger");
        }
    });
}

async function updateAtividade(atividade_id, data, callback = null) {
    toggleLoading("updateAtividade")
    return await $.ajax({
        url: "/editarAtividade/"+atividade_id,
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("updateAtividade after")
            showFloatingMessage("Atividade atualizada com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("updateAtividade error")
            showFloatingMessage("Erro ao atualizar atividade", "alert-danger");
        }
    });
}

function deleteAtividade(atividade_id, callback = null) {
    toggleLoading("deleteAtividade")
    return $.ajax({
        url: "/deleteAtividade/"+atividade_id,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        dataType: 'json',
        method: "POST",
        success: function (data) {
            toggleLoading("deleteAtividade after")
            showFloatingMessage("Atividade deletada com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("deleteAtividade error")
            showFloatingMessage("Erro ao deletar atividade", "alert-danger");
        }
    });
}

function getAtividadeDrawer(atividade_id, callback = null) {
    toggleLoading("atividade drawer")
    return $.ajax({
        url: "/getAtividadeDrawer/"+atividade_id,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "GET",
        success: function (data) {
            toggleLoading("atividade drawer after")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("atividade drawer error")
            showFloatingMessage("Erro ao carregar atividade", "alert-danger");
        }
    });
}

// function atividadeSectionsTable(filters, callback=null) {
//     toggleLoading("atividadeSectionsTable")
//     return $.ajax({
//         url: "/atividadeSectionTable",
//         method: "GET",
//         data: filters,
//         success: function (data) {
//             toggleLoading("atividadeSectionsTable after")
//             if (callback) callback(data);
//         },
//         error: function (data) {
//             showFloatingMessage("Erro ao buscar seções", "alert-danger");
//         }
//     });
// }