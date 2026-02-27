import { X } from "lucide-react";

class PredictionHelper {
    constructor(slope, intercept) {
        this.slope = slope;
        this.intercept = intercept;
    }

    predict(x) {
        return this.slope*x + this.intercept;
    }
    /**
     * 
     * @param data array of person count from the regression data
     * @returns an array of corresponding xy-pairs to visualize the regression line  
     */
    getXYValues(data) {
        return data.map(x => [parseFloat(x), this.predict(x)])
    }
}

export { PredictionHelper };