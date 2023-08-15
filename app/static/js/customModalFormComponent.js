/**
 * CustomModalComponent Documentation
 * 
 * Overview:
 * CustomModalComponent is a flexible modal (dialog) implementation that allows dynamic content loading, 
 * custom actions, and event handling. It's built on top of jQuery and is designed for easy integration 
 * into web applications.
 * 
 * Initialization:
 * To create a new modal instance, use the CustomModalComponent constructor:
 * const myModal = new CustomModalComponent(options);
 * 
 * Options:
 * The CustomModalComponent accepts an options object with the following properties:
 * - `loadContent`: A function to fetch and load content into the modal.
 * - `modalTitle`: The title of the modal.
 * - `modalBtnActionText`: Text for the primary action button.
 * - `modalActionFunction`: Function to execute when the action button is clicked.
 * 
 * Example:
 * {
 *     loadContent: fetchDataFunction,
 *     modalTitle: "My Modal Title",
 *     modalBtnActionText: "Execute Action",
 *     modalActionFunction: executeActionFunction
 * }
 * 
 * Methods:
 * - open(size): Opens the modal. Accepts an optional size parameter ('sm', 'lg', 'xl'). Default size is medium.
 * - close(): Closes the modal.
 * - setContent(content): Sets the modal's content.
 * - setTitle(title): Sets the modal's title.
 * - setSize(size): Sets the modal's size.
 * 
 * Events:
 * - `itemCreated`: Dispatched when an item is successfully created via the modal.
 * 
 * Usage Examples:
 * 1. Initialization:
 *    Create a new modal with custom content loading and action functions:
 *    const myModal = new CustomModalComponent({
 *        loadContent: function(data, onSuccess, onError) {
 *            // Fetch data or generate content
 *            // Call onSuccess(content) with the fetched/generated content
 *        },
 *        modalTitle: "Sample Modal",
 *        modalBtnActionText: "Save Data",
 *        modalActionFunction: function(formData, onSuccess, onError) {
 *            // Handle form data, e.g., save to server
 *            // Call onSuccess(response) on success or onError(error) on failure
 *        }
 *    });
 * 
 * 2. Open Modal:
 *    To open the modal:
 *    myModal.open();
 * 
 *    To open the modal with a specific size:
 *    myModal.open('lg'); // Possible values: 'sm', 'lg', 'xl'
 * 
 * 3. Event Handling:
 *    Listen to events emitted by the modal:
 *    myModal.element.on('itemCreated', (event) => {
 *        console.log("Item was created!", event.detail);
 *    });
 * 
 * Note:
 * It's recommended to include more detailed explanations, examples, and potential caveats in a full 
 * documentation set, especially if this component will be used by other developers.
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
        this.element.on('shown.bs.modal', () => this.state.isOpen = true);
        this.element.on('hidden.bs.modal', () => this.state.isOpen = false);
    }

    handleActionClick() {
        const formData = this.getFormValues();
        this.options.modalActionFunction(formData)
            .then(response => {
                this.emitEvent('action-success', response);
                this.close();
            })
            .catch(error => {
                console.log("erro dentro da modal", error);
                this.emitEvent('action-fail', error);
            });
    }

    setActionButtonText(text) {
        this.element.find(".modal-action").html(text);
    }

    open(size) {
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
        const formDataArray = this.element.find('form').serializeArray();
        const formDataObject = {};

        formDataArray.forEach(field => {
            formDataObject[field.name] = field.value;
        });

        return formDataObject;
    }

    loadContent() {
        this.state.isLoading = true;
        this.options.loadContent({})
            .then(content => {
                this.setContent(content);
                this.element.modal('show');
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
