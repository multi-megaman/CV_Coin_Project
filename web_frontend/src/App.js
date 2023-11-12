import { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';
import Background from './components/background';
import Navbar from './components/navbar';
import LoadImage from './components/loadImage';
import ImageDisplay from './components/imagedisplay';
import MoneyTable from './components/moneytable';
import axios from 'axios';
import placeHolder from './images/placeholder2.png';
import FormData from 'form-data'

function extractValuesFromResponse(response) {
  let values = [];
  for (let i = 0; i < response.data.length; i++) {
    values.push(response.data[i].value);
  }
  return values;
}


function App() {
  const [apiResponse, setApiResponse] = useState(null);
  const [image, setImage] = useState(null);
  const [imageDimensions, setImageDimensions] = useState(null);
  const [coinsValue, setCoinsValue] = useState(null);
  


  async function uploadImage(image) {
    let data = new FormData();
    data.append('image', image)
    const result = await axios.post("http://localhost:8080/getCoins", data, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }).catch((error) => {return error.response});
    console.log(result.data.data);
    setApiResponse(result.data);
    setCoinsValue(extractValuesFromResponse(result.data));
    
    return result
  }

  return (
    <div style={styles.app}>
      <Background/>
      <Navbar/>
      {apiResponse && (
        <div style={styles.content}>
            <ImageDisplay image = {image} imageDimensions={imageDimensions} apiData={apiResponse.data}/>
            <MoneyTable inference = {coinsValue}/>
        </div>
      )}
      {!apiResponse && (
        <div style={styles.content}>
            <LoadImage uploadImage = {uploadImage} setImage={setImage} setImageDimensions={setImageDimensions} apiResponse={apiResponse}/>
        </div>
      )}
    </div>
  );
}

const styles = {
  app: {
    textAlign: "center",
    height: "100vh",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    fontSize: "calc(10px + 2vmin)",
    color: "white"
  },
  content: {
    textAlign: "center",
    height: "100%",
    width: "100%",
    display: "flex",
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "space-evenly",
    fontSize: "calc(10px + 2vmin)",
    color: "white",
    overflow: 'hidden',
  },

};

export default App;
