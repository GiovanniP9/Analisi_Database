import numpy as np
import csv
csv_path = "videogame.csv"

def load_data(csv_path):
    """
    Carica il dataset dei videogiochi da un file CSV usando il modulo csv.
    Ritorna un ndarray strutturato con i campi:
    Name, Platform, Year, Genre, Publisher,
    NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales
    """
    # Definizione del tipo strutturato
    dtype = [("Name", "U100"), ("Platform", "U50"), ("Year", int),
             ("Genre", "U50"), ("Publisher", "U100"),
             ("NA_Sales", float), ("EU_Sales", float),
             ("JP_Sales", float), ("Other_Sales", float), ("Global_Sales", float)]

    records = []
    with open(csv_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                record = (
                    row['Name'],
                    row['Platform'],
                    int(float(row['Year'])) if row['Year'] else 0,
                    row['Genre'],
                    row['Publisher'],
                    float(row['NA_Sales'] or 0),
                    float(row['EU_Sales'] or 0),
                    float(row['JP_Sales'] or 0),
                    float(row['Other_Sales'] or 0),
                    float(row['Global_Sales'] or 0)
                )
                records.append(record) # te lo salva in un record
            except ValueError:
                # Salta righe mal formattate
                continue

    data = np.array(records, dtype=dtype)
    return data

#funzione per calcolare le vendite di una regione specifica
def analisi_vendite_regioni(data, region):
    
    if region not in data.dtype.names:
        raise ValueError(f"Regione '{region}' non valida.")
    return np.sum(data[region])  # Somma delle vendite per la regione specificata

#funzione per calcolare le vendite globali di un gioco specifico in base all'anno
def total_sales_for_game_year(data, game_name, year):

    mask = (data['Name'] == game_name) & (data['Year'] == year)
    if np.any(mask): # Se esistono vendite per il gioco e l'anno specificati
        return np.sum(data[mask]['Global_Sales'])
    else:
        print(f"Nessuna vendita trovata per il gioco '{game_name}' nell'anno {year}.")
        return 0.0


#funzione per calcolare le vendite globali in base alla piattaforma in tutti gli anni
def  top_platform_sales(data):
    
    platform = np.unique(data['Platform'])
    totals = {}
    for plat in platform:
        total = np.sum(data['Global_Sales'][data['Platform'] == plat])
        #costruiamo un dizionario con le piattaforme e le vendite globali
        totals[plat] = total
    # Ordina le piattaforme in base alle vendite globali
    best = max(totals, key=totals.get)
    return best, totals[best]  # Restituisce la piattaforma con le vendite globali più alte e il totale delle vendite

# funzione per calcolare le vendite globali in base all'editore in tutti gli anni
def top_publisher_sales(data):
    publishers = np.unique(data['Publisher'])
    totals = {}
    for pub in publishers:
        total = np.sum(data['Global_Sales'][data['Publisher'] == pub])
        #costruiamo un dizionario con gli editori e le vendite globali
        totals[pub] = total
    # Ordina gli editori in base alle vendite globali
    best = max(totals, key=totals.get)
    return best, totals[best]  # Restituisce l'editore con le vendite globali più alte e il totale delle vendite

# funzione per calcolare le vendite globali in base al genere
def top_genre_sales(data):
    genres = np.unique(data['Genre'])
    totals = {}
    for genre in genres:
        total = np.sum(data['Global_Sales'][data['Genre'] == genre])
        #costruiamo un dizionario con i generi e le vendite globali
        totals[genre] = total
    # Ordina i generi in base alle vendite globali
    best = max(totals, key=totals.get)
    return best, totals[best]  # Restituisce il genere con le vendite globali più alte e il totale delle vendite

#funzione per calcolare la vendita media per genere globale in tutti gli anni
def average_sales_by_genre(data):
    genres = np.unique(data['Genre'])
    averages = {}
    for g in genres:
        mean = np.mean(data['Global_Sales'][data['Genre'] == g])
        #costruiamo un dizionario con i generi e le vendite medie
        averages[g] = mean
    return averages

#funzione per calcolare la somma delle vendite di una piattaforma in base all'anno
def yearly_sales_by_platform(data, platform):
    years = np.unique(data['Year'])
    trends = {}
    for y in years:
        mask = (data['Year'] == y) & (data['Platform'] == platform)
        if np.any(mask):
            total = np.sum(data[mask]['Global_Sales'])
            trends[y] = total
    return trends  # Restituisce un dizionario con gli anni e le vendite globali per la piattaforma specificata

    
#funzione per calcolare il numero minimo di vendite di un pubblisher in base all'anno
def min_sales_by_publisher(data, publisher):
    years = np.unique(data['Year'])
    mins = {}
    for y in years:
        mask = (data['Year'] == y) & (data['Publisher'] == publisher)
        if np.any(mask):
            total = np.min(data[mask]['Global_Sales'])
            mins[y] = total
    return mins  # Restituisce un dizionario con gli anni e le vendite minime per l'editore specificato

#funzione per stampare i primi 10 giochi in base alle vendite globali
def top_10_games(data):
    
    sorted_data = np.sort(data, order='Global_Sales')[::-1]  # Ordina in ordine decrescente
    return sorted_data[:10]  # Restituisce i primi 10 giochi

#funzione per usare a menu tutte le funzioni
def menu(data):
    while True:
        print("\n--- MENU ANALISI VENDITE VIDEOGIOCHI ---")
        print("1. Vendite totali per regione")
        print("2. Vendite globali di un gioco per anno")
        print("3. Piattaforma con più vendite globali")
        print("4. Editore con più vendite globali")
        print("5. Genere con più vendite globali")
        print("6. Vendita media per genere")
        print("7. Vendite per piattaforma per anno")
        print("8. Vendita minima per editore per anno")
        print("9. Top 10 giochi per vendite globali")
        print("0. Esci")

        scelta = input("Scegli un'opzione: ")
        match scelta:
            case "1":
                regione = input("Inserisci il nome della regione (NA_Sales, EU_Sales, JP_Sales, Other_Sales, Global_Sales): ")
                try:
                    totale = analisi_vendite_regioni(data, regione)
                    print(f"Totale vendite per la regione '{regione}': {totale:.2f} milioni")
                except ValueError as e:
                    print(e)

            case "2":
                nome = input("Inserisci il nome del gioco: ")
                anno = int(input("Inserisci l'anno: "))
                totale = total_sales_for_game_year(data, nome, anno)
                print(f"Vendite globali di '{nome}' nel {anno}: {totale:.2f} milioni")

            case "3":
                try:
                    piattaforma, vendite = top_platform_sales(data)
                    print(f"Piattaforma con più vendite: {piattaforma} ({vendite:.2f} milioni)")
                except Exception as e:
                    print("Errore:", e)

            case "4":
                editore, vendite = top_publisher_sales(data)
                print(f"Editore con più vendite: {editore} ({vendite:.2f} milioni)")

            case "5":
                genere, vendite = top_genre_sales(data)
                print(f"Genere con più vendite: {genere} ({vendite:.2f} milioni)")

            case "6":
                medie = average_sales_by_genre(data)
                print("\nVendita media per genere:")
                for genere, media in medie.items():
                    print(f"{genere}: {media:.2f} milioni")

            case "7":
                piattaforma = input("Inserisci il nome della piattaforma: ")
                vendite_annuali = yearly_sales_by_platform(data, piattaforma)
                if vendite_annuali:
                    print(f"\nVendite per piattaforma '{piattaforma}' per anno:")
                    for anno, vendite in sorted(vendite_annuali.items()):
                        print(f"{anno}: {vendite:.2f} milioni")
                else:
                    print("Nessuna vendita trovata per la piattaforma.")

            case "8":
                editore = input("Inserisci il nome dell'editore: ")
                vendite_minime = min_sales_by_publisher(data, editore)
                if vendite_minime:
                    print(f"\nVendite minime per editore '{editore}' per anno:")
                    for anno, vendite in sorted(vendite_minime.items()):
                        print(f"{anno}: {vendite:.2f} milioni")
                else:
                    print("Nessuna vendita trovata per l'editore.")

            case "9":
                print("\nTop 10 giochi per vendite globali:")
                top = top_10_games(data)
                for i, gioco in enumerate(top, 1):
                    print(f"{i}. {gioco['Name']} ({gioco['Global_Sales']:.2f} milioni)")

            case "0":
                print("Uscita dal programma. A presto!")
                break

            case _:
                print("Scelta non valida. Riprova.")

menu(load_data(csv_path))