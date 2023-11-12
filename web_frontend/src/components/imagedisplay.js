
import React from 'react';
import { useState, useRef, useEffect } from 'react';


const ImageDisplay = ({image, imageDimensions, apiData}) => {
    
    const [inicialized, setInicialized] = useState(true);
    const [canvasDim, setCanvasDim] = useState({width: 800, height: 800});
    const canvasRef = useRef(null);
    useEffect(() => {
    const ctx = canvasRef.current.getContext('2d'); 
    if (inicialized){
        let crop;
        ctx.strokeStyle = 'yellow'; 
        ctx.lineWidth = 4; 
        ctx.fillStyle = 'orange'; 
        ctx.font = 'bold 20px Arial'; 

        var canvas = ctx.canvas ;
        var hRatio = canvas.width  / imageDimensions.width    ;
        var vRatio =  canvas.height / imageDimensions.height  ;
        var ratio  = Math.min ( hRatio, vRatio );
        var centerShift_x = ( canvas.width - imageDimensions.width*ratio ) / 2;
        var centerShift_y = ( canvas.height - imageDimensions.height*ratio ) / 2;  
        ctx.clearRect(0,0,canvas.width, canvas.height);
        const img = new Image();
        img.src = URL.createObjectURL(image);
        img.onload = function() {
            ctx.drawImage(img, 0,0, imageDimensions.width, imageDimensions.height,
                                centerShift_x,centerShift_y,imageDimensions.width*ratio, imageDimensions.height*ratio); 
            
            //Drawing the bounding boxes on the image
            for (var i = 0; i < apiData.length; i++){
                console.log(apiData.length);
                crop = {x: (apiData[i].bounding_box[0]), 
                        y: (apiData[i].bounding_box[1]), 
                        width: ((apiData[i].bounding_box[2] - apiData[i].bounding_box[0])), 
                        height: ((apiData[i].bounding_box[3] - apiData[i].bounding_box[1])),
                        class: apiData[i].class,
                        value: apiData[i].value}
                console.log(crop);
                ctx.strokeRect(crop.x, crop.y, crop.width, crop.height);
                
                // const label = crop.class; 
                // const labelX =  crop.x + crop.width - ctx.measureText(label).width;
                // const labelY = crop.y + crop.height + 20;
                // ctx.strokeText(label, labelX, labelY);
                // ctx.fillText(label, labelX, labelY);
                const prediction = crop.value;
                const predictionX = crop.x + crop.width - ctx.measureText(prediction).width;  
                const predictionY =  crop.y - 10; 
                ctx.strokeText(prediction, predictionX, predictionY);
                ctx.fillText(prediction, predictionX, predictionY);
            }
        }

        setInicialized(false);
    }
    }, []);
    return (

        <>
            {image && (
                <canvas className="canv" ref={canvasRef} width={imageDimensions.width} height={imageDimensions.height}></canvas>
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
        alignapiDatas: "center",
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
        alignapiDatas: "center",
        justifyContent: "space-evenly",
    },

};

export default ImageDisplay;
