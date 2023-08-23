async function updateItemOrcamento(item_orcamento_id, data, onSuccess=null, onError=null) {
    console.log("dentro de update Item de orcamento",data)
    return await $.ajax({
        url: "/update-item-orcamento/"+item_orcamento_id,
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

async function createItemOrcamento(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/create-item-orcamento",
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

async function removeItemOrcamento(item_orcamento_id, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/remove-item-orcamento/"+item_orcamento_id,
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

async function getItemOrcamentoForm(data, onSuccess=null, onError=null) {
    return await $.ajax({
        url: "/item-orcamento-form",
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

function initializeItemOrcamentoForm(itemOrcamentoId, container = null) {
    params = { itemOrcamentoId: itemOrcamentoId };
    console.log("params dentro do formulario de item de orcamento: ", params)
    let formContainer = container ? container : $("#form-container-" + params.itemOrcamentoId);
    console.log("formcontainer dentro de initialize form: ", formContainer)
    function handleSemCustoCheckbox() {
        var isChecked = $("#em_estoque_" + params.itemOrcamentoId).is(':checked');
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

    $("#em_estoque_" + params.itemOrcamentoId).on('change', function () {
        handleSemCustoCheckbox();
        handleUpdateItemOrcamento(params.itemOrcamentoId, {
            valor: $(formContainer).find("input[name='valor']").val(),
            valor_total: $(formContainer).find("input[name='valor_total']").val(),
            em_estoque: $(this).is(':checked')
        });
    });

    function handleUpdateItemOrcamento(id, data) {
        updateItemOrcamento(id,
            data,
            function (response) {
                showFloatingMessage("Item de orcamento atualizado com sucesso!", "alert-success")
            }, function (error) {
                showFloatingMessage("Erro ao atualizar item de orcamento!", "alert-danger")
                $(this).val(current_value);
            });
    }

    $(formContainer)[0].getValue = function () {
        var itemOrcamento = {}
        $(formContainer).find("input, textarea").each(function () {
            var name = $(this).attr('name');
            itemOrcamento[name] = $(this).val();
        });

        return itemOrcamento;
    }

    $(formContainer).find("input , textarea").each(function () {
        let includedField = ['descricao', 'unidade'];
        if (!includedField.includes($(this).attr('name'))) return;
        $(this).on('change', function () {
            var name = $(this).attr('name');
            var value = $(this).val();
            let data = {}
            let current_value = $(this).data('current-value');
            data[name] = value;

            if (current_value == value || !params.itemOrcamentoId) return;
            console.log("dentro do change do input: ", data)
            handleUpdateItemOrcamento(params.itemOrcamentoId, data);
        });
    });

    $(formContainer).find("input[name='quantidade'], input[name='valor']").each(function () {
        $(this).on('change', function () {
            var quantidade = $(formContainer).find("input[name='quantidade']").val();
            var valor = $(formContainer).find("input[name='valor']").val();
            if (!quantidade && !valor) return;
            var valor_total = quantidade * valor;
            $(formContainer).find("input[name='valor_total']").val(valor_total);
            handleUpdateItemOrcamento(params.itemOrcamentoId, { 
                quantidade: quantidade,
                valor: valor,
                valor_total: valor_total 
            });
        });
    });
} 