
import React from 'react';
import logo from "../images/web_icon.png";
import axios from 'axios';




const Navbar = () => {
  return (
    <nav style={styles.navbar}>
      <button style={styles.button}>Upload Image</button>
      <img src={logo} style={styles.logo} alt="logo" />
      <button style={styles.button}>About</button>
    </nav>
  );
};

const styles = {
    navbar: {
        justifyContent: 'space-evenly',
        alignItems: 'center',
        display: 'flex',
        backgroundColor: 'rgba(68, 144, 219, 1)',
        // borderRadius: '0px 0px 20px 20px',
        borderBottom: '5px solid rgba(255, 255, 255, 0.8)',
        height: '75px',
        width: '100%', 
        position: 'sticky', 
        // marginBottom: '100px',
        top: 0,
        right: 0,
    },
    logo: {
        position: 'absolute',
        top: '0%',
        height: '150px',
        
    
    },
    button: {
        backgroundColor: 'rgba(160, 198, 235, 1)',
        borderRadius: '10px',
        height: '50px',
        width: '200px',
        fontWeight: 'bold',
        fontSize: "calc(10px + 1vmin)",
        // webkitTextStrokeWidth: '2px',
        // webkitTextStrokeColor: ',
        color: 'rgba(236, 120, 0, 1)',

    }
};

export default Navbar;