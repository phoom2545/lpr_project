import "./Home.css";
import React from "react";
import test_pic from "./test_pic2.jpg";

function Home() {
  return (
    <div className="HomePage">
      <div className="title">Detection System</div>
      <div className="realtime-monitor">
        <img
          // src="http://127.0.0.1:5001/video_feed"
          src={test_pic}
          alt="Live Video Feed"
          width="45%"
        />
      </div>
      <div className="ResultContainer">
        <div className="Result-Detected">
          <div className="Result-Detected-Detail-Name">Detection No</div>
          <div className="Result-Detected-Detail-Value">ฒก8534</div>
        </div>
        <div className="Result-Detected">
          <div className="Result-Detected-Detail-Name">Detection Province</div>
          <div className="Result-Detected-Detail-Value">กรุงเทพมหานคร</div>
        </div>
      </div>
    </div>
  );
}

export default Home;
