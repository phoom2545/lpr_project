import "./Home.css";
import React from "react";

function Home() {


  return (
    <div className="HomePage">
      <div className="title">Detection System</div>
      <div className="realtime-monitor">
        <img
          // src="http://127.0.0.1:5001/get_image"
          src="http://127.0.0.1:5001/get_video_stream"
          // src={test_pic}
          alt="Live Video Feed"
          width="45%"
        />
      </div>
      <div className="ResultContainer">
        <div className="Result-Detected">
          <div className="Result-Detected-Detail-Name">License Number</div>
          <div className="Result-Detected-Detail-Value">ฒก8534</div>
        </div>
        <div className="Result-Detected">
          <div className="Result-Detected-Detail-Name">Province</div>
          <div className="Result-Detected-Detail-Value">กรุงเทพมหานคร</div>
        </div>
      </div>
    </div>
  );
}

export default Home;
