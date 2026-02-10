class TimeFormatter {
    constructor(timestamp) {
        console.log(timestamp)
        this.timestamp = timestamp
        const [date, time] = this.timestamp.split("T");
        const [hours, minutes, seconds] = time.split(":");

        this.date = new Date(date);

        this.date.setHours(hours);
        this.date.setMinutes(minutes);
    }

    getGraphFormat() {
        return `${this.date.getHours()}:${this.date.getMinutes()}`;
    }
};

export { TimeFormatter };