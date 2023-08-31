const menuPostgres = document.getElementById('menuPostgres');

function selezione(){

  menuPostgres.addEventListener("change", function() {
    
  });
}

async function caricamentoPostgres(){
    //const button = document.getElementById('myButton');

    //button.addEventListener('click', () => {
    //document.addEventListener('DOMContentLoaded',function(){
    // Esegui lo script al click del bottone

    // faccio una richiesta
    const response = await fetch(`http://localhost:8080/connPostgres`, { method: 'GET', headers: { 'Accept': 'application/json',},
      }).then(response => {
        // la risposta la passo in json
        const postgresJson = response.json()
        // accedo al contenuto del body
        postgresJson.then(risultato => {
          console.log(risultato)
          // scorro e carico il menu
          for (const i in risultato){
            var paragraph = document.createElement("option");
            paragraph.textContent= risultato[i][9]
            paragraph.value = risultato[i][9]
            menuPostgres.appendChild(paragraph)
            //menuPostgres.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })
}

window.onload = selezione();
window.onload = caricamentoPostgres();