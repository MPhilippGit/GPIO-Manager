const PATHS = {
  TEMP: "api/temps",
  HUMID: "api/humids",
  VOC: "api/vocs",
  DASHBOARD: "dashboard",
  RECORDINGS: "recordings",
  PREDICT: (voc) => {
    return "predict/" + voc;
  },
};

export { PATHS };
