class CustomSelectMultiple {
    constructor(modal, options, onReady) {
        this.modal = modal;
        this.state = {
            options: [],
            selectedOptions: options.selectedOptions || [],
            isLoading: false
        };
        this.config = {
            label: "Select",
            multiple: true,
            ...options
        };

        getSelectMultipleComponent({}, (htmlContent) => {
            this.element = $(htmlContent);
            this.bindModalEvents();
            this.init();
            
            if (onReady) {
                onReady();
            }
        }, (error) => {
            console.error("Failed to load the select multiple component:", error);
        });
    }

    init() {
        this.loadOptions();
        this.bindUIEvents();
        this.updateLabel();
    }

    bindModalEvents() {
        this.modal.element.on('action-success', (event) => this.handleNewItem(event.detail));
        this.modal.element.on('action-fail', (event) => showFloatingMessage("Erro ao cadastrar item", "alert-danger"));
    }

    bindUIEvents() {
        this.element.on('click', '.dropdown-item', this.handleOptionClick.bind(this));
        this.element.on('click', 'button.close', this.handleBadgeRemove.bind(this));
        this.element.on('keyup', '#filterInput', this.handleFilter.bind(this));
        this.element.find('#btn-open-modal').on('click', () => this.modal.open());
        this.element.on('hide.bs.dropdown', this.resetFilter.bind(this));
        this.element.find('#filterInput').on('focus', () => this.openDropdown());
        $("body").on('click', (event) => {
            if (!this.element.is(event.target) && this.element.has(event.target).length === 0) {
                this.closeDropdown();
            }
        })
    }

    openDropdown() {
        this.element.find('#dropdownMenu').addClass('show');
    }
    
    closeDropdown() {
        this.element.find('#dropdownMenu').removeClass('show');
    }

    resetFilter() {
        this.element.find('#filterInput').val('');
        this.renderOptions(); // Reset the display of options without filtering
    }

    loadOptions() {
        this.state.isLoading = true;
        this.config.loadOptions({}).then(options => {
            this.state.options = options;
            this.renderOptions();
            this.state.isLoading = false;
        }).catch(error => {
            console.log('Failed to load options:', error);
            this.state.isLoading = false;
        });
    }

    renderOptions(filteredOptions = null) {
        const optionsToRender = filteredOptions || this.state.options;
        const optionsContainer = this.element.find('#options-container');
        optionsContainer.empty();

        optionsToRender.forEach(option => {
            let isChecked = this.state.selectedOptions.includes(option.id) ? 'checked' : '';
            const optionElement = $(`
                <a class="dropdown-item" href="#">
                    <input type="checkbox" data-id="${option.id}" ${isChecked}> ${option.nome}
                </a>
            `);
            optionsContainer.append(optionElement);
        });
    }

    updateLabel() {
        this.element.find('#dropdownMenuButton').text(this.config.label);
    }

    handleNewItem(item) {
        this.state.options.push(item);
        if (!this.config.multiple) {
            this.state.selectedOptions = [];
        }
        this.state.selectedOptions.push(item.id);
        this.renderOptions();
        this.renderBadges();
    }

    handleOptionClick(event) {
        event.preventDefault();
        event.stopPropagation(); 
        const checkbox = $(event.target).is('input[type="checkbox"]') ? $(event.target) : $(event.target).find('input[type="checkbox"]');
        const optionId = checkbox.data('id');

        if (this.config.multiple) {
            if (checkbox.prop('checked')) {
                const index = this.state.selectedOptions.indexOf(optionId);
                if (index > -1) this.state.selectedOptions.splice(index, 1);
            } else {
                this.state.selectedOptions.push(optionId);
            }
        } else {
            this.state.selectedOptions = [optionId];
            this.element.find('.dropdown-item input:checked').not(checkbox).prop('checked', false);
        }

        checkbox.prop('checked', !checkbox.prop('checked')); 
        this.renderBadges();
        this.openDropdown();
    }

    handleBadgeRemove(event) {
        const badge = $(event.target).closest('.badge');
        const optionId = badge.data('id');
        const index = this.state.selectedOptions.indexOf(optionId);
        if (index > -1) this.state.selectedOptions.splice(index, 1);

        this.element.find(`input[data-id="${optionId}"]`).prop('checked', false);

        this.renderOptions();
        badge.remove();
    }

    handleFilter(event) {
        const query = $(event.target).val().toLowerCase();
        const filteredOptions = this.state.options.filter(option => {
            if (option && option.nome) {
                return option.nome.toLowerCase().includes(query);
            }
            return false;
        });
        this.renderOptions(filteredOptions);
    }    

    renderBadges() {
        const badgesContainer = this.element.find('#badges-container');
        badgesContainer.empty();

        this.state.selectedOptions.forEach(id => {
            const option = this.state.options.find(o => o.id === id);
            const badge = $(`
            <span class="badge badge-primary mr-1" data-id="${option.id}">
                ${option.nome}
                <button type="button" class="close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </span>
        `);

            badgesContainer.append(badge);
        });
    }

    getValue() {
        return this.config.multiple ? this.state.selectedOptions : this.state.selectedOptions[0];
    }

    setValue(values) {
        this.state.selectedOptions = this.config.multiple ? values : [values];
        this.renderOptions();
        this.renderBadges();
    }
}