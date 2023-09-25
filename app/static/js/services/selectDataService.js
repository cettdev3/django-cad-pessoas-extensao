class SelectDataService {
    constructor() {
        if (SelectDataService.instance) {
            return SelectDataService.instance;
        }

        SelectDataService.instance = this;

        this.observers = {};

        this.dataCache = new Proxy({}, {
            set: (target, key, value) => {
                target[key] = value;  // Set the value as normal

                // If there's an observer for this key, call it
                if (this.observers[key]) {
                    this.observers[key].forEach(callback => callback(value));
                }

                return true;
            }
        });
    }

    addObserver(key, callback) {
        if (!this.observers[key]) {
            this.observers[key] = [];
        }
        this.observers[key].push(callback);
    }

    async fetchData(key, callback, forceRefresh = false) {
        return new Promise((resolve, reject) => {
            if (this.dataCache[key] && !forceRefresh) {
                resolve(this.dataCache[key]);
            } else {
                callback().then(data => {
                    this.dataCache[key] = data;  // This will trigger any observers if they exist
                    resolve(data);
                }).catch(error => {
                    reject(error);
                });
            }
        });
    }
}

const selectDataService = new SelectDataService();