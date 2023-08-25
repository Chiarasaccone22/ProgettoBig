function prova(){
    //const button = document.getElementById('myButton');

    //button.addEventListener('click', () => {
    //document.addEventListener('DOMContentLoaded',function(){
    // Esegui lo script al click del bottone

    // carico menu a tendina 2
    const outputElement2 = document.getElementById('menu2');
    const response2 = fetch(`http://localhost:8080/connDynamo`, { method: 'GET',
                                                                    headers: { 'Accept': 'application/json',},
    }).then(response2 => {console.log(response2)}).then(data => {console.log(data)})
    /* for (i in dataArray){
        console.log('ciao')
        console.log(dataArray[i])
        var paragraph = document.createElement("option");
        paragraph.textContent= dataArray[i]
        outputElement.appendChild(paragraph)
        //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
    } 
    })*/
    ;

    // carico menu a tendina 1
    const outputElement = document.getElementById('menu1');
      const response = fetch(`http://localhost:8080/connPostgres`, { method: 'GET',
                                                                      headers: { 'Accept': 'application/json',},
      }).then(response => response.json()).then(dataArray => { 
       for (i in dataArray){
          console.log(dataArray[i])
          var paragraph = document.createElement("option");
          paragraph.textContent= dataArray[i]
          outputElement.appendChild(paragraph)
          //outputElement.textContent += `Risultato dello script: ${dataArray[i]}`;
      }
    })  
}

window.onload = prova;