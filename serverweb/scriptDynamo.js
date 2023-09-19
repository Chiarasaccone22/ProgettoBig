

function selezioneCompagnia(){

  menuDynamo.addEventListener("change", function() {
    // prendo valore assegnato all'opzione
    console.log(menuDynamo[menuDynamo.selectedIndex].value)
    var compagnia=menuDynamo[menuDynamo.selectedIndex].value
    // invoco metodo del backend
    const response = fetch(`http://localhost:8080/selectdynamocascata/`+compagnia, { method: 'GET',mode: 'no-cors', headers: { 'Accept': 'application/json',},
      }).then(response => {
        var dynamoJson= response.json()
        dynamoJson.then(risultato =>{
          
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
            paragraph.textContent= opt
            paragraph.value = opt
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

          console.log(risultato['resultPostgres'])
          /*console.log(risultato['resultPostgres'].length) */
          // carico menu di cassandra
          console.log('Postgres:')
          var scorroPostgres = risultato['resultPostgres']
          // ripuliscomenu a tendina per inserire elementi selezionati
          while (window.menuPostgres.firstChild) {
            window.menuPostgres.removeChild(window.menuPostgres.firstChild);
          }
          for (var valPostgres in scorroPostgres){
            console.log(scorroPostgres[valPostgres][0])
            var opt = scorroPostgres[valPostgres][0]

            var paragraph = document.createElement("option");
            paragraph.textContent= opt[3]
            paragraph.value = opt[3]
            window.menuPostgres.appendChild(paragraph)
          } 

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
    const response = await fetch(`http://localhost:8080/connDynamo`, { method: 'GET', mode: 'no-cors',headers: { 'Accept': 'application/json',},
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
window.menuDynamo = document.getElementById('menuDynamo');
window.menuMongo = document.getElementById('menuMongo');
window.menuCassandra = document.getElementById('menuCassandra');
window.menuPostgres = document.getElementById('menuPostgres');
window.output = document.getElementById('output');
