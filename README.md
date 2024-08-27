# Thesis Project

Dit is het thesisproject van Wout Vercauter. Dit project maakt gebruik van Docker om een Python-script uit te voeren dat gegevens fysiologische gegevens verwerkt in de vorm van streams en zo verschillende CSV-bestanden genereert.

## Beschrijving

Het uiteindelijke doel is een uitgebreid scala aan streams te ontwikkelen die verschillende gedragingen van het individu zoals sportactiviteiten, alcoholgebruik en slaap monitoren. Synchroon opereert ook een stream dat stress voorspelt zonder contextuele input. Wanneer deze ‘fysiologische stressreactie’-stream een positief signaal geeft, wordt gekeken naar de contextuele streams om de veranderingen in fysiologische parameters mogelijks te verklaren. Op deze manier kunnen de vals positieve van de reële stresssignalen gescheiden worden op een transparante manier. In het eerste deel van dit hoofdstuk wordt de architectuur van deze streams toegelicht, met hun verschillende eigenschappen en hun onderlinge interacties.

Dit alles maakt gebruik van fuzzy-technologie voor zijn berekeningen.

## Vereisten

Om dit project te gebruiken, heb je het volgende nodig:

- **Docker**: Dit is nodig om de gecontaineriseerde omgeving te draaien.
- **Python Libraries**: De volgende Python-bibliotheken worden gebruikt in dit project:
  - **`scikit-fuzzy`**: Gebruikt voor fuzzy logic controlesystemen.
  - **`neurokit2`**: Gebruikt voor neurofysiologische signaalverwerking, geval van deze thesis voor verwerking HRV-gegevens.
  - **`numpy`**: Voor numerieke berekeningen.
  - **`pandas`**: Voor datamanipulatie en -analyse.
  - **`matplotlib`**: Voor het visualiseren van data.

Deze bibliotheken worden automatisch geïnstalleerd in de Docker-container wanneer de image wordt gebouwd.

## Installatie en Gebruik

Volg deze stappen om het project te installeren, de Docker-image te bouwen en de container uit te voeren:

1. **Kloon de repository en bouw de Docker-image**:

   Gebruik git om de repository te klonen naar je lokale machine en bouw daarna de Docker-image:

   ```bash
   git clone https://github.com/woutvercauter/Thesis_Project_Stress.git
   cd Thesis_Project
   docker build -t mijn-python-app .

2. **Run conatiner**:
   docker run -it --rm -v "$(pwd)/output:/output" mijn-python-app

   Dit commando start de container en koppelt de output map de lokale machine aan de /output map in de container. Hierdoor worden de gegenereerde CSV-bestanden opgeslagen in de output map op je lokale machine. De optie --rm zorgt ervoor dat de container automatisch wordt verwijderd nadat deze is gestopt.

3. **Press Ctrl+c**:
   Dit stopt het uitwisselen van data en schrijft de opgebouwde lijsten naar app\output\Docker_out

## Interpretatie

Bijvoorbeeld uit: ‘BewegingSport_processed_history.csv’:
85.37,45.751726006640574,"{'HR_bpm': [134.89], 'Activiteit_sport': [7.0], 'Poi_sport': [10.0], 'BewegingSport_recent': 0}","{9: array([0.25]), 10: array([0.70864865]), 16: array([0.25])}",45.751726006640574

85.37 -> zoveel seconden sinds start metingen.
45.751726006640574 -> score tussen 0 en 10 die wordt gegeven over de intensiteit van de sport.
"{'HR_bpm': [134.89], 'Activiteit_sport': [7.0], 'Poi_sport': [10.0], 'BewegingSport_recent': 0}"
-> de inputwaarden waarmee de fuzzylogica aan de slag is gegaan.
"{9: array([0.25]), 10: array([0.70864865]), 16: array([0.25])}"
-> de regels en hun waarheidsgehalte.

Deze regels waren dus bijvoorbeeld:
 
Regel 10: {'HR_bpm': 'drempel', 'Poi_sport': 'hoog'}, {'Intensiviteit_sport': 'gemiddeld'} of als HR_bpm boven aerobe drempel en Poi_sport is hoog (gemapped getal door mappingmanager, gym is bv 10/10, office een 2 ofzo) dan is de Intensiviteit van sport gemiddeld. Deze regel zal voor het grootste deel meewegen (0.7)

Regel 16: {'HR_bpm': 'drempel', 'Activiteit_sport': 'hoog', 'BewegingSport_recent': 'niet'}, {'Intensiviteit_sport': 'heel kort'} of als HR_bpm boven de aerobe drempel en de detection van sport hoog is en de afgelopen 10 minuten geen sport is vastgesteld (gemiddeld), dan is de intensiviteit van sport heel kort (0.25)
