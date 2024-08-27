# datastore.py

from collections import deque
from typing import Any, Dict, List, Union, Optional
import csv
import os
import time

from utilities import MappingManager, ModelStartTime, PrintManager, InsufficientDataError

# Basis klasse voor het beheren van data-opslag
class DataStoreManager:
    def __init__(self, event_name_out: str):
        # Initialiseer een lijst om data op te slaan
        self.data_queue = []  # Veranderd van deque() naar list()
        current_directory = os.getcwd()
        print(current_directory)

        # SELECTEER HIER OF JE MET DOCKER RUNT OF NIET
        self.filename_output = f'{current_directory}/output/long_out/{event_name_out}_history.csv'
        #self.filename_output = f'app/output/Docker_out/{event_name_out}_history.csv'
        self.print_manager = PrintManager()
        

    # Methode om gegevens op te slaan in de data queue
    def store_data(self, event: Dict[str, Any]):
        self.data_queue.append(event)

    # Methode om opgeslagen gegevens naar een CSV-bestand te loggen
    def log_to_csv(self, headers: List[str]):
        print(f"Logging to: {self.filename_output}")

        try:
            # Zorg ervoor dat de output directory bestaat
            #os.makedirs(os.path.dirname(self.filename_output), exist_ok=True)

            # Open het bestand en schrijf de data
            with open(self.filename_output, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                for entry in self.data_queue:
                    writer.writerow(entry.values())

            print(f"Data successfully logged to {self.filename_output}")

        except Exception as e:
            print(f"Error while logging data to CSV: {e}")

    # Methode om veranderingen in opgeslagen gegevens te detecteren
    def detect_change(self, key: str) -> bool:
        try:
            values = self.get_value(2, key)
        except InsufficientDataError as e:
            return True
        return values[0] != values[1]

    # Methode om de laatste x waarden van een bepaalde sleutel te verkrijgen
    def get_value(self, x: int, key: str) -> List[Any]:
        if len(self.data_queue) < x:
            raise InsufficientDataError(f"Insufficient data for the last {x} values")
        return [entry[key] for entry in self.data_queue[-x:]]

    # Methode om alle waarden uit de laatste x seconden te verkrijgen
    def get_values_seconds(self, x, key):
        """
        Geef alle waarden uit de laatste x seconden terug.
        Als er niet genoeg data is, geef een waarschuwing en gooi een gespecialiseerde fout.
        """
        cutoff = ModelStartTime.get_elapsed_time() - x
        if not self.data_queue or self.data_queue[0]['timestamp'] > cutoff:
            raise InsufficientDataError(f"Insufficient data for the last {x} seconds", self.__class__.__name__)
        return [entry[key] for entry in self.data_queue if entry['timestamp'] >= cutoff]
    
    # Methode om de waarde van x seconden geleden te verkrijgen
    def get_value_at_seconds_ago(self, x, key):
        """
        Geef de waarde van x seconden geleden terug.
        Als er niet genoeg data is, geef een waarschuwing en gooi een gespecialiseerde fout.
        """
        values = self.get_values_seconds(x, key)
        return values[-1]

    # Methode om het gemiddelde van alle waarden uit de laatste x seconden te verkrijgen
    def get_avg_value_seconds(self, x, key):
        """
        Geef het gemiddelde van alle waarden uit de laatste x seconden terug.
        Als er niet genoeg data is, geef een waarschuwing en gooi een gespecialiseerde fout.
        """
        values = self.get_values_seconds(x, key)
        return sum(values) / len(values)

    # Methode om een gebeurtenis te parseren; moet worden geïmplementeerd door subclasses
    def parse_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError("parse_event moet worden geïmplementeerd door subclasses")

# Subklasse voor het beheren van integer data
class DataStoreManagerInteger(DataStoreManager):
    def parse_event(self, unparsed_event: Any) -> Dict[str, int]:
        """
        Parse een integer event naar het juiste formaat.
        """
        try:
            float_value = float(unparsed_event)
            # Afronden tot 2 decimalen
            rounded_value = round(float_value, 2)
            return {'timestamp': ModelStartTime.get_elapsed_time(), 'integer': rounded_value}
        except (ValueError, TypeError):
            return {'timestamp': ModelStartTime.get_elapsed_time(), 'integer': 0}

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'integer'])

# Subklasse voor het beheren van rule-based result data
class DataStoreManagerRuleBasedResult(DataStoreManager):
    def parse_event(self, event: Any) -> Dict[str, Any]:
        """
        Parse een RuleBasedResult event naar het juiste formaat.
        """
        return {
            'timestamp': ModelStartTime.get_elapsed_time(),
            'output': event.output,
            'input': event.input_values,
            'relevant': event.relevant_rules,
            'string_output': self.map_output_to_string(event.output)
        }

    def map_output_to_string(self, output: Any) -> str:
        """
        Converteer een output waarde naar een string.
        """
        return str(output)

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'output', 'input', 'relevant', 'string_output'])

# Subklasse voor het beheren van string data
class DataStoreManagerString(DataStoreManager):
    def parse_event(self, unparsed_event: Any) -> Dict[str, Union[float, str]]:
        """
        Parse een string event naar het juiste formaat.
        """
        return {'timestamp': ModelStartTime.get_elapsed_time(), 'string': str(unparsed_event)}

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'string'])

# Subklasse voor het beheren van JSON data
class DataStoreManagerJSON(DataStoreManager):
    def parse_event(self, unparsed_event: Any) -> Dict[float, Any]:
        """
        Parse een JSON event naar het juiste formaat.
        """
        return {'timestamp': ModelStartTime.get_elapsed_time(), 'JSON': unparsed_event}

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'JSON'])

# Subklasse voor het beheren van boolean data
class DataStoreManagerBool(DataStoreManager):
    def parse_event(self, unparsed_event: Any) -> Dict[str, Any]:
        """
        Parse een boolean event naar het juiste formaat.
        """
        value = unparsed_event.lower() in ['true', '1']
        return {'timestamp': ModelStartTime.get_elapsed_time(), 'bool': value}

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'bool'])

# Subklasse voor het beheren van gemapte string data
class DataStoreManagerMappedString(DataStoreManager):
    def parse_event(self, unparsed_event: str) -> Dict[str, Union[float, str, int]]:
        """
        Parse een gemapt string event naar het juiste formaat.
        """
        return {
            'timestamp': ModelStartTime.get_elapsed_time(),
            'string': unparsed_event,
            'integer': MappingManager().map_string_to_integer(unparsed_event, self.filename)
        }

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'string', 'integer'])

# Subklasse voor het beheren van rule-based elapsed time data
class DataStoreManagerRuleBasedElapsed(DataStoreManager):
    def parse_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse het event om verstreken tijd sinds de laatste actie, gemiddelde intensiteit, actieduur, en maximale intensiteit te extraheren.
        """
        return {
            'timestamp': ModelStartTime.get_elapsed_time(),
            'elapsed_since_last_action': event['elapsed_since_last_action'],
            'average_intensity': event['average_intensity'],
            'action_duration': event['action_duration'],
            'max_intensity': event['max_intensity']
        }

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'elapsed_since_last_action', 'average_intensity', 'action_duration', 'max_intensity'])

# Subklasse voor het beheren van HRV data
class DataStoreManagerHRV(DataStoreManager):
    def parse_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse een HRV event naar het juiste formaat.
        """
        return {
            'timestamp': ModelStartTime.get_elapsed_time(),
            'RMSSD': event['rmssd_event'],
            'LFn': event['LFn_event'],
            'HFn': event['HFn_event'],
            'LF': event['LF_event'],
            'HF': event['HF_event']
        }

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'RMSSD', 'LFn', 'HFn', 'LF', 'HF'])

# Subklasse voor het beheren van delta data
class DataStoreManagerDelta(DataStoreManager):
    def parse_event(self, event: Dict[str, Union[int, float]]) -> Dict[str, Union[int, float]]:
        """
        Parse een delta event naar het juiste formaat.
        """
        return {
            'timestamp': ModelStartTime.get_elapsed_time(),
            'delta_absolute': event['delta_absolute'],
            'delta_percentage': event['delta_percentage'],
            'delta_absolute_past': event['delta_absolute_past'],
            'delta_percentage_past': event['delta_percentage_past']
        }

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'delta_absolute', 'delta_percentage', 'delta_absolute_past', 'delta_percentage_past'])

# Subklasse voor het beheren van elapsed time data
class DataStoreManagerElapsedTime(DataStoreManager):
    def parse_event(self, event: Dict[str, int]) -> Dict[str, int]:
        """
        Parse een elapsed time event naar het juiste formaat.
        """
        return {
            'timestamp': ModelStartTime.get_elapsed_time(),
            'elapsed_time': event['elapsed_time'],
            'action_count': event['action_count']
        }

    def log_to_csv(self):
        super().log_to_csv(['timestamp', 'elapsed_time', 'action_count'])