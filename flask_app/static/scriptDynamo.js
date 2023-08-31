const menuDynamo = document.getElementById('menuDynamo');

function selezioneCompagnia(){

  menuDynamo.addEventListener("change", function() {
    // prendo valore assegnato all'opzione
    console.log(menuDynamo[menuDynamo.selectedIndex].value)
    compagnia=menuDynamo[menuDynamo.selectedIndex].value
    // invoco metodo del backend
    const response = fetch(`http://localhost:8080/selectdynamo/`+compagnia, { method: 'GET', headers: { 'Accept': 'application/json',},
      }).then(response => {
        dynamoJson= response.json()
        dynamoJson.then(risultato =>{
          console.log(risultato)
        })
        })
  });
}

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
          paragraph.value = risultato[i]['compagnia_id']
          menuDynamo.appendChild(paragraph)
          //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })    
}

selezioneCompagnia();
window.onload = caricamentoDynamo();