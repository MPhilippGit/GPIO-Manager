import { X } from "lucide-react";

class PredictionHelper {
    constructor(slope, intercept) {
        this.slope = slope;
        this.intercept = intercept;
    }

    predict(x) {
        return this.slope*x + intercept;
    }

    getYValues(data) {
        return data.map(x => this.predict(x))
    }
}

export { PredictionHelper };