import csv

# Apri il file CSV in modalità di lettura
with open('/home/chiara/archive/flights.csv', 'r') as csvfile:
    # Crea un oggetto lettore CSV
    csvreader = csv.reader(csvfile)

    # Salta l'intestazione (se presente)
    #next(csvreader)

    # Inizializza un contatore per tenere traccia delle righe lette
    count = 0

    # Crea un nuovo file CSV in modalità di scrittura
    with open('/home/chiara/archive/output_file1.csv', 'w', newline='') as output_csvfile:
        # Crea un oggetto scrittore CSV
        csvwriter = csv.writer(output_csvfile)
        
        # Scrivi le prime 50 righe nel nuovo file
        for row in csvreader:
            if count < 500:
                csvwriter.writerow(row)
                count += 1
            else:
                break
