/**
 * CustomModalComponent
 * 
 * A custom modal (dialog) component designed for flexibility and ease of use. 
 * It supports dynamic content loading, custom actions, and event handling.
 * This modal is built on top of jQuery and is meant for seamless integration 
 * in web applications.
 * 
 * @param {Object} options - Configuration options for the modal.
 *   @param {Function} [options.loadContent] - A function that returns a promise resolving to the content of the modal.
 *   @param {String} [options.modalTitle="Default Title"] - The title of the modal.
 *   @param {String} [options.modalBtnActionText="Default Action"] - Text for the primary action button.
 *   @param {Function} options.modalActionFunction - A function to execute when the action button is clicked.
 * 
 * @property {Object} state - The current state of the modal.
 * @property {Object} element - The jQuery DOM element of the modal.
 * @property {Object} options - Configuration options for the modal.
 * 
 * @example
 * 
 * // Create a new modal instance with custom content and action functions
 * const customModal = new CustomModalComponent({
 *     loadContent: () => fetchContentFunction(),
 *     modalTitle: "Sample Modal",
 *     modalBtnActionText: "Execute",
 *     modalActionFunction: (formData) => handleFormDataFunction(formData)
 * });
 * 
 * // Open the modal with a specific size
 * customModal.open('lg'); // Values: 'sm', 'lg', 'xl'
 * 
 * // Listen to events emitted by the modal
 * customModal.element.on('action-success', (event) => {
 *     console.log("Action was successful!", event.detail);
 * });
 * 
 * @method init - Initializes the modal.
 * @method bindEvents - Binds the primary action button event.
 * @method bindModalEvents - Binds bootstrap modal events.
 * @method handleActionClick - Handles the click event for the primary action button.
 * @method setActionButtonText - Sets the text of the primary action button.
 * @method open - Opens the modal with an optional size parameter.
 * @method close - Closes the modal.
 * @method setContent - Sets the content of the modal.
 * @method setTitle - Sets the title of the modal.
 * @method setSize - Sets the size of the modal.
 * @method getFormValues - Retrieves form values from the modal's content.
 * @method loadContent - Loads content into the modal.
 * @method emitEvent - Emits a custom event from the modal.
 */
class CustomModalComponent {
    constructor(options) {
        this.state = {
            isOpen: false,
            isLoading: false
        };
        this.element = $("#custom-modal-template").clone().removeAttr('id');
        this.options = {
            modalTitle: "Default Title",
            modalBtnActionText: "Default Action",
            loadContent: () => Promise.resolve(),
            modalActionFunction: () => Promise.resolve(),
            ...options
        };
        this.init();
    }

    init() {
        this.bindEvents();
        this.setTitle(this.options.modalTitle);
        this.setActionButtonText(this.options.modalBtnActionText);
        this.bindModalEvents();
    }

    bindEvents() {
        this.element.find(".modal-action").on("click", this.handleActionClick.bind(this));
    }

    bindModalEvents() {
        setTimeout(() => {
            this.element.on('shown.bs.modal', () => this.state.isOpen = true);
            this.element.on('hidden.bs.modal', () => this.state.isOpen = false);
        }, 1000)
    }

    handleActionClick() {
        const formData = this.getFormValues();
        this.options.modalActionFunction(formData)
            .then(response => {
                this.emitEvent('action-success', response);
                this.close();
            })
            .catch(error => {
                this.emitEvent('action-fail', error);
            });
    }

    setActionButtonText(text) {
        this.element.find(".modal-action").html(text);
    }

    open(size = 'lg') {
        this.setSize(size); 
        this.loadContent();
    }

    close() {
        this.element.modal('hide');
    }

    setContent(content) {
        this.element.find(".modal-body").html(content);
    }

    setTitle(title) {
        this.element.find(".modal-title").html(title);
    }

    setSize(size) {
        const dialog = this.element.find('.modal-dialog');
        dialog.removeClass('modal-sm modal-lg modal-xl');
        if(['sm', 'lg', 'xl'].includes(size)) {
            dialog.addClass(`modal-${size}`);
        }
    }

    getFormValues() {
        const formDataObject = {};
        this.element.find('input, textarea, select, checkbox').each(function() {
            let name = $(this).attr('name'); 
            if ($(this).attr('type') == 'checkbox') formDataObject[name] = $(this).is(':checked')
            else formDataObject[name] = $(this).val();
        });

        return formDataObject;
    }

    loadContent() {
        this.state.isLoading = true;
        this.options.loadContent({})
            .then(content => {
                this.element.modal('show');
                this.setContent(content);
                this.options.initializeForm(this.element.find('form'))
            })
            .catch(error => {
                this.emitEvent('load-fail', error);
            })
            .finally(() => {
                this.state.isLoading = false;
            });
    }

    emitEvent(eventName, detail) {
        let event = new CustomEvent(eventName, { detail });
        this.element[0].dispatchEvent(event);
    }
}
