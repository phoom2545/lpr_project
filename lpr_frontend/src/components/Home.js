import "./detection.css";
import React, { useState, useEffect } from "react";

function Home() {

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

    // Create a function to fetch the license data
    const fetchLicenseData = async () =>{
      try{
        const response = await fetch(data_URL);
        const data = await response.json();
        console.log(data)
        setLicenseData(data);
      
      }catch(error){
        console.error("Error fetching license data: ", error);
      }
    };
    
    // Initial the function
    fetchLicenseData();

    // Set up the polling to fetch every 2 seconds (2000 millisecs)
    const interval = setInterval(fetchLicenseData,2000);

    // Clean up the interval on component unmount
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="HomePage">
      <div className="title">Home Page</div>
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

export default Home;
