async function updateRecurso(recurso_id, data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/recurso-edit/"+recurso_id,
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

async function createRecurso(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/recurso-save",
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

async function removeRecurso(recurso_id, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/recurso-delete/"+recurso_id,
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

async function getRecursoForm(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/recurso-form",
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

async function getRecursoTable(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/recurso-tabela",
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

function initializeRecursoForm(recursoId, container = null) {
    params = { recursoId: recursoId };
    let formContainer = container ? container : $("#form-container-" + params.recursoId);
    function handleSemCustoCheckbox() {
        var isChecked = $(formContainer).find("input[id='em_estoque_" + params.recursoId + "']").is(':checked');
        if (isChecked) {
            $(formContainer).find("input[name='valor'], input[name='valor_total']").prop('readonly', true).val('0');
        } else {
            $(formContainer).find("input[name='valor']").prop('readonly', false);
        }
    }

    $(formContainer).find("#descricao").each(function () {
        let resizeTextarea = function (el) {
            $(el).css('height', 'auto');
            $(el).height(el.scrollHeight);
        };

        $(this).on('input', function () {
            resizeTextarea(this);
        });

        resizeTextarea(this);
    });

    handleSemCustoCheckbox();
    $(formContainer).find("input[id='em_estoque_" + params.recursoId + "']").on('change', function () {
        handleSemCustoCheckbox();
        handleUpdateRecurso(params.recursoId, {
            valor: $(formContainer).find("input[name='valor']").val(),
            valor_total: $(formContainer).find("input[name='valor_total']").val(),
            em_estoque: $(this).is(':checked')
        });
    });

    function handleUpdateRecurso(id, data) {
        if (!id) return;
        updateRecurso(id,
            data,
            function (response) {
                showFloatingMessage("Recurso atualizado com sucesso!", "alert-success")
            }, function (error) {
                showFloatingMessage("Erro ao atualizar item de orcamento!", "alert-danger")
                $(this).val(current_value);
            });
    }

    $(formContainer)[0].getValue = function () {
        var recurso = {}
        $(formContainer).find("input, textarea, checkbox").each(function () {
            var name = $(this).attr('name');
            console.log($(this).attr('type'), name, $(this).val(), $(this).is(':checked'))
            if ($(this).attr('type') == 'checkbox') recurso[name] = $(this).is(':checked')
            else recurso[name] = $(this).val();
        });

        return recurso;
    }

    $(formContainer).find("input , textarea").each(function () {
        let includedField = ['nome', 'descricao', 'unidade'];
        if (!includedField.includes($(this).attr('name'))) return;
        $(this).on('change', function () {
            var name = $(this).attr('name');
            var value = $(this).val();
            let data = {}
            let current_value = $(this).data('current-value');
            data[name] = value;

            if (current_value == value || !params.recursoId) return;
            console.log("dentro do change do input: ", data)
            handleUpdateRecurso(params.recursoId, data);
        });
    });

    $(formContainer).find("input[name='quantidade'], input[name='valor']").each(function () {
        $(this).on('change', function () {
            var quantidade = $(formContainer).find("input[name='quantidade']").val();
            var valor = $(formContainer).find("input[name='valor']").val();
            if (!quantidade && !valor) return;
            var valor_total = quantidade * valor;
            $(formContainer).find("input[name='valor_total']").val(valor_total);
            handleUpdateRecurso(params.recursoId, { 
                quantidade: quantidade,
                valor: valor,
                valor_total: valor_total 
            });
        });
    });
} 