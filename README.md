# Thesis Project

Dit is het thesisproject van Wout Vercauter. Dit project maakt gebruik van Docker om een Python-script uit te voeren dat gegevens fysiologische gegevens verwerkt in de vorm van streams en zo verschillende CSV-bestanden genereert.

## Beschrijving

Het uiteindelijke doel is een uitgebreid scala aan streams te ontwikkelen die verschillende gedragingen van het individu zoals sportactiviteiten, alcoholgebruik en slaap monitoren. Synchroon opereert ook een stream dat stress voorspelt zonder contextuele input. Wanneer deze ‘fysiologische stressreactie’-stream een positief signaal geeft, wordt gekeken naar de contextuele streams om de veranderingen in fysiologische parameters mogelijks te verklaren. Op deze manier kunnen de vals positieve van de reële stresssignalen gescheiden worden op een transparante manier. In het eerste deel van dit hoofdstuk wordt de architectuur van deze streams toegelicht, met hun verschillende eigenschappen en hun onderlinge interacties.

## Vereisten

Om dit project te gebruiken, heb je het volgende nodig:

- **Docker**: Dit is nodig om de gecontaineriseerde omgeving te draaien.
- **Python Libraries**: De volgende Python-bibliotheken worden gebruikt in dit project:
  - **`scikit-fuzzy`**: Gebruikt voor fuzzy logic controlesystemen.
  - **`neurokit2`**: Gebruikt voor neurofysiologische signaalverwerking.
  - **`numpy`**: Voor numerieke berekeningen.
  - **`pandas`**: Voor datamanipulatie en -analyse.
  - **`matplotlib`**: Voor het visualiseren van data.

Deze bibliotheken worden automatisch geïnstalleerd in de Docker-container wanneer de image wordt gebouwd.

## Installatie en Gebruik

Volg deze stappen om het project te installeren, de Docker-image te bouwen en de container uit te voeren:

1. **Kloon de repository en bouw de Docker-image**:

   Gebruik git om de repository te klonen naar je lokale machine en bouw daarna de Docker-image:

   ```bash
   git clone https://github.com/woutvercauter/Thesis_Project.git
   cd Thesis_Project
   docker build -t mijn-python-app .

2. **Run conatiner**:
   docker run -it --rm -v "$(pwd)/output:/output" mijn-python-app

   Dit commando start de container en koppelt de output map op je lokale machine aan de /output map in de container. Hierdoor worden de gegenereerde CSV-bestanden opgeslagen in de output map op je machine. De optie --rm zorgt ervoor dat de container automatisch wordt verwijderd nadat deze is gestopt.
