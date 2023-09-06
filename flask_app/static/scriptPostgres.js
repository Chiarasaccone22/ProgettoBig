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
          /*console.log(risultato['resultCassandra'].length)
          console.log(risultato['resultCassandra'][0][0]) */
          // carico menu di cassandra 
          console.log('CASSANDRA:')
          var scorroCassandra = risultato['resultCassandra']
          // ripuliscomenu a tendina per inserire elementi selezionati
          while (window.menuCassandra.firstChild) {
            window.menuCassandra.removeChild(window.menuCassandra.firstChild);
          }
          for (var valCassandra in scorroCassandra){
            console.log(scorroCassandra[valCassandra][0])
            var opt = scorroCassandra[valCassandra][0]

            var paragraph = document.createElement("option");
            paragraph.textContent= opt[0]
            paragraph.value = opt[0]
            window.menuCassandra.appendChild(paragraph)
          } 

  
          console.log(risultato['resultMongo'])
          /*console.log(risultato['resultMongo'].length) */
          // carico menu di mongo 
          console.log('MONGO:')
          var scorroMongo = risultato['resultMongo']
          // ripuliscomenu a tendina per inserire elementi selezionati
          while (window.menuMongo.firstChild) {
            window.menuMongo.removeChild(window.menuMongo.firstChild);
          }
          // mentto nel menu pulito gli elementi selezionati
          for (var valMongo in scorroMongo){
            console.log(scorroMongo[valMongo][0])
            var opt = scorroMongo[valMongo][0]

            var paragraph = document.createElement("option");
            paragraph.textContent= opt['AIRPORT']
            paragraph.value = opt['IATA_CODE']
            window.menuMongo.appendChild(paragraph)
          } 

          console.log(risultato['resultDynamo'])
          /*console.log(risultato['resultDynamo'].length) */
          // carico menu di cassandra
          console.log('DYNAMO:')
          var scorroDynamo = risultato['resultDynamo']
          // ripuliscomenu a tendina per inserire elementi selezionati
          while (window.menuDynamo.firstChild) {
            window.menuDynamo.removeChild(window.menuDynamo.firstChild);
          }
          for (var valDynamo in scorroDynamo){
            console.log(scorroDynamo[valDynamo][0])
            var opt = scorroDynamo[valDynamo][0]

            var paragraph = document.createElement("option");
            paragraph.textContent= opt['name']
            paragraph.value = opt['compagnia_id']
            window.menuDynamo.appendChild(paragraph)
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
