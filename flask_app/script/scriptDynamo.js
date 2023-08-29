async function caricamentoDynamo(){
    //const button = document.getElementById('myButton');

    //button.addEventListener('click', () => {
    //document.addEventListener('DOMContentLoaded',function(){
    // Esegui lo script al click del bottone

    // carico menu a tendina 3
    const outputElement3 = document.getElementById('menu3');

    const response3 = await fetch(`http://localhost:8080/connDynamo`, { method: 'GET', headers: { 'Accept': 'application/json',},
    }).then(response3 => {
      const dynamoJson = response3.json()
      dynamoJson.then(risultato =>{
        console.log(risultato['Items'])
        risultato = risultato['Items']
        for (i in risultato){
          //console.log(risultato[i])
          var paragraph = document.createElement("option");
          paragraph.textContent= risultato[i]['name']
          outputElement3.appendChild(paragraph)
          //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })    
}

window.onload = caricamentoDynamo();