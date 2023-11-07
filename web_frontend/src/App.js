import { useState } from 'react';
import logo from './logo.svg';
import './App.css';
import Background from './components/background';
import Navbar from './components/navbar';
import ImageDisplay from './components/imagedisplay';
import MoneyTable from './components/moneytable';

import placeHolder from './images/placeholder2.png';

function App() {
  const [apiResponse, setApiResponse] = useState([1,1,1,1,1,1,0.25,0.10,0.10,0.05]);
  return (
    <div style={styles.app}>
      <Background/>
      <Navbar/>
      <div style={styles.content}>
        <ImageDisplay image = {placeHolder}/>
        <MoneyTable inference = {apiResponse}/>
      </div>
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
