/* import { menuDynamo } from './scriptDynamo.js';
import { menuCassandra } from './scriptCassandra.js';
import { menuMongo } from './scriptMongo.js'; */



//const menuPostgres = document.getElementById('menuPostgres');
// const output = document.getElementById('output')

function selezionePartenza(){

  menuPostgres.addEventListener("change", function() {
    // prendo valore assegnato all'opzione
    const partenzaPrevista=menuPostgres[menuPostgres.selectedIndex].value
    console.log(partenzaPrevista)
    // invoco metodo del backend
    const response = fetch(`http://localhost:8080/selectpostgrescascata/`+partenzaPrevista, { method: 'GET', headers: { 'Accept': 'application/json',},
      }).then(response => {
        var postgresJson= response.json()
        postgresJson.then(risultato =>{

          console.log(risultato['resultCassandra'])
          // carico menu di cassandra 
          for (var valCassandra in risultato['resultCassandra']){
            var paragraph = document.createElement("option");
            console.log(valCassandra)
            /* paragraph.textContent= risultato[i][0]
            paragraph.value = risultato[i][0]
            window.menuCassandra.appendChild(paragraph) */
          } 

  
          console.log(risultato['resultMongo'])
          // carico menu di mongo 
          for (var valMongo in risultato['resultMongo']){
            var paragraph = document.createElement("option");
            console.log(valMongo)
            /* paragraph.textContent= risultato[i][0]
            paragraph.value = risultato[i][0]
            window.menuCassandra.appendChild(paragraph) */
          } 

          console.log(risultato['resultDynamo'])
          // carico menu di cassandra 
          for (var valDynamo in risultato['resultDynamo']){
            var paragraph = document.createElement("option");
            console.log(valDynamo)
            /* paragraph.textContent= risultato[i][0]
            paragraph.value = risultato[i][0]
            window.menuCassandra.appendChild(paragraph) */
          } 

          /*
          if (output.firstChild){
            output.removeChild(output.firstChild)
          }
          for (const j in risultato){
            output.innerHTML+=risultato[j]+"<br>"
          } */

        })
        })
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
            paragraph.textContent= risultato[i][0]
            paragraph.value = risultato[i][0]
            menuPostgres.appendChild(paragraph)
            //menuPostgres.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })
}

selezionePartenza();
window.onload = caricamentoPostgres();
window.menuPostgres = document.getElementById('menuPostgres');
window.menuCassandra = document.getElementById('menuCassandra');
window.menuMongo = document.getElementById('menuMongo');
window.menuDynamo = document.getElementById('menuDynamo');
window.output = document.getElementById('output');
