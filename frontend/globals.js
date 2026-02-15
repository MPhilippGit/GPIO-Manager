const PATHS = {
    TEMP: "api/temps",
    HUMID: "api/humids",
    VOC: "api/vocs",
    PREDICT: (voc) => {
        return "predict/"+voc;
    }
};

export { PATHS }