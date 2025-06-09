import "./detection.css";
import React, { useState, useEffect } from "react";

function Img_detection() {

  const BASE_URL = "http://127.0.0.1:5001";
  const image_URL = BASE_URL + "/get_image";
  const data_URL = BASE_URL + "/get_license_data";

  // Initialize the state and set it as object in default with key and value : "".
  const [licenseData, setLicenseData] = useState(
    {
      license_no: "",
      province_name: ""
    }
  )

  useEffect(() =>{

    // Create a function to fetch the license data (async is required when using 'await' because JS wants to know ahead of time that it will have pause and wait for things)
    const fetchLicenseData = async () =>{
      try{
        const response = await fetch(data_URL);   // await means wait for this process to finish!! (need to put async on top of the funtion using await too)
        const data = await response.json();       
        console.log(data)                         // This will print but only after the fetch is finished
        setLicenseData(data);
      
      }catch(error){
        console.error("Error fetching license data: ", error);
      }
    };
    
    // Runn immediately when component loads (to run the fetch function without having to wait 2 seconds initially)
    fetchLicenseData();

    // Set up the polling to fetch every 2 seconds (2000 millisecs)
    const interval = setInterval(fetchLicenseData,2000);

    // Clean up the interval on component unmount.
    // return () will runs when the component is about to be removed(exit the page) or 
    return () => clearInterval(interval);
  }, [data_URL]);

  return (
    <div className="HomePage">
      <div className="title">Image Detection System</div>
      <div className="realtime-monitor">
        <img
          src= {image_URL}
          // src="http://127.0.0.1:5001/get_video_stream"
          alt="Live Feed"
          width="25%"
        />
      </div>
      <div className="ResultContainer">
        <div className="Result-Detected">
          <div className="Result-Detected-Detail-Name">License Number</div>
          <div className="Result-Detected-Detail-Value">{licenseData.license_no}</div>
        </div>
        <div className="Result-Detected">
          <div className="Result-Detected-Detail-Name">Province</div>
          <div className="Result-Detected-Detail-Value">{licenseData.province_name}</div>
        </div>
      </div>
    </div>
  );
}

export default Img_detection;
