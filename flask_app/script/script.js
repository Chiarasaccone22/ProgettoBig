function prova(){
    //const button = document.getElementById('myButton');

    //button.addEventListener('click', () => {
    //document.addEventListener('DOMContentLoaded',function(){
    // Esegui lo script al click del bottone

    // carico menu a tendina 1
    const outputElement = document.getElementById('menu1');

    const response = fetch(`http://localhost:8080/connPostgres`, { method: 'GET', headers: { 'Accept': 'application/json',},
      }).then(response => {
        const postgresJson = response.json()
        postgresJson.then(risultato => {
          console.log(risultato)
          for (i in risultato){
            var paragraph = document.createElement("option");
            paragraph.textContent= risultato[i]
            outputElement.appendChild(paragraph)
            //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })

    // carico menu a tendina 2
    const outputElement2 = document.getElementById('menu2');

    const response2 = fetch(`http://localhost:8080/connMongo`, { method: 'GET', headers: { 'Accept': 'application/json',},
    }).then(response2 => {
      const mongoJson = response2.json()
      mongoJson.then(risultato =>{
        console.log(risultato[0])
        risultato = risultato[0]
        for (i in risultato){
          //console.log(risultato[i])
          var paragraph = document.createElement("option");
          paragraph.textContent= risultato[i]['AIRPORT']
          outputElement2.appendChild(paragraph)
          //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })


    // carico menu a tendina 3
    const outputElement3 = document.getElementById('menu3');

    const response3 = fetch(`http://localhost:8080/connDynamo`, { method: 'GET', headers: { 'Accept': 'application/json',},
    }).then(response3 => {
      const dynamoJson = response3.json()
      dynamoJson.then(risultato =>{
        console.log(risultato['Items'])
        risultato = risultato['Items']
        for (i in risultato){
          //console.log(risultato[i])
          var paragraph = document.createElement("option");
          paragraph.textContent= risultato[i]['name']
          outputElement3.appendChild(paragraph)
          //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
        }
      })
    })


    
}

window.onload = prova;