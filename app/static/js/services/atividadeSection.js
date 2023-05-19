async function createAtividadeSection(data, callback=null) {
    toggleLoading("createAtividadeSection")
    return await $.ajax({
        url: "/saveAtividadeSection",
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("after createAtividadeSection")
            showFloatingMessage("Seção adicionada com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("createAtividadeSection error")
            showFloatingMessage("Erro ao cadastrar seção", "alert-danger");
        }
    });
}

async function updateAtividadeSection(atividade_section_id, data, callback = null) {
    toggleLoading("updateAtividadeSection")
    return await $.ajax({
        url: "/updateAtividadeSection/"+atividade_section_id,
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        dataType: 'json',
        method: "POST",
        success: function (data) {
            toggleLoading("updateAtividadeSection after")
            showFloatingMessage("Seção atualizada com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("updateAtividadeSection error")
            showFloatingMessage("Erro ao atualizar seção", "alert-danger");
        }
    });
}

function deleteAtividadeSection(atividade_section_id, callback = null) {
    toggleLoading("deleteAtividadeSection")
    return $.ajax({
        url: "/deleteAtividadeSection/"+atividade_section_id,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        dataType: 'json',
        method: "POST",
        success: function (data) {
            toggleLoading("deleteAtividadeSection after")
            showFloatingMessage("Seção atualizada com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("deleteAtividadeSection error")
            showFloatingMessage("Erro ao atualizar seção", "alert-danger");
        }
    });
}

function atividadeSectionsTable(filters, callback=null) {
    toggleLoading("atividadeSectionsTable")
    return $.ajax({
        url: "/atividadeSectionTable",
        method: "GET",
        data: filters,
        success: function (data) {
            toggleLoading("atividadeSectionsTable after")
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("atividadeSectionsTable error")
            showFloatingMessage("Erro ao buscar seções", "alert-danger");
        }
    });
}