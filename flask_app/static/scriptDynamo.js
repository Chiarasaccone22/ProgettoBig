const menuDynamo = document.getElementById('menuDynamo');

async function caricamentoDynamo(){
    //const button = document.getElementById('myButton');

    //button.addEventListener('click', () => {
    //document.addEventListener('DOMContentLoaded',function(){
    // Esegui lo script al click del bottone

    // carico menu a tendina 3
    // faccio richiesta http
    const response = await fetch(`http://localhost:8080/connDynamo`, { method: 'GET', headers: { 'Accept': 'application/json',},
    }).then(response => {
      // traspormo risposta in json
      const dynamoJson = response.json()
      dynamoJson.then(risultato =>{
        console.log(risultato['Items'])
        risultato = risultato['Items']
        // carico menu
        for (const i in risultato){
          //console.log(risultato[i])
          var paragraph = document.createElement("option");
          paragraph.textContent= risultato[i]['name']
          menuDynamo.appendChild(paragraph)
          //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })    
}

window.onload = caricamentoDynamo();