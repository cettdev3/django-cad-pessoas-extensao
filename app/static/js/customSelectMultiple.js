/**
 * CustomSelectMultiple
 * 
 * A custom dropdown component that allows users to select multiple options from a list. 
 * It supports filtering of options, adding new options through a modal, and selecting/deselecting options.
 * 
 * @param {Object} modal - An instance of the modal component used to add new items.
 * @param {Object} options - Configuration options for the component.
 *   @param {Array} [options.selectedOptions] - An initial array of selected option IDs.
 *   @param {String} [options.label="Select"] - The label to display on the dropdown button.
 *   @param {Boolean} [options.multiple=true] - Whether multiple options can be selected.
 *   @param {Function} options.loadOptions - A function that returns a promise resolving to the list of options.
 * @param {Function} [onReady] - A callback function to execute once the component is initialized.
 * 
 * @property {Object} modal - Reference to the modal component.
 * @property {Object} state - The current state of the component.
 * @property {Object} config - Configuration options for the component.
 * 
 * @example
 * 
 * // HTML placeholder for the component
 * <div id="multiple-select-component"></div>
 * 
 * // Initialize the modal component
 * const customModal = new CustomModalComponent({
 *     // ... modal configuration options ...
 * });
 * 
 * // Initialize the select multiple component
 * const customSelect = new CustomSelectMultiple(customModal, {
 *     label: "Select Item",
 *     multiple: true,
 *     loadOptions: functionToLoadOptions
 * }, function() {
 *     $('#multiple-select-component').append(customSelect.element);
 * });
 * 
 * @method init - Initializes the component.
 * @method bindModalEvents - Binds events related to the modal.
 * @method bindUIEvents - Binds UI events like click and keyup.
 * @method openDropdown - Opens the dropdown menu.
 * @method closeDropdown - Closes the dropdown menu.
 * @method resetFilter - Resets the filter input value.
 * @method loadOptions - Loads options using the provided loadOptions function.
 * @method renderOptions - Renders the options in the dropdown.
 * @method updateLabel - Updates the dropdown button label.
 * @method handleNewItem - Handles adding a new item to the options.
 * @method handleOptionClick - Handles selecting/deselecting an option.
 * @method handleBadgeRemove - Handles removing a selected option badge.
 * @method handleFilter - Filters the options based on user input.
 * @method renderBadges - Renders the badges for selected options.
 * @method getValue - Gets the currently selected option(s).
 * @method setValue - Sets the selected option(s).
 */

class CustomSelectMultiple {
    constructor(modal, options, onReady) {
        this.modal = modal;
        this.state = {
            options: options.options || [],
            selectedOptions: options.selectedOptions || [],
            readOnly: options.readOnly || false,
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
        this.state.options = [];
        this.loadOptions();
        this.bindUIEvents();
        this.updateLabel();
    }

    bindModalEvents() {
        if (!this.modal) return;
        this.modal.element.on('action-success', (event) => this.handleNewItem(event.detail));
        this.modal.element.on('action-fail', (event) => {
            if (event.originalEvent && event.originalEvent.detail && event.originalEvent.detail.responseJSON && event.originalEvent.detail.responseJSON.message) {
                showFloatingMessage("Erro ao cadastrar item: "+ event.originalEvent.detail.responseJSON.message, "alert-danger")
            } else {
                showFloatingMessage("Erro ao cadastrar item", "alert-danger")
            }
        });
    }

    emitChangeEvent(from) {
        const event = new CustomEvent('change', { detail: this.state.selectedOptions });
        if (!this.element) return;
        this.element[0].dispatchEvent(event);
    }

    bindUIEvents() {
        if (!this.element) return;
        this.element.on('click', '.dropdown-item', this.handleOptionClick.bind(this));
        this.element.on('click', 'button.close', this.handleBadgeRemove.bind(this));
        this.element.on('keyup', '#filterInput', this.handleFilter.bind(this));
        if (this.modal) {
            this.element.find('#btn-open-modal').on('click', () => this.modal.open());
        } else {
            this.element.find('#btn-open-modal').hide();
        }
        this.element.find('#filterInput').on('focus', () => this.openDropdown());
        $("body").on('click', (event) => {
            if (!this.element.is(event.target) && this.element.has(event.target).length === 0) {
                this.closeDropdown();
            }
        })
    }

    openDropdown() {
        if (!this.element) return;
        this.element.find('#dropdownMenu').addClass('show');
    }
    
    closeDropdown() {
        if (!this.element) return;
        this.element.find('#dropdownMenu').removeClass('show');
        this.resetFilter();
    }

    resetFilter() {
        if (!this.element) return;
        this.element.find('#filterInput').val('');
        this.renderOptions();
    }

    loadOptions() {
        if (this.state.options.length > 0) {
            this.renderOptions();
            this.renderBadges();
            return;
        }

        this.state.isLoading = true;
        this.showSpinner();
    
        this.config.loadOptions({}).then(options => {            
            this.state.options = options;
            this.renderOptions();
            this.renderBadges();
            this.state.isLoading = false;
            this.hideSpinner();
        }).catch(error => {
            console.log('Failed to load options:', error);
            this.state.isLoading = false;
            this.hideSpinner();
        });
    }
    
    showSpinner() {
        if(!this.element) return;
        this.element.find("#loading-spinner").show();
    }
    
    hideSpinner() {
        if(!this.element) return;
        this.element.find("#loading-spinner").hide();
    }

    renderOptions(filteredOptions = null) {
        if (!this.element) return;
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
        if (!this.element) return;
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
        this.emitChangeEvent("handel new item");
    }

    handleOptionClick(event) {
        if (!this.element) return;
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
            if (checkbox.prop('checked')) {
                const index = this.state.selectedOptions.indexOf(optionId);
                if (index > -1) this.state.selectedOptions.splice(index, 1);
            } else {
                this.state.selectedOptions = [optionId] 
                this.element.find('.dropdown-item input:checked').not(checkbox).prop('checked', false);
            }
        }

        checkbox.prop('checked', !checkbox.prop('checked')); 
        this.renderBadges();
        this.openDropdown();
        this.emitChangeEvent("handle option click");
    }

    handleBadgeRemove(event) {
        if (!this.element) return;
        const badge = $(event.target).closest('.item-badge');
        const optionId = badge.data('id');
        const index = this.state.selectedOptions.indexOf(optionId);
        if (index > -1) this.state.selectedOptions.splice(index, 1);

        this.element.find(`input[data-id="${optionId}"]`).prop('checked', false);

        this.renderOptions();
        badge.remove();
        this.emitChangeEvent("handle badge remove");
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
        if (!this.element) return;
        const badgesContainer = this.element.find('#badges-container');
        badgesContainer.empty();
        this.state.selectedOptions.forEach(id => {
            const option = this.state.options.find(o => {
                return o.id === id
            });
            if (!option) return;
            const badge = $(`
                <div class="badge-outline-secondary d-flex align-items-center mx-2 item-badge" data-id="${option.id}">
                    <span>${option.nome}</span>
                    <button type="button" 
                    data-toggle="tooltip"
                    data-placement="top"
                    title="Remover"
                    class="close ml-2">
                        <i class="fa fa-close"></i>
                    </button>
                </div>
            `);
            badgesContainer.append(badge);
        });
    }

    getValue() {
        return this.config.multiple ? this.state.selectedOptions : this.state.selectedOptions[0];
    }

    setValue(values, emmitChangeEvent = true) {
        this.state.selectedOptions = this.config.multiple ? values : [values];
        this.renderOptions();
        this.renderBadges();
        if (emmitChangeEvent) this.emitChangeEvent("set value");
    }
}