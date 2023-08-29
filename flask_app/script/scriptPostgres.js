async function caricamentoPostgres(){
    //const button = document.getElementById('myButton');

    //button.addEventListener('click', () => {
    //document.addEventListener('DOMContentLoaded',function(){
    // Esegui lo script al click del bottone

    // carico menu a tendina 1
    const outputElement = document.getElementById('menu1');

    const response = await fetch(`http://localhost:8080/connPostgres`, { method: 'GET', headers: { 'Accept': 'application/json',},
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
}

window.onload = caricamentoPostgres();