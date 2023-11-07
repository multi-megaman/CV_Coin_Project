import React from 'react';
import backgroundImage from '../images/web_background.jpg';


function Background() {
    return (
        <div style={styles.background}>
        </div>
    );
}


const styles = {
    background: {
        backgroundImage: `url(${backgroundImage})`,
        filter: 'blur(20px)',
        height: '102vh',
        width: '102vw',
        position: 'fixed',
        top: "-1%",
        left: "-1%",
        zIndex: -1,
        overflow: 'hidden',
        backgroundRepeat: 'repeat',
    },
};

export default Background;