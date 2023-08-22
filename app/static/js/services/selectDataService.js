class SelectDataService {
    constructor() {
        if (SelectDataService.instance) {
            return SelectDataService.instance;
        }

        SelectDataService.instance = this;

        this.dataCache = {};
    }

    async fetchData(key, callback) {
        return new Promise((resolve, reject) => {
            if (this.dataCache[key]) {
                resolve(this.dataCache[key]);
            } else {
                callback().then(data => {
                    this.dataCache[key] = data;
                    resolve(data);
                }).catch(error => {
                    reject(error);
                })
            }
        });
    }
}
const selectDataService = new SelectDataService();