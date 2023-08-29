const menuMongo = document.getElementById('menuMongo');

async function caricamentoMongo(){
    //const button = document.getElementById('myButton');

    //button.addEventListener('click', () => {
    //document.addEventListener('DOMContentLoaded',function(){
    // Esegui lo script al click del bottone

    // carico menu a tendina 2
    // faccio richiesta http
    const response = await fetch(`http://localhost:8080/connMongo`, { method: 'GET', headers: { 'Accept': 'application/json',},
    }).then(response => {
      // risposta in json
      const mongoJson = response.json()
      mongoJson.then(risultato =>{
        console.log(risultato[0])
        risultato = risultato[0]
        // carico menu
        for (const i in risultato){
          //console.log(risultato[i])
          var paragraph = document.createElement("option");
          paragraph.textContent= risultato[i]['AIRPORT']
          menuMongo.appendChild(paragraph)
          //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })
}

window.onload = caricamentoMongo();