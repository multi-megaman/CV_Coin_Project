
import React, { useState, useEffect } from 'react';

function Add(inference) {
    const sum = inference.reduce((acc, curr) => acc + curr, 0);
    return sum.toFixed(2);

}

//this function will get the numbers on the array and group them into a dictionary with the key being the number and the value being the number of times it appears
function getFrequency(inference) {
    var dict = {};
    for (var i = 0; i < inference.length; i++) {
        if (dict[inference[i]] === undefined) {
            dict[inference[i]] = 1;
        } else {
            dict[inference[i]] += 1;
        }
    }
    //transforming the dictionary into an array of objects
    var arr = [];
    for (var key in dict) {
        arr.push({ money: key, qnt: dict[key] });
    }

    return arr;
}

function MoneyTable({inference}) {
    const [data, setData] = useState([0]);
    const [sum, setSum] = useState(0);

    useEffect(() => {
        if (inference === null) return; 
        setData(getFrequency(inference));
        setSum(Add(inference));
    }, [inference]);

    return (
        <div style={styles.moneytable}>
            <div style={styles.tabletitle}>
                Total <br/>${sum}
            </div>
            <div style={styles.tableWrapper}>
                <table style={styles.table} >
                    <thead>
                        <tr>
                            <th>Value</th>
                            <th>Qnt</th>
                        </tr>
                    </thead>
                    <tbody>
                        {inference && (
                            data.map((number, index) => (
                                <tr key={index} style={index % 2 === 0 ? styles.even : styles.odd}>
                                    <td>{number.money}</td>
                                    <td>{number.qnt}</td>
                                </tr>
                            ))
                        )}

                        
                        {/* {inference.map((number, index) => (
                            <tr key={index} style={index % 2 === 0 ? styles.even : styles.odd}>
                                <td>{number}</td>
                            </tr>
                        ))} */}
                    </tbody>
                </table>
            </div>
        </div>

    );
}

const styles = {
    moneytable: {
        // backgroundColor: 'rgba(60, 255, 255, 0.8)',
        color: 'rgba(255,187,0,1)',
        fontWeight: 'bold',
        fontSize: "calc(10px + 4vmin)",
        webkitTextStrokeWidth: '2px',
        webkitTextStrokeColor: 'rgba(236, 120, 0, 1)',
        height: '80%',
        width: '20%', 
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "space-evenly",
        overflow: 'hidden',
    },
    tabletitle: {
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        border: '5px solid rgba(255, 255, 255, 1)',
        width: "75%",
        height: '20%',
        textAlign: 'center',
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
    },
    tableWrapper: {
        width: '100%',
        height: '60%',
        overflow: 'auto',    
    },
    table: {
        width: '100%',
        textAlign: 'center',
        // overflowX: 'scroll',
        border: '5px solid rgba(255, 255, 255, 1)',
        backgroundColor: 'rgba(0, 0, 0, 0.8)',
        borderRadius: '10px',
    },
    even: {
        backgroundColor: 'rgba(68, 144, 219, 1)',
        height: '5vh',
    },
    odd: {
        backgroundColor: 'rgba(160, 198, 235, 1)',
        height: '5vh',
    }
};

export default MoneyTable;
