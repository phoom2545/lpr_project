import "./detection.css";
import React, { useState, useEffect } from "react";

function Video_show() {

  const BASE_URL = "http://127.0.0.1:5001";
  const image_URL = BASE_URL + "/get_video_stream";


  return (
    <div className="HomePage">
      <div className="title">Video Show</div>
      <div className="realtime-monitor">
        <img
          src= {image_URL}
          // src="http://127.0.0.1:5001/get_video_stream"
          alt="Live Feed"
          width="50%"
        />
      </div>
      <div className="ResultContainer">
        <div className="Result-Detected">
          <div className="Result-Detected-Detail-Name">License Number</div>
          <div className="Result-Detected-Detail-Value">Testing Vid</div>
        </div>
        <div className="Result-Detected">
          <div className="Result-Detected-Detail-Name">Province</div>
          <div className="Result-Detected-Detail-Value">Testing Vid</div>
        </div>
      </div>
    </div>
  );
}

export default Video_show;
