const PATHS = {
    TEMP: "api/temps",
    HUMID: "api/humids",
    VOC: "api/vocs",
    DASHBOARD: "dashboard",
    PREDICT: (voc) => {
        return "predict/"+voc;
    }
};

export { PATHS }