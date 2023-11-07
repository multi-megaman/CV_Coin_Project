
import React from 'react';


const ImageDisplay = ({ image }) => {
    return (
        <div style={styles.imagedisplay}>
            <img
                src={image}
                alt="displayed image"
                className="image"
                style={styles.image}
            />
        </div>
    );
};


const styles = {
    imagedisplay: {
        width: '60%',
        height: '70%',
        // backgroundColor: 'rgba(0, 0, 0, 1)',
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-evenly",
    },
    image: {
        maxWidth: '100%',
        maxHeight: '100%',
        // border: '5px solid white',
        borderRadius: '25px',
    }
};

export default ImageDisplay;
