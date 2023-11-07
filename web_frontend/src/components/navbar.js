
import React from 'react';
import logo from "../images/web_icon.png";


const Navbar = () => {
  return (
    <nav style={styles.navbar}>
      <img src={logo} style={styles.logo} alt="logo" />
    </nav>
  );
};

const styles = {
    navbar: {
        justifyContent: 'center',
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
        height: '140px',
        
    
    }
};

export default Navbar;