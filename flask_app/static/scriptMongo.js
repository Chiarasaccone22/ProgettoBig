
function selezioneAeroporto(){

  menuMongo.addEventListener("change", function() {
    // prendo valore assegnato all'opzione
    console.log(menuMongo[menuMongo.selectedIndex].value)
    var aeroporto=menuMongo[menuMongo.selectedIndex].value
    // invoco metodo del backend
    const response = fetch(`http://localhost:8080/selectmongocascata/`+aeroporto, { method: 'GET', headers: { 'Accept': 'application/json',},
      }).then(response => {
        var mongoJson= response.json()
        mongoJson.then(risultato =>{
          
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

  
          console.log(risultato['resultDynamo'])
          /*console.log(risultato['resultDynamo'].length) */
          // carico menu di mongo 
          console.log('DYNAMO:')
          var scorroDynamo = risultato['resultDynamo']
          // ripuliscomenu a tendina per inserire elementi selezionati
          while (window.menuDynamo.firstChild) {
            window.menuDynamo.removeChild(window.menuDynamo.firstChild);
          }
          // mentto nel menu pulito gli elementi selezionati
          for (var valDynamo in scorroDynamo){
            console.log(scorroDynamo[valDynamo][0])
            var opt = scorroDynamo[valDynamo][0]

            var paragraph = document.createElement("option");
            paragraph.textContent= opt['name']
            paragraph.value = opt['compagnia_id']
            window.menuDynamo.appendChild(paragraph)
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
            paragraph.textContent= opt[9]
            paragraph.value = opt[9]
            window.menuPostgres.appendChild(paragraph)
          } 

        })
        })
  });
}

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
          paragraph.value = risultato[i]['IATA_CODE']
          menuMongo.appendChild(paragraph)
          //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })
}

selezioneAeroporto();
window.onload = caricamentoMongo();
window.menuMongo = document.getElementById('menuMongo');
window.menuCassandra = document.getElementById('menuCassandra');
window.menuPostgres = document.getElementById('menuPostgres');
window.menuDynamo = document.getElementById('menuDynamo');
window.output = document.getElementById('output');