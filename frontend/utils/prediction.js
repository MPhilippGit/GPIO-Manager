import { X } from "lucide-react";

class PredictionHelper {
    constructor(slope, intercept) {
        this.slope = slope;
        this.intercept = intercept;
    }

    predict(x) {
        return this.slope*x + this.intercept;
    }

    getXYValues(data) {
        return data.map(x => [parseFloat(x), this.predict(x)])
    }
}

export { PredictionHelper };