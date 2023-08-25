import csv

# Apri il file CSV in modalità di lettura
with open('/home/chiara/archive/flights.csv', 'r') as csvfile:
    # Crea un oggetto lettore CSV
    csvreader = csv.reader(csvfile)

    # Inizializza un contatore per tenere traccia delle righe lette
    count = 0

    """     # Crea un nuovo file CSV in modalità di scrittura
    with open('/home/chiara/Documenti/GitHub/ProgettoBig/flask_app/Dataset/timestamp_1000.csv', 'w', newline='') as output_csvfile:
        # Crea un oggetto scrittore CSV
        csvwriter = csv.writer(output_csvfile)
        
        # Scrivi le prime 10 colonne delle righe nel nuovo file
        for row in csvreader:
            if count < 1000:
                selected_columns = row[:11] + [row[14]]+ row[18:19] + row[21: 22] + row[24:26]# Seleziona le colonne desiderate
                csvwriter.writerow(selected_columns)
                count += 1
            else:
                break  """

    
     # Crea un nuovo file CSV in modalità di scrittura
    with open('/home/chiara/Documenti/GitHub/ProgettoBig/flask_app/Dataset/intervalli_1000.csv', 'w', newline='') as output_csvfile:
        # Crea un oggetto scrittore CSV
        csvwriter = csv.writer(output_csvfile)
        
        # Scrivi le prime 10 colonne delle righe nel nuovo file
        for row in csvreader:
            if count < 1000:
                selected_columns = row[:11] +  row[12:13] + row[15: 17] + [row[18]] + [row[20]]+ row[23:31]# Seleziona le colonne desiderate
                csvwriter.writerow(selected_columns)
                count += 1
            else:
                break 
    
""" 
Leggenda di cosa va preso e cosa no:
YEAR,MONTH,DAY,DAY_OF_WEEK,AIRLINE,FLIGHT_NUMBER,TAIL_NUMBER,ORIGIN_AIRPORT,DESTINATION_AIRPORT,    9 (1 e 2)
SCHEDULED_DEPARTURE,DEPARTURE_TIME,     11 (1)
DEPARTURE_DELAY,TAXI_OUT, 13 (2)
WHEELS_OFF, 14  (1)
SCHEDULED_TIME,ELAPSED_TIME,AIR_TIME, 17 (2)
DISTANCE, 18 (1 e 2)
WHEELS_ON, 19 (1)
TAXI_IN, 20 (2)
SCHEDULED_ARRIVAL,ARRIVAL_TIME, 22 (1)
ARRIVAL_DELAY, 23 (2)
DIVERTED,CANCELLED,CANCELLATION_REASON, 26 (1 e 2)
AIR_SYSTEM_DELAY,SECURITY_DELAY,AIRLINE_DELAY,LATE_AIRCRAFT_DELAY,WEATHER_DELAY (2) """
