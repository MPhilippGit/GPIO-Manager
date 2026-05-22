import { useState, useEffect } from "react";
import { TimeFormatter } from "../utils/Timeformatter";
import { VideoPlayer } from "./VideoPlayer";

function Recordings() {
  const [list, setList] = useState([]);
  let recordingIndex;

  console.log(list, "my fetched list");
  const fetchBulk = async (endpoint) => {
    try {
      const response = await fetch(endpoint);
      const result = await response.json();
      setList(result);
    } catch (error) {
      setList([]);
    }
  };

  useEffect(() => {
    fetchBulk("videos");
  }, []);

  if (list) {
    recordingIndex = list.map((entry, idx) => {
      const { filename, timestamp } = entry;
      return (
        <div className="dash-container_row">
          <div>{timestamp}</div>
          <VideoPlayer
            src={"/media/videos/" + filename}
            title={filename}
          />
        </div>
      );
    });
  }

  return <div className="dash-container dash-board">{recordingIndex}</div>;
}

export default Recordings;
