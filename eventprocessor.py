import time
import threading
from datetime import datetime
from collections import deque
from typing import Any, Dict, List, Union

import neurokit2 as nk

from utilities import EventManager, PrintManager, ModelStartTime, InsufficientDataError, MappingManager, PersonInfoManager, RuleBasedResult
from datastore import (
    DataStoreManager,
    DataStoreManagerDelta,
    DataStoreManagerElapsedTime,
    DataStoreManagerInteger,
    DataStoreManagerRuleBasedResult,
    DataStoreManagerString,
    DataStoreManagerJSON,
    DataStoreManagerBool,
    DataStoreManagerMappedString,
    DataStoreManagerHRV,
    DataStoreManagerRuleBasedElapsed,
    InsufficientDataError
)

# Basisinterface voor event processing
class EventProcessor:
    def __init__(self, event_manager, event_name_in, event_name_out, data_type, change=False):
        self.event_manager = event_manager
        self.event_name_in = event_name_in
        self.event_name_out = event_name_out
        self.event_manager.subscribe(self.process_event)
        self.print_manager = PrintManager()
        self.data_store_manager = self.create_data_store_manager(data_type, event_name_out)
        self.change = change

    # Creëert de juiste data store manager op basis van het gegeven type data
    def create_data_store_manager(self, data_type, event_name_out):
        data_store_classes = {
            'integer': DataStoreManagerInteger,
            'rulebased': DataStoreManagerRuleBasedResult,
            'string': DataStoreManagerString,
            'json': DataStoreManagerJSON,
            'bool': DataStoreManagerBool,
            'mappedstring': DataStoreManagerMappedString,
            'hrv': DataStoreManagerHRV,
            'rulebasedelapsed': DataStoreManagerRuleBasedElapsed,
            'elapsed_time': DataStoreManagerElapsedTime, 
            'delta': DataStoreManagerDelta 
        }
        store_class = data_store_classes.get(data_type)
        if not store_class:
            raise ValueError(f"Unsupported data type: {data_type}")
        self.print_manager.print(self.__class__.__name__, "EventProcessor", "create_data_store_manager", 'MAKE OBJECT', f"Creating data store manager for {event_name_out}")
        return store_class(event_name_out)

    # Verwerkt binnenkomende gebeurtenissen; moet worden geïmplementeerd door subclasses
    def process_event(self, unparsed_or_parsed_event, event_name):
        self.print_manager.print(self.__class__.__name__, "EventProcessor", "process_event", "RECEIVING", f"Received {event_name} with data: {unparsed_or_parsed_event}")
        raise NotImplementedError("process_event moet worden geïmplementeerd door subclasses")

    # Stuurt verwerkte gebeurtenis door naar event manager
    def notify_event(self, parsed_event, event_name):
        self.print_manager.print(self.__class__.__name__, "EventProcessor", "notify_event", "SENDING", f"Sending {event_name} with data: {parsed_event}")
        self.event_manager.publish(parsed_event, event_name)

# Abstracte klasse voor InputEventProcessor
class InputEventProcessor(EventProcessor):
    def __init__(self, event_manager, event_names_in, event_name_out, data_type, change=False):
        super().__init__(event_manager, event_names_in, event_name_out, data_type, change)
    
    def process_event(self, unparsed_event, event_name):
        if self.event_name_in == event_name:
            self.print_manager.print(self.__class__.__name__, "InputEventProcessor", "process_event", "RECEIVING", f"Received {event_name} with data: {unparsed_event}")
            parsed_event = self.data_store_manager.parse_event(unparsed_event)
            self.data_store_manager.store_data(parsed_event)
            self.notify_event(parsed_event, self.event_name_out)

            # Controleert op verandering en stuurt een aangepast event als er een wijziging is
            if self.change and self.data_store_manager.detect_change(self.change):
                self.notify_event(parsed_event, f"{self.event_name_out}_changed")

# Abstracte klasse voor CalculateEventProcessor
class CalculateEventProcessor(EventProcessor):
    def __init__(self, event_manager, event_names_in, event_name_out, data_type, getter_streams, calculate_interval=None, change=False):
        super().__init__(event_manager, event_names_in, event_name_out, data_type, change)
        self.getter_streams = getter_streams
        self.calculate_interval = calculate_interval
        self.last_calculate_time = None
        self.stop_flag = False
        if self.calculate_interval:
            self.start_periodic_event()

    def process_event(self, parsed_event, event_name):
        if event_name in self.event_name_in:
            self.print_manager.print(self.__class__.__name__, "CalculateEventProcessor", "process_event", "RECEIVING", f"Received {event_name} with data: {parsed_event}")
            self.calculate_wrapper(parsed_event)

    def calculate_wrapper(self, parsed_event):
        self.print_manager.print(self.__class__.__name__, "CalculateEventProcessor", "calculate", "CRITICAL")
        calculated_event = self.calculate_by_child(parsed_event)
        calculated_and_parsed_event = self.data_store_manager.parse_event(calculated_event)
        self.data_store_manager.store_data(calculated_and_parsed_event)

        if not isinstance(self.event_name_out, list):
            self.notify_event(calculated_and_parsed_event, self.event_name_out)
            if self.change and self.data_store_manager.detect_change():
                self.notify_event(calculated_and_parsed_event, f"{self.event_name_out}_changed")
        else:
            for key, value in calculated_event.items():
                if key in self.event_name_out:
                    self.notify_event(value, key)

    # Abstracte methode voor het uitvoeren van de berekeningen; moet worden geïmplementeerd door subclasses
    def calculate_by_child(self, event):
        raise NotImplementedError("calculate_by_child moet worden geïmplementeerd door subclasses")

    # Methode om periodieke berekeningen uit te voeren op basis van een tijdsinterval
    def periodic_event(self):
        while not self.stop_flag:
            current_time = ModelStartTime.get_elapsed_time()
            if current_time > self.calculate_interval and (self.last_calculate_time is None or (current_time - self.last_calculate_time) > self.calculate_interval):
                event = {'timestamp': current_time}
                self.calculate_wrapper(event)
                self.last_calculate_time = current_time
            time.sleep(self.calculate_interval)

    def start_periodic_event(self):
        thread = threading.Thread(target=self.periodic_event)
        thread.daemon = True
        thread.start()

    def stop_periodic_event(self):
        self.stop_flag = True

# InputStream: Klasse voor het verwerken van input events
class InputStream(InputEventProcessor):
    def __init__(self, event_manager, event_name_in, event_name_out, data_type, change=False):
        super().__init__(event_manager, event_name_in, event_name_out, data_type, change)

# ElapsedTimeStream: Klasse voor het berekenen van verstreken tijd sinds een bepaalde gebeurtenis
class ElapsedTimeStream(CalculateEventProcessor):
    def __init__(self, event_manager, event_names_in, event_name_out, getter_streams=[]):
        super().__init__(event_manager, event_names_in, event_name_out, 'elapsed_time', getter_streams=[])
        self.last_change_time = None
        self.action_count = 0

    def calculate_by_child(self, event):
        current_time = ModelStartTime.get_elapsed_time()
        elapsed_time = 0

        # Probeer laatste bekende bool-waarde op te halen
        try:
            last_event_bool = self.data_store_manager.get_value(1, 'elapsed_time')[0]
        except InsufficientDataError as e:
            self.print_manager.print(self.__class__.__name__, self.event_name_out, event, "CRITICAL")
            if event['bool']:
                # Eerste keer dat een actie wordt gedetecteerd
                self.last_change_time = current_time
                self.action_count += 1
                return {'elapsed_time': -1, 'action_count': self.action_count}
            else:
                # Geen actie gedetecteerd
                self.last_change_time = current_time
                return {'elapsed_time': 1, 'action_count': self.action_count}

        # Bereken de verstreken tijd gebaseerd op de huidige en vorige event status
        if event['bool'] and last_event_bool < 0:
            elapsed_time = -1 * (current_time - self.last_change_time)
        elif not event['bool'] and last_event_bool > 0:
            elapsed_time = 1 * (current_time - self.last_change_time)
        elif event['bool'] and last_event_bool > 0:
            self.last_change_time = current_time
            elapsed_time = -1
            self.action_count += 1
        elif not event['bool'] and last_event_bool < 0:
            self.last_change_time = current_time
            elapsed_time = 1

        return {'elapsed_time': elapsed_time, 'action_count': self.action_count}

# RuleBasedElapsedTimeStream: Klasse voor het berekenen van tijd en intensiteit van acties op basis van regels
class RuleBasedElapsedTimeStream(CalculateEventProcessor):
    def __init__(self, event_manager, event_name_in, event_name_out, getter_streams=[]):
        super().__init__(event_manager, event_name_in, event_name_out, 'rulebasedelapsed', getter_streams=[])
        self.current_action = False
        self.start_time = None
        self.intensity_sum = 0
        self.intensity_count = 0
        self.max_intensity = 0

    def calculate_by_child(self, event):
        current_time = ModelStartTime.get_elapsed_time()
        output = event['output']

        # Controleer of de output boven een bepaalde drempelwaarde ligt
        if output > 50:
            if not self.current_action:
                # Start een nieuwe actie
                self.current_action = True
                self.start_time = current_time
                self.intensity_sum = output
                self.intensity_count = 1
                self.max_intensity = output
            else:
                # Update huidige actie
                self.intensity_sum += output
                self.intensity_count += 1
                if output > self.max_intensity:
                    self.max_intensity = output
            return {'elapsed_since_last_action': 0, 'average_intensity': 0, 'action_duration': 0, 'max_intensity': 0}
        else:
            if self.current_action:
                # Bereken de eigenschappen van de beëindigde actie
                action_duration = current_time - self.start_time
                average_intensity = self.intensity_sum / self.intensity_count if self.intensity_count else 0
                elapsed_since_last_action = action_duration
                max_intensity = self.max_intensity
                self.current_action = False
                self.intensity_sum = 0
                self.intensity_count = 0
                self.max_intensity = 0
                self.start_time = None

                return {
                    'elapsed_since_last_action': elapsed_since_last_action,
                    'average_intensity': average_intensity,
                    'action_duration': action_duration,
                    'max_intensity': max_intensity
                }
            else:
                return {'elapsed_since_last_action': 0, 'average_intensity': 0, 'action_duration': 0, 'max_intensity': 0}

# DeltaStream: Klasse voor het berekenen van veranderingen (delta's) in gegevens over tijd
class DeltaStream(CalculateEventProcessor):
    def __init__(self, event_manager, event_name_in, event_name_out, time_interval: int, getter_streams=[]):
        super().__init__(event_manager, event_name_in, event_name_out, 'delta', getter_streams)
        self.time_interval = time_interval

    def calculate_by_child(self, event):
        # Haal de baseline waarde op
        baseline = PersonInfoManager().get_info(self.event_name_in[0])
        if baseline is not None:
            current_value = event['integer']
            delta_absolute = current_value - baseline
            delta_percentage = (delta_absolute / baseline) * 100
            
        # Probeer de waarde van een bepaald aantal seconden geleden op te halen
        try:
            past_value = self.data_store_manager.get_value_at_seconds_ago(self.time_interval, 'delta_absolute')
        except (IndexError, InsufficientDataError) as e:
            past_value = baseline  # Gebruik de baseline als fallback als er geen eerdere waarde beschikbaar is

        delta_absolute_past = current_value - past_value
        if past_value == 0:
            delta_percentage_past = 0
        else:
            delta_percentage_past = (delta_absolute_past / past_value) * 100

        # Retourneer de berekende delta waarden
        return {
            'delta_absolute': delta_absolute,
            'delta_percentage': delta_percentage,
            'delta_absolute_past': delta_absolute_past,
            'delta_percentage_past': delta_percentage_past
        }

# MappedStream: Klasse voor het mappen van strings naar numerieke waarden
class MappedStream(CalculateEventProcessor):
    def __init__(self, event_manager, event_names_in, event_name_out):
        super().__init__(event_manager, event_names_in, event_name_out, 'integer', getter_streams=[])

    def calculate_by_child(self, event):
        # Maakt een mapping van string naar integer waarde
        mapped_value = MappingManager().map_string_to_integer(event['string'], self.event_name_out)
        return mapped_value

# HRVStream: Klasse voor het berekenen van hartslagvariabiliteit (HRV)
class HRVStream(CalculateEventProcessor):
    def __init__(self, event_manager, event_names_in, event_name_out, getter_streams, calculate_interval=60, rolling=300, sample_rate_rr=1000, sample_rate_ecg=130):
        super().__init__(event_manager, event_names_in, event_name_out, 'hrv', getter_streams, calculate_interval)
        self.rolling = rolling
        self.sample_rate_rr = sample_rate_rr
        self.sample_rate_ecg = sample_rate_ecg

    def calculate_by_child(self, event):
        data = []

        if 'rr_ms_processed' in self.getter_streams:
            # Controleer of het systeem lang genoeg draait voor HRV-berekening
            if ModelStartTime.get_elapsed_time() < self.rolling:
                print('lfn_event: ', PersonInfoManager().get_info("LFn_processed"))
                print('hfn_event: ', PersonInfoManager().get_info("HFn_processed"))

                # Retourneer eerdere waarden als de HRV-berekening nog niet kan worden uitgevoerd
                return {'rmssd_event': PersonInfoManager().get_info("RMSSD_processed") , 'LFn_event': PersonInfoManager().get_info("LFn_processed"), 'LF_event': PersonInfoManager().get_info("LF_processed"), 'HF_event': PersonInfoManager().get_info("HF_processed"), 'HFn_event': PersonInfoManager().get_info("HFn_processed"), 'LF_HF_event': PersonInfoManager().get_info("LF_HF_processed")}
            
            try:
                # Haal gegevens op voor HRV-berekening
                data = self.getter_streams['rr_ms_processed'].data_store_manager.get_values_seconds(self.rolling, 'integer')
                if not data:  # Controleer of data leeg is
                    raise InsufficientDataError("No data available for rr_ms_processed")
            
            except InsufficientDataError as e:
                self.print_manager.print(self.__class__.__name__, "HRVStream", "calculate_by_child", "WARNING", "No data available for rr_ms_processed")
                return {'rmssd_event': PersonInfoManager().get_info("RMMSD_processed") , 'LFn_event': PersonInfoManager().get_info("LFn_processed"), 'LF_event': PersonInfoManager().get_info("LF_processed"), 'HF_event': PersonInfoManager().get_info("HF_processed"), 'HFn_event': PersonInfoManager().get_info("HFn_processed"), 'LF_HF_event': PersonInfoManager().get_info("LF_HF_processed")}
            
            # Bereken pieken en HRV metrics
            peaks = nk.intervals_to_peaks(data)
            
            hrv_time = nk.hrv_time(peaks, sampling_rate=self.sample_rate_rr)
            hrv_freq = nk.hrv_frequency(peaks, sampling_rate=self.sample_rate_rr, normalize=False)
            hrv_freq_norm = nk.hrv_frequency(peaks, sampling_rate=self.sample_rate_rr, normalize=True)
            
            rmssd = hrv_time.get('HRV_RMSSD').iloc[0] if 'HRV_RMSSD' in hrv_time else 0
            lf = hrv_freq.get('HRV_LF').iloc[0] if 'HRV_LF' in hrv_freq else 0
            hf = hrv_freq.get('HRV_HF').iloc[0] if 'HRV_HF' in hrv_freq else 0
            lfn = hrv_freq_norm.get('HRV_LF').iloc[0] if 'HRV_LF' in hrv_freq_norm else 0
            hfn = hrv_freq_norm.get('HRV_HF').iloc[0] if 'HRV_HF' in hrv_freq_norm else 0
            lf_hf_ratio = hrv_freq.get('HRV_LFHF').iloc[0] if 'HRV_LFHF' in hrv_freq else 0

            # Retourneer de berekende HRV waarden
            return {'rmssd_event': rmssd, 'LFn_event': lfn, 'LF_event': lf, 'HF_event': hf, 'HFn_event': hfn, 'LF_HF_event': lf_hf_ratio}

        elif 'ecg_processed' in self.getter_streams:
            try:
                # Haal ECG-gegevens op voor HRV-berekening
                data = self.getter_streams['ecg_processed'].data_store_manager.get_values_seconds(self.rolling, 'integer')
                if not data:  # Controleer of data leeg is
                    raise InsufficientDataError("No data available for ecg_processed")
            except InsufficientDataError as e:
                self.print_manager.print(self.__class__.__name__, "HRVStream", "calculate_by_child", "WARNING", str(e))
                return {'rmssd_event': PersonInfoManager().get_info("RMMSD_processed") , 'LFn_event': PersonInfoManager().get_info("LFn_processed"), 'LF_event': PersonInfoManager().get_info("LF_processed"), 'HF_event': PersonInfoManager().get_info("HF_processed"), 'HFn_event': PersonInfoManager().get_info("HFn_processed"), 'LF_HF_event': PersonInfoManager().get_info("LF_HF_processed")}

# StrategyStream: Klasse voor het uitvoeren van berekeningen op basis van een strategie
class StrategyStream(CalculateEventProcessor):
    """
    Een gegeneraliseerde klasse voor het verwerken van gebeurtenissen met behulp van een strategie.
    """
    def __init__(self, event_manager, event_name_out, getter_streams, strategy, calculate_interval, strategy_name, consequent_name, antecedent_names, fault, **extra_info):
        """
        Initialiseert de StrategyStream.

        Parameters:
            event_manager: De EventManager instantie.
            event_name_out: De naam van het uitvoerevent.
            getter_streams: Dict die invoervariabelen koppelt aan (stream, veld) tuples.
            strategy: Het strategie-object.
            calculate_interval: Het interval waarop moet worden berekend.
            strategy_name: De naam van de strategie.
            consequent_name: De naam van de consequent variabele.
            antecedent_names: Lijst van antecedent variabele namen.
            fault: De uitvoerwaarde wanneer de strategie faalt.
            extra_info: Extra informatie die aan de strategie wordt doorgegeven.
        """
        super().__init__(event_manager, [], event_name_out, 'rulebased', getter_streams, calculate_interval)
        self.strategy = strategy
        self.antecedent_names = antecedent_names
        self.default_output = fault
        # Stel de strategie in met zijn naam, de consequent en alle antecedenten
        self.strategy.set_attributes(strategy_name, consequent_name, *antecedent_names, **extra_info)

    def calculate_by_child(self, event):
        # Verzamelt invoerwaarden van de getter streams
        input_values = {}
        for name in self.antecedent_names:
            if name in self.getter_streams:
                stream, field = self.getter_streams[name]
                try:
                    if stream == 'self':
                        # Verkrijg de gemiddelde waarde over 100 seconden
                        input_values[name] = self.data_store_manager.get_avg_value_seconds(100, field)
                    else:
                        # Verkrijg de meest recente event data
                        input_values[name] = stream.data_store_manager.get_value(1, field)
                    
                    if input_values[name] is None:
                        raise ValueError(f"Geen data gevonden voor {name}")

                except (InsufficientDataError, KeyError, ValueError) as e:
                    # Gebruik fallback-waarde van PersonInfoManager
                    input_values[name] = PersonInfoManager().get_info(name)
                    # De lus gaat verder, zelfs na een fout

        # Voer de strategie uit met de verzamelde invoerwaarden

        #OPTIONEEL
        try:
            strategy_output = self.strategy.execute(**input_values)
        except Exception as e:
            strategy_output = None

        if (strategy_output is None):
            if isinstance(self.default_output, int):
                return RuleBasedResult(self.default_output, 0, 0)
            else:
                try:
                    return RuleBasedResult(self.default_output.data_store_manager.get_value(1, 'output'), 0, 0)
                except InsufficientDataError as e:
                    return RuleBasedResult(0, 0, 0)
        
        return RuleBasedResult(strategy_output.output, strategy_output.input_values, strategy_output.relevant_rules)