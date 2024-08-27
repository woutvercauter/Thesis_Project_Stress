from typing import List, Callable, Any, Optional, Dict, Union
import csv
import time
from datetime import datetime
from threading import Lock

class InsufficientDataError(Exception):
    """
    Foutklasse die aangeeft dat er onvoldoende data beschikbaar is.
    """
    def __init__(self, message, classname=None):
        super().__init__(message)
        self.classname = classname if classname else "UnknownClass"

class RuleBasedResult:
    """
    Een klasse die het resultaat vertegenwoordigt van een regelgebaseerde berekening.
    """
    def __init__(self, output: Any, input_values: Dict[str, Any], relevant_rules: Dict[str, bool]) -> None:
        """
        Initialiseer de RuleBasedResult met de berekende output, inputwaarden en relevante regels.

        :param output: Het berekende resultaat van de regelgebaseerde logica.
        :param input_values: De inputwaarden die zijn gebruikt bij de berekening.
        :param relevant_rules: Een dict die aangeeft welke regels relevant waren bij de berekening.
        """
        self.output = output
        self.input_values = input_values
        self.relevant_rules = relevant_rules

    def __repr__(self) -> str:
        """
        Een representatieve string van de RuleBasedResult.
        """
        return f"RuleBasedResult(output={self.output}, input_values={self.input_values}, relevant_rules={self.relevant_rules})"

class EventManager:
    """
    Klasse om evenementabonnementen en publicaties te beheren.
    """
    def __init__(self) -> None:
        self.subscribers: List[Callable[[Any, str], None]] = []

    def subscribe(self, callback: Callable[[Any, str], None]) -> None:
        """
        Abonneer een callback op evenementen.
        """
        self.subscribers.append(callback)

    def publish(self, event: Any, event_name: str) -> None:
        """
        Publiceer een evenement naar alle geabonneerde abonnees.
        """
        for subscriber in self.subscribers:
            subscriber(event, event_name)

class Sender:
    """
    Klasse verantwoordelijk voor het verzenden van evenementen vanuit een CSV-bestand.
    """
    def __init__(self, event_manager: EventManager) -> None:
        self.event_manager = event_manager
        self.start_time: datetime = None
        self.stop_flag: bool = False
        self.print_manager = PrintManager()

    def parse_timestamp(self, timestamp: str) -> datetime:
        """
        Parseer de timestamp met meerdere formaten om verschillende datetime-strings te verwerken.
        """
        for fmt in ('%Y-%m-%d %H:%M:%S.%f%z', '%Y-%m-%d %H:%M:%S%z'):
            try:
                return datetime.strptime(timestamp, fmt)
            except ValueError:
                continue
        raise ValueError(f"Timestamp '{timestamp}' komt niet overeen met een bekend formaat.")

    def send_from_csv(self, csv_file: str, skip_lines: int = 0) -> None:
        """
        Stuur evenementen vanuit een CSV-bestand, te beginnen na een bepaald aantal overgeslagen regels.
        """
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            headers = reader.fieldnames
            print("CSV Headers:", headers)

            # Sla de eerste regels over
            for _ in range(skip_lines):
                next(reader, None)

            for row in reader:
                if self.stop_flag:
                    print("Verzenden gestopt.")
                    break
                timestamp = row['timestamp']
                event_datetime = self.parse_timestamp(timestamp)

                # Bereken de relatieve tijd in seconden vanaf de starttijd
                if self.start_time is None:
                    self.start_time = event_datetime
                elapsed_time = (event_datetime - self.start_time).total_seconds()

                current_time = time.time()
                if not hasattr(self, 'runtime_start_time'):
                    self.runtime_start_time = current_time
                elapsed_time_runtime = current_time - self.runtime_start_time
                wait_time = elapsed_time - elapsed_time_runtime

                if wait_time > 0:
                    time.sleep(wait_time)

                for eventtype in headers[1:]:  # Sla de 'timestamp' header over
                    event = row[eventtype]
                    if event:  # Verwerk alleen als er een waarde is
                        self.print_manager.print("Sender", "Sender", "send_from_csv", "SENDING", f"{eventtype}: {event}")
                        self.event_manager.publish(event, eventtype)

    def stop_sending(self) -> None:
        """
        Stop met het verzenden van evenementen.
        """
        self.stop_flag = True

COLORS = {
    'INFO': '\033[92m',   # Groen
    'SENDING': '\033[96m',   # Cyaan
    'RECEIVING': '\033[90m',   # Grijs
    'DEBUG': '\033[91m',   # Rood
    'CRITICAL': '\033[95m',  # Magenta
    'MAKE OBJECT': '\033[93m',   # Geel
    'RESULT': '\033[101m',   # Rode achtergrond
    'WARNING': '\033[95m',  # Magenta
    'ENDC': '\033[0m'     # Einde kleur
}

ICONS = {
    'INFO': '\u2139\ufe0f ',   # Informatie
    'DEBUG': '\u274c ',   # Kruisje
    'CRITICAL': '\u26a0\ufe0f ',  # Waarschuwing
    'SENDING': '\u27a1\ufe0f ',  # Rechter pijl
    'RECEIVING': '\u2b05\ufe0f ',   # Linker pijl
    'MAKE OBJECT': '\U0001f528 ',  # Hamer
    'RESULT': '\U0001f4c8 ',  # Grafiek
    'WARNING': '\u26a0\ufe0f ',  # Waarschuwing
}

class ModelStartTime:
    """
    Singleton klasse om de starttijd van het model bij te houden.
    """
    _instance: Optional['ModelStartTime'] = None
    _start_time: Optional[datetime] = None

    def __new__(cls: type) -> 'ModelStartTime':
        if cls._instance is None:
            cls._instance = super(ModelStartTime, cls).__new__(cls)
            cls._start_time = datetime.now()
        return cls._instance

    @staticmethod
    def get_start_time() -> datetime:
        if ModelStartTime._start_time is None:
            ModelStartTime._start_time = datetime.now()
        return ModelStartTime._start_time

    @staticmethod
    def get_elapsed_time() -> float:
        start_time = ModelStartTime.get_start_time()
        elapsed_time = datetime.now() - start_time
        return round(elapsed_time.total_seconds(), 2)

class PrintManager:
    """
    Singleton klasse om berichten te beheren met verschillende kleurcodes.
    """
    _instance: Optional['PrintManager'] = None
    _lock: Lock = Lock()

    def __new__(cls: type) -> 'PrintManager':
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(PrintManager, cls).__new__(cls)
                    cls._instance._configured_streams = None
                    cls._instance._configured_streams_bool = True
        return cls._instance

    def configure_printing(self, streamingsonderdelen: List[str], bool: bool = True) -> None:
        self._configured_streams = streamingsonderdelen
        self._configured_streams_bool = bool

    def should_print(self, message: str) -> bool:
        if self._configured_streams is None:
            return True
        return any(substring in message for substring in self._configured_streams)

    def print(self, streamingsonderdeel: str, klasse: str, methode: str, type: str, uitleg: str = "") -> None:
        elapsed_time = ModelStartTime.get_elapsed_time()
        message = f"{elapsed_time:.2f}s - {ICONS.get(type, '')} {streamingsonderdeel} - {klasse}  ::  {methode} - {type}"
        if uitleg:
            message += f" - {uitleg}"
        if self.should_print(message):
            color = COLORS.get(type, COLORS['ENDC'])
            if type in ['SENDING', 'RECEIVING', 'CRITICAL']:
                print(f"  {color}{message}{COLORS['ENDC']}")  # Extra spatie voor inspringen
            else:
                print(f"{color}{message}{COLORS['ENDC']}")

class PersonInfoManager:
    """
    Singleton klasse om persoonspecifieke informatie te beheren.
    """
    _instance: Optional['PersonInfoManager'] = None

    def __new__(cls: type) -> 'PersonInfoManager':
        if cls._instance is None:
            cls._instance = super(PersonInfoManager, cls).__new__(cls)
            cls._instance.person_info = {}
        return cls._instance

    def set_person_info(self, person_info: Dict[str, Union[int, float, str]]) -> None:
        self.person_info = person_info

    def get_info(self, key: str) -> Union[int, float, str, None]:
        return self.person_info.get(key, None)

class MappingManager:
    """
    Singleton klasse om mappings van stringwaarden naar integers te beheren.
    """
    _instance: Optional['MappingManager'] = None

    def __new__(cls: type) -> 'MappingManager':
        if cls._instance is None:
            cls._instance = super(MappingManager, cls).__new__(cls)
            cls._instance.mappings = {
                "ActivityRecognitionMappedSport_processed": {
                    'Liggen': 1, 'Zitten': 1, 'Sedentair': 5, 'Staan': 5,
                    'Onderweg': 7, 'Verplaatsing': 7, 'Wandelen': 7, 'Fietsen': 7
                },
                "POIMappedSport_processed": {
                    'playground': 10, 'arena': 10, 'gym': 10,
                    'park': 8, 'recreation_center': 8,
                    'school': 6, 'university': 6, 'stadium': 6,
                    'office': 4, 'home': 4, 'shop': 4,
                    'restaurant': 2, 'bar': 2,
                    'default': 0
                }
            }
        return cls._instance

    def map_string_to_integer(self, event_string: str, event_name_out: str) -> int:
        return self.mappings.get(event_name_out, {}).get(event_string, 0)