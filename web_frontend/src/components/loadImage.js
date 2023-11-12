
import React from 'react';
import { useState } from 'react';


const LoadImage = ({uploadImage, setImage, setImageDimensions, apiResponse}) => {
    const [previewImage, setPreviewImage] = useState(null);

    //Nada otimizado, mas funciona por enquanto :D
    function HardSetImageDimensions(file){
    
        var img = new Image();
        img.src = URL.createObjectURL(file);
        img.onload = function() {
        setImageDimensions({width: img.width, height: img.height})
        console.log(img.width, img.height);
        }
    
        return null;
    }


    async function uploadImageWrapper(previewImage) {
        const result = await uploadImage(previewImage);
        console.log(result);
        if (result.status != 200) {
            setPreviewImage(null);
        }
    }
    return (
        <>
            {previewImage && !apiResponse && (
                <div style={styles.imagedisplay}>
                    <div style={styles.buttons}>
                        <button style={styles.Xbutton} onClick={() => {setPreviewImage(null)}}>X</button>
                        <button style={styles.Vbutton} onClick={() => {uploadImageWrapper(previewImage)}}>V</button>
                    </div>
                    <img
                        src={URL.createObjectURL(previewImage)}
                        alt="displayed image"
                        className="image"
                        style={styles.image}
                    />
                    
                </div>
                
            )}

            {!previewImage && !apiResponse && (
                <div style={styles.imagedisplay}>
                    

                    {/* <button style={styles.button}>uploadImage</button> */}
                    
                    <input
                        type="file"
                        name="myImage"
                        onChange={(event) => {
                        setImage(...Array.from(event.target.files));
                        HardSetImageDimensions(...Array.from(event.target.files))
                        setPreviewImage(...Array.from(event.target.files));
                        }}
                    />
                </div>
            )}
        </>
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
    },
    buttons: {
        backgroundColor: 'rgba(160, 198, 235, 0)',
        width: '15%',
        position: 'absolute',
        display: "flex",
        flexDirection: "row",
        alignItems: "center",
        justifyContent: "space-evenly",
    },
    Vbutton: {
        backgroundColor: 'rgba(160, 198, 235, 0)',
        boder: '3px solid white',
        borderRadius: '10px',
        height: '100px',
        width: '100px',
        fontWeight: 'bold',
        fontSize: "calc(10px + 3vmin)",
        color: 'rgba(0, 255, 0, 1)',
        cursor: 'pointer',

    },
    Xbutton: {
        backgroundColor: 'rgba(160, 198, 235, 0)',
        boder: '3px solid white',
        borderRadius: '10px',
        height: '100px',
        width: '100px',
        fontWeight: 'bold',
        fontSize: "calc(10px + 3vmin)",
        color: 'rgba(255, 0, 0, 1)',
        cursor: 'pointer',
    }
};

export default LoadImage;
