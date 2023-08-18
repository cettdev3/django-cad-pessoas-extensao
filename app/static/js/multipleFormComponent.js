class MultipleFormComponent {
    constructor(options) {
        this.fetchFormTemplateFunction = options.fetchFormTemplateFunction;
        this.fetchComponentTemplateFunction = options.fetchComponentTemplateFunction;
        this.onReady = options.onReady || null;
        this.createFunction = options.createFunction || null;
        this.updateFunction = options.updateFunction || null;
        this.deleteFunction = options.deleteFunction || null;
        this.initialFormCount = options.initialFormCount || 0;
        this.showDeleteButton = options.showDeleteButton !== undefined ? options.showDeleteButton : true;
        this.showSaveButton = options.showSaveButton !== undefined ? options.showSaveButton : true;
        this.showAddButton = options.showAddButton !== undefined ? options.showAddButton : true;

        this.init();
    }

    async init() {
        try {
            const template = await this.fetchComponentTemplateFunction();
            this.element = $(template);
            this.bindUIEvents();
            
            for(let i = 0; i < this.initialFormCount; i++) {
                await this.addForm();
            }
            
            // Callback execution after initialization
            if (this.onReady) {
                this.onReady();
            }
        } catch (error) {
            console.error("Failed to fetch the component template:", error);
        }
    }

    bindUIEvents() {
        const self = this;
        if (this.showAddButton) {
            this.element.find('.add-form-btn').on('click', function() {
                self.addForm();
                self.bindFormActions();
            });
        } else {
            this.element.find('.add-form-btn').hide();
        }
    }

    async addForm(modelIdOverride = null, formData = null) {
        try {
            let modelId = modelIdOverride;
            let saveButton = '';
    
            // If a creation function is provided and no modelIdOverride is given, create the model first.
            if (this.createFunction && !modelId) {
                let model = await this.createFunction();
                modelId = model.id;
                saveButton = this.showSaveButton ? '<button class="btn btn-primary save-form-btn" style="margin-top: 10px;">Save</button>' : '';
            }
    
            const formContent = await this.fetchFormTemplateFunction({ model_id: modelId });
            const wrappedFormContent = `
            <div class="individual-form" data-id="${modelId}" style="border: 1px solid #e0e0e0; padding: 10px;">
                ${formContent}
                <div class="form-actions d-flex justify-content-end">
                    ${saveButton}
                    ${this.showDeleteButton ? '<button class="btn btn-danger remove-form-btn" style="margin-top: 10px;">Remover</button>' : ''}
                </div>
            </div>`;
            this.element.find('.form-container').append(wrappedFormContent);
    
            if (formData) {
                const newForm = this.element.find('.individual-form').last();
                for (const key in formData) {
                    newForm.find(`[name=${key}]`).val(formData[key]);
                }
            }
    
            this.bindFormActions(); // This will bind both removal and save actions
        } catch (error) {
            showFloatingMessage("Erro ao adicionar formulário: " + error.responseJSON.message, "alert-danger");
        }
    }

    bindFormActions() {
        const self = this;

        // Removal
        this.element.find('.remove-form-btn').off('click').on('click', async function() {
            const formId = $(this).closest('.individual-form').data('id');
            if (self.deleteFunction) {
                try {
                    await self.deleteFunction(formId);
                } catch (error) {
                    console.error("Failed to delete the model:", error);
                    return;
                }
            }
            $(this).closest('.individual-form').remove();
        });

        // Save
        this.element.find('.save-form-btn').off('click').on('click', async function() {
            const formId = $(this).closest('.individual-form').data('id');
            const data = $(this).closest('.individual-form').find("[id^=form-container-]")[0].getValue();
            if (self.updateFunction) {
                try {
                    await self.updateFunction(formId, data);
                } catch (error) {
                    console.error("Failed to update the model:", error);
                }
            }
        });
    }

    getValues() {
        const values = [];
        this.element.find('.individual-form').each(function() {
            const formContainer = $(this).find("[id^=form-container-]");
            
            // Check if the form container has an embedded getValue function
            if (formContainer[0].getValue && typeof formContainer[0].getValue === 'function') {
                values.push(formContainer[0].getValue());
            } else {
                // Fall back to the old method if there's no getValue function
                const formDataArray = $(this).find('form').serializeArray();
                const formDataObject = {};
                formDataArray.forEach(field => {
                    formDataObject[field.name] = field.value;
                });
                values.push(formDataObject);
            }
        });
        return values;
    }    

    async setValue(data) {
        if (typeof data === 'number') {
            for (let i = 0; i < data; i++) {
                await this.addForm();
            }
        } else if (Array.isArray(data)) {
            for (let item of data) {
                if (item.id) {
                    await this.addForm(item.id, item);
                } else {
                    await this.addForm(null, item);
                }
            }
        }
    }
}
