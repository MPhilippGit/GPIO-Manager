import { X } from "lucide-react";

class PredictionHelper {
    constructor(slope, intercept) {
        this.slope = slope;
        this.intercept = intercept;
    }

    predict(x) {
        return Math.round(this.slope*x + this.intercept);
    }

    getXYValues(data) {
        console.log(data, "this should be only voc values")
        return data.map(x => [x, this.predict(x)])
    }
}

export { PredictionHelper };