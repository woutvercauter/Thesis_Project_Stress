# main.py

from datastore import (
    DataStoreManagerInteger,
    DataStoreManagerRuleBasedResult,
    DataStoreManagerString,
    DataStoreManagerJSON,
    DataStoreManagerBool,
    DataStoreManagerMappedString,
    DataStoreManagerHRV,
    DataStoreManagerRuleBasedElapsed
)
from utilities import PrintManager, ModelStartTime, PersonInfoManager, MappingManager, EventManager, Sender
from eventprocessor import (
    ElapsedTimeStream,
    RuleBasedElapsedTimeStream,
    DeltaStream,
    MappedStream,
    HRVStream,
    InputStream,
    StrategyStream
)
from RulesLogic.TestStrategyFinalAlternative import FuzzyStrategy
from datastore import InsufficientDataError
import os

def main() -> None:
    # Initialiseer de EventManager
    event_manager = EventManager()

    # Verkrijg de huidige werkdirectory en print deze
    current_directory = os.getcwd()
    print(current_directory)

    # Configureer PersonInfoManager met initiële gegevens van de persoon
    person_info_manager = PersonInfoManager()
    person_info_manager.set_person_info({
        "HR_bpm_processed": 70,
        "rr_ms_processed": 800,
        "TMP_processed": 24,
        "LF_processed": 10000,
        "HF_processed": 10000,
        "HFn_processed": 0.1,
        "LFn_processed": 0.1,
        "RMSSD_processed": 400,
        "SDNN_processed": 100,
        "LF_HF_processed": 1,
        "age": 30,
        "gender": "male",
        'fysiologische_stressreactie': 0,  # Geen baseline/default beschikbaar; waarde moet berekend worden
        'BewegingSport': 0,
        'Roken': 5,
        'Cafeïne': -1,
        'Temperatuurschommeling': -1,
        'EtenTijdSindsMaaltijd': -1,
        'AlcoholHoeveelheid': -1,
        'HR_bpm': -1,
        'Activiteit_sport': -1,
        'Poi_sport': -1,
        'BewegingSport_recent' : 0,
        'LF_delta': 0,
        'HF_delta': 0,
        'RMSSD_delta': 0,
        'LFn_delta': 0,
        'HFn_delta': 0,
        'LF_HF_ratio': 0
    })

    # Maak Strategy-objecten voor verschillende soorten stressdetectie
    strategy_sport = FuzzyStrategy()
    strategy_fysiologische_stressreactie = FuzzyStrategy()
    strategy_mentale_stress = FuzzyStrategy()

    # Creëer InputStreams voor verschillende gegevens
    hr_bpm_stream = InputStream(event_manager, "HR [bpm]", "HR_bpm_processed", 'integer')
    rr_ms_stream = InputStream(event_manager, "RR-interval [ms]", "rr_ms_processed", 'integer')
    tmp_stream = InputStream(event_manager, "TMP_event", "TMP_processed", 'integer')
    activity_recognition_stream = InputStream(event_manager, "ActivityRecognition_event", "ActivityRecognition_processed", 'string', change='string')
    poi_stream = InputStream(event_manager, "POI_event", "POI_processed", 'string')
    sleep_stream = InputStream(event_manager, "Sleep_event", "Sleep_processed", 'bool')
    eating_stream = InputStream(event_manager, "Eating_event", "Eating_processed", 'bool')
    smoking_stream = InputStream(event_manager, "Smoking_event", "Smoking_processed", 'bool')
    caffeine_stream = InputStream(event_manager, "Caffeine_event", "Caffeine_processed", 'bool')
    alcohol_stream = InputStream(event_manager, "Alcohol_event", "Alcohol_processed", 'bool')
    #medicine_stream = InputStream(event_manager, "Medicine_event", "Medicine_processed", 'bool')

    # Creëer Elapsed Time Streams om de tijd sinds een bepaalde gebeurtenis te berekenen
    sleep_elapsed_time_stream = ElapsedTimeStream(event_manager, ["Sleep_processed"], "SleepElapsedTime_processed")
    eating_elapsed_time_stream = ElapsedTimeStream(event_manager, ["Eating_processed"], "EatingElapsedTime_processed")
    smoking_elapsed_time_stream = ElapsedTimeStream(event_manager, ["Smoking_processed"], "SmokingElapsedTime_processed")
    caffeine_elapsed_time_stream = ElapsedTimeStream(event_manager, ["Caffeine_processed"], "CaffeineElapsedTime_processed")
    alcohol_elapsed_time_stream = ElapsedTimeStream(event_manager, ["Alcohol_processed"], "AlcoholElapsedTime_processed")
    #medicine_elapsed_time_stream = ElapsedTimeStream(event_manager, ["Medicine_processed"], "MedicineElapsedTime_processed")
    
    # Maak Mapped Streams om activiteit en locaties te koppelen aan sporten
    activity_recognition_mapped_sport_stream = MappedStream(event_manager, ["ActivityRecognition_processed"], "ActivityRecognitionMappedSport_processed")
    poi_mapped_sport_stream = MappedStream(event_manager, ["POI_processed"], "POIMappedSport_processed")
    
    # Maak HRVStream om verschillende parameters te berekenen en te monitoren
    hrv_stream = HRVStream(event_manager, [], ["rmssd_event", "LFn_event", "LF_event", "HF_event", "HFn_event"], getter_streams={'rr_ms_processed': rr_ms_stream}, calculate_interval=5, rolling=300)
    lfn_stream = InputStream(event_manager, "LFn_event", "LFn_processed", "integer")
    lf_stream = InputStream(event_manager, "LF_event", "LF_processed", "integer")
    hf_stream = InputStream(event_manager, "HF_event", "HF_processed", "integer")
    hfn_stream = InputStream(event_manager, "HFn_event", "HFn_processed", "integer")
    rmssd_stream = InputStream(event_manager, "rmssd_event", "RMSSD_processed", "integer")
    lf_hf_ratio_stream = InputStream(event_manager, "'LF_HF_event'", "LF/HF_ratio_processed", "integer")
    
    # Creëer Delta Streams voor het berekenen van veranderingen over tijd
    rr_ms_delta_stream = DeltaStream(event_manager, ["rr_ms_processed"], "rr_ms_delta_processed", time_interval=60)
    tmp_delta_stream = DeltaStream(event_manager, ["TMP_processed"], "TMP_delta_processed", time_interval=60)
    lf_delta_stream = DeltaStream(event_manager, ["LF_processed"], "LF_delta_processed", time_interval=60)
    hf_delta_stream = DeltaStream(event_manager, ["HF_processed"], "HF_delta_processed", time_interval=60)
    rmssd_delta_stream = DeltaStream(event_manager, ["RMSSD_processed"], "RMSSD_delta_processed", time_interval=60)
    lfn_delta_stream = DeltaStream(event_manager, ["LFn_processed"], "LFn_delta_processed", time_interval=60)
    hfn_delta_stream = DeltaStream(event_manager, ["HFn_processed"], "HFn_delta_processed", time_interval=60)

    # Configureer de streams voor sport
    beweging_sport_stream = StrategyStream(
        event_manager=event_manager,
        event_name_out="BewegingSport_processed",
        getter_streams={
            'HR_bpm': (hr_bpm_stream, 'integer'),
            'Activiteit_sport': (activity_recognition_mapped_sport_stream, 'integer'),
            'Poi_sport': (poi_mapped_sport_stream, 'integer'),
            'BewegingSport_recent' : ('self', 'integer')
        },
        strategy=strategy_sport,
        calculate_interval=5,
        strategy_name="Sport",
        consequent_name="Intensiviteit_sport",
        fault=0, # Wanneer er geen data beschikbaar is/ of geen enkele regel van de regelset voldoet -> 0
        antecedent_names=['HR_bpm', 'Activiteit_sport', 'Poi_sport', 'BewegingSport_recent'],
        leeftijd=35
    )

    # Stream voor herstel na fysieke activiteit
    herstel_stream = RuleBasedElapsedTimeStream(event_manager=event_manager, event_name_in="BewegingSport_processed", event_name_out="Herstel_processed")
                                                
    # Configureer de streams voor fysiologische stressrespons
    fysiologische_stress_stream = StrategyStream(
        event_manager=event_manager,
        event_name_out="FysiologischeStressreactie_processed",
        getter_streams={
            'LF_delta': (lf_delta_stream, 'delta_percentage'),
            'HF_delta': (hf_delta_stream, 'delta_percentage'),
            'RMSSD_delta': (rmssd_delta_stream, 'delta_percentage'),
            'LFn_delta': (lfn_delta_stream, 'delta_percentage'),
            'HFn_delta': (hfn_delta_stream, 'delta_percentage'),
            'LF_HF_ratio': (lf_hf_ratio_stream, 'integer')
        },
        strategy=strategy_fysiologische_stressreactie,
        calculate_interval=5,
        strategy_name="fysiologische_stressreactie",
        consequent_name="fysiologische_stress_niveau",
        fault=0, # Wanneer er geen data beschikbaar is/ of geen enkele regel van de regelset voldoet -> 0
        antecedent_names=['RMSSD_delta', 'LF_HF_ratio', 'LFn_delta', 'HFn_delta', 'LF_delta', 'HF_delta']
    )

    # Configureer de streams voor mentale stress
    mentale_stress_stream = StrategyStream(
        event_manager=event_manager,
        event_name_out="MentaleStress_processed",
        getter_streams={
            'fysiologische_stressreactie': (fysiologische_stress_stream, 'output'),
            'BewegingSport': (beweging_sport_stream, 'output'),
            'Roken': (smoking_elapsed_time_stream, 'elapsed_time'),
            'Cafeïne': (caffeine_elapsed_time_stream, 'elapsed_time'),
            'Temperatuurschommeling': (tmp_delta_stream, 'delta_absolute'),
            'EtenTijdSindsMaaltijd': (eating_elapsed_time_stream, 'elapsed_time'),
            'AlcoholHoeveelheid': (alcohol_elapsed_time_stream, 'action_count')
        },
        strategy=strategy_mentale_stress,
        calculate_interval=2,
        strategy_name="mentale_stress",
        consequent_name="mentale_stress",
        fault=fysiologische_stress_stream, # Wanneer er geen data beschikbaar is/ of geen enkele regel van de regelset voldoet -> fysiologische_stressreactie = mentale_stress
        antecedent_names=[
            'fysiologische_stressreactie', 'BewegingSport', 'Roken', 'Cafeïne',
            'Temperatuurschommeling'
        ]
    )

    # Configureer de Sender om gebeurtenissen uit een CSV-bestand te verzenden
    sender = Sender(event_manager)
    try:
        # Zie voor output in output/long_out (of Docker_out als je met docker werkt)
        sender.send_from_csv('Updated_Filtered_and_Modified_Data_test_inputs.csv')
    except KeyboardInterrupt:
        sender.stop_sending()
        print("Gestopt door gebruiker")

        # Log de gegevens van alle streams naar CSV-bestanden. Hierin duidelijk de werking van model te zien.
        streams = [
            hr_bpm_stream, rr_ms_stream, tmp_stream, activity_recognition_stream, poi_stream, sleep_stream,
            smoking_stream, caffeine_stream, alcohol_stream, activity_recognition_mapped_sport_stream,
            poi_mapped_sport_stream, sleep_elapsed_time_stream, smoking_elapsed_time_stream,
            caffeine_elapsed_time_stream, alcohol_elapsed_time_stream, hrv_stream, 
            rr_ms_delta_stream, tmp_delta_stream, rmssd_delta_stream, lfn_delta_stream, hfn_delta_stream,
            beweging_sport_stream, 
            fysiologische_stress_stream, 
            mentale_stress_stream, 
            lfn_stream, hfn_stream, rmssd_stream, herstel_stream
        ]

        for stream in streams:
            stream.data_store_manager.log_to_csv()

if __name__ == "__main__":
    main()