async function createAnexo(data, callback=null) {
    toggleLoading("createAnexoSection")
    console.log(data)
    return await $.ajax({
        url: "/saveAnexo",
        data: JSON.stringify(data),
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        method: "POST",
        success: function (data) {
            toggleLoading("after create anexo")
            showFloatingMessage("Anexo adicionado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("createAnexoSection error")
            showFloatingMessage("Erro ao adicionar anexo", "alert-danger");
        }
    });
}

function deleteAnexo(anexo_id, callback = null) {
    toggleLoading("deleteAanexo")
    return $.ajax({
        url: "/deleteAnexo/"+anexo_id,
        headers: { "X-CSRFToken":  XCSRFToken },
        contentType: 'application/json',
        dataType: 'json',
        method: "POST",
        success: function (data) {
            toggleLoading("deleteAanexo after")
            showFloatingMessage("Aanexo deletado com sucesso", "alert-success");
            if (callback) callback(data);
        },
        error: function (data) {
            toggleLoading("deleteAanexo error")
            showFloatingMessage("Erro ao deletar Anexo", "alert-danger");
        }
    });
}
