const menuCassandra = document.getElementById('menuCassandra');

function selezione(){
    
}

async function caricamentoCassandra(){
    //const button = document.getElementById('myButton');

    //button.addEventListener('click', () => {
    //document.addEventListener('DOMContentLoaded',function(){
    // Esegui lo script al click del bottone

    // faccio una richiesta
    const response = await fetch(`http://localhost:8080/connCassandra`, { method: 'GET', headers: { 'Accept': 'application/json',},
      }).then(response => {
        // la risposta la passo in json
        const cassandraJson = response.json()
        // accedo al contenuto del body
        cassandraJson.then(risultato => {
          console.log(risultato)
          // scorro e carico il menu
          for (const i in risultato){
            var paragraph = document.createElement("option");
            paragraph.textContent= risultato[i][0]
            paragraph.value = risultato[i][0]
            menuCassandra.appendChild(paragraph)
            //menuPostgres.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })
}

window.onload = selezione();
window.onload = caricamentoCassandra();menuCassandra