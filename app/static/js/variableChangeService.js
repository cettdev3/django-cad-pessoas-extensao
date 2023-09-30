class VariableChangeService {
    constructor() {
        // Ensure there's only one instance of VariableChangeService
        if (!VariableChangeService.instance) {
            this.subscribers = [];
            this.values = {};  // Store last known values for variables
            VariableChangeService.instance = this;
        }
        return VariableChangeService.instance;
    }

    // Method to add a new subscriber
    subscribe(callback) {
        this.subscribers.push(callback);
        // Immediately notify the subscriber with the last known values
        for (let variable in this.values) {
            callback({ variable: variable, value: this.values[variable] });
        }
    }

    // Method to remove a subscriber
    unsubscribe(callback) {
        this.subscribers = this.subscribers.filter(subscriber => subscriber !== callback);
    }

    // Method to notify all subscribers of a change
    notify(data) {
        // Store the latest value
        this.values[data.variable] = data.value;
        this.subscribers.forEach(subscriber => subscriber(data));
    }

    // Method to get the last known value of a variable
    getLastValue(variable) {
        return this.values[variable];
    }
}


const variableChangeInstance = new VariableChangeService(); // This instance will be shared
