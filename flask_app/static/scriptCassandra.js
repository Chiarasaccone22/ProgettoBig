//const menuCassandra = document.getElementById('menuCassandra');

function selezioneIdVolo(){
  menuCassandra.addEventListener("change",function(){
    console.log(menuCassandra[menuCassandra.selectedIndex].value)
    var idVolo = menuCassandra[menuCassandra.selectedIndex].value
    const response = fetch(`http://localhost:8080/selectcassandracascata/`+idVolo, { method: 'GET', headers: { 'Accept': 'application/json',},
      }).then(response => {
        var cassandraJson = response.json()
        cassandraJson.then(risultato =>{
          
          console.log('Result cassandra:')
          console.log(risultato['resultPostgres'])
          /*console.log(risultato['resultPostgres'].length)
          console.log(risultato['resultPostgres'][0][0]) */
          // carico menu di cassandra 
          console.log('POSTGRES:')
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

        })
        })
  })
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

selezioneIdVolo();
window.onload = caricamentoCassandra();
window.menuCassandra = document.getElementById('menuCassandra');
window.menuPostgres = document.getElementById('menuPostgres');
window.menuMongo = document.getElementById('menuMongo');
window.menuDynamo = document.getElementById('menuDynamo');
window.output = document.getElementById('output');