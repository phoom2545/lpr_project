import "./App.css";
import React from "react";
import Home from "./components/Home";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"; // npm install react-router-dom
import Img_detection from "./components/Img_detection";
import Video_detection from "./components/Video_detection";
import Video_show from "./components/Video_show";


function App() {
  return (
      <Router>
        <Routes>
          <Route path="/" element={<Home/>}></Route>
          <Route path="/img_detection" element={<Img_detection/>}></Route>
          <Route path="/video_detection" element={<Video_detection/>}></Route>
          <Route path="/video_show" element={<Video_show/>}></Route>
        </Routes>
      </Router>
  );
}

export default App;
