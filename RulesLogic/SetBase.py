import skfuzzy as fuzz
from skfuzzy import control as ctrl

#from RulesLogic.RuleHolder import RuleHolder
from skfuzzy.control import ControlSystem, Antecedent, Consequent, Rule, ControlSystemSimulation
import numpy as np
import sys
import os
import matplotlib.pyplot as plt


# Bepaal de huidige directory van dit script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Ga één directory omhoog naar de project root
project_root = os.path.abspath(os.path.join(current_dir, '..'))

# Voeg de project_root directory toe aan sys.path
if project_root not in sys.path:
    sys.path.append(project_root)

from RulesLogic.RuleHolderB import RuleHolder
from utilities import PrintManager


class FuzzyVariablesAntecedents:
    def __init__(self, *args, **extra_info):
        self.antecedents = {}
        self.print_manager = PrintManager()
        self.print_manager.print(None, "FuzzyVariablesAntecedents", "__init__", "MAKE OBJECT", f"Antecedents: {args}, Extra info: {extra_info}")

        for arg in args:
            if arg == 'HR_bpm':
                if 'leeftijd' in extra_info:
                    maximum_hartslag = 220 - extra_info['leeftijd']
                    self.antecedents[arg] = ctrl.Antecedent(np.arange(-1, 220, 1), 'HR_bpm')
                    self.antecedents[arg]['zeer laag'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, maximum_hartslag * 0.5])
                    self.antecedents[arg]['licht'] = fuzz.trimf(self.antecedents[arg].universe, [maximum_hartslag * 0.45, maximum_hartslag * 0.55, maximum_hartslag * 0.65])
                    self.antecedents[arg]['drempel'] = fuzz.trimf(self.antecedents[arg].universe, [maximum_hartslag * 0.6, maximum_hartslag * 0.7 , maximum_hartslag * 0.8])
                    self.antecedents[arg]['hoog'] = fuzz.trimf(self.antecedents[arg].universe, [maximum_hartslag * 0.8, maximum_hartslag, 220])
                    self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-1, -1, -1])
                else:
                    raise ValueError("Leeftijd is een verplichte parameter voor het initialiseren van de hartslagzone")

            elif arg == 'Activiteit_sport':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-1, 11, 1), 'Activiteit_sport')
                self.antecedents[arg]['laag'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 3])
                self.antecedents[arg]['gemiddeld'] = fuzz.trimf(self.antecedents[arg].universe, [3, 5, 7])
                self.antecedents[arg]['hoog'] = fuzz.trimf(self.antecedents[arg].universe, [6, 10, 10])
                self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-1, -1, -1])

            elif arg == 'Poi_sport':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-1, 11, 1), 'Poi_sport')
                self.antecedents[arg]['laag'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 8])
                self.antecedents[arg]['hoog'] = fuzz.trimf(self.antecedents[arg].universe, [2, 10, 10])
                self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-1, -1, -1])


            elif arg == 'BewegingSport_recent':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-1, 10, 1), 'BewegingSport_recent')
                self.antecedents[arg]['niet'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 2])
                self.antecedents[arg]['licht'] = fuzz.trimf(self.antecedents[arg].universe, [1, 3, 5])
                self.antecedents[arg]['zwaar'] = fuzz.trimf(self.antecedents[arg].universe, [4, 7, 10])
                self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-1, -1, -1])
            
            # Corrected to match rule terms
            elif arg == 'RMSSD_delta':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-100, 101, 1), 'RMSSD_delta')
                self.antecedents[arg]['grote daling'] = fuzz.trimf(self.antecedents[arg].universe, [-100, -100, -40])
                self.antecedents[arg]['lichte daling'] = fuzz.trimf(self.antecedents[arg].universe, [-40, -20, 0])
                self.antecedents[arg]['constant'] = fuzz.trimf(self.antecedents[arg].universe, [-5, 0, 5])
                self.antecedents[arg]['lichte stijging'] = fuzz.trimf(self.antecedents[arg].universe, [0, 20, 40])
                self.antecedents[arg]['grote stijging'] = fuzz.trimf(self.antecedents[arg].universe, [40, 100, 100])

            elif arg == 'SDNN_delta':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-100, 101, 1), 'SDNN_delta')
                self.antecedents[arg]['grote daling'] = fuzz.trimf(self.antecedents[arg].universe, [-100, -100, -40])
                self.antecedents[arg]['lichte daling'] = fuzz.trimf(self.antecedents[arg].universe, [-40, -20, 0])
                self.antecedents[arg]['constant'] = fuzz.trimf(self.antecedents[arg].universe, [-5, 0, 5])
                self.antecedents[arg]['lichte stijging'] = fuzz.trimf(self.antecedents[arg].universe, [0, 20, 40])
                self.antecedents[arg]['grote stijging'] = fuzz.trimf(self.antecedents[arg].universe, [40, 100, 100])

            elif arg == 'LF_delta':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-100, 101, 1), 'LF_delta')
                self.antecedents[arg]['grote daling'] = fuzz.trimf(self.antecedents[arg].universe, [-100, -100, -40])
                self.antecedents[arg]['lichte daling'] = fuzz.trimf(self.antecedents[arg].universe, [-40, -20, 0])
                self.antecedents[arg]['constant'] = fuzz.trimf(self.antecedents[arg].universe, [-5, 0, 5])
                self.antecedents[arg]['lichte stijging'] = fuzz.trimf(self.antecedents[arg].universe, [0, 20, 40])
                self.antecedents[arg]['grote stijging'] = fuzz.trimf(self.antecedents[arg].universe, [40, 100, 100])

            elif arg == 'HF_delta':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-100, 101, 1), 'HF_delta')
                self.antecedents[arg]['grote daling'] = fuzz.trimf(self.antecedents[arg].universe, [-100, -100, -40])
                self.antecedents[arg]['lichte daling'] = fuzz.trimf(self.antecedents[arg].universe, [-40, -20, 0])
                self.antecedents[arg]['constant'] = fuzz.trimf(self.antecedents[arg].universe, [-5, 0, 5])
                self.antecedents[arg]['lichte stijging'] = fuzz.trimf(self.antecedents[arg].universe, [0, 20, 40])
                self.antecedents[arg]['grote stijging'] = fuzz.trimf(self.antecedents[arg].universe, [40, 100, 100])

            elif arg == 'LFn_delta':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-100, 101, 1), 'LFn_delta')
                self.antecedents[arg]['grote daling'] = fuzz.trimf(self.antecedents[arg].universe, [-100, -100, -40])
                self.antecedents[arg]['lichte daling'] = fuzz.trimf(self.antecedents[arg].universe, [-40, -20, 0])
                self.antecedents[arg]['constant'] = fuzz.trimf(self.antecedents[arg].universe, [-5, 0, 5])
                self.antecedents[arg]['lichte stijging'] = fuzz.trimf(self.antecedents[arg].universe, [0, 20, 40])
                self.antecedents[arg]['grote stijging'] = fuzz.trimf(self.antecedents[arg].universe, [40, 100, 100])

            elif arg == 'HFn_delta':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-100, 101, 1), 'HFn_delta')
                self.antecedents[arg]['grote daling'] = fuzz.trimf(self.antecedents[arg].universe, [-100, -100, -40])
                self.antecedents[arg]['lichte daling'] = fuzz.trimf(self.antecedents[arg].universe, [-40, -20, 0])
                self.antecedents[arg]['constant'] = fuzz.trimf(self.antecedents[arg].universe, [-5, 0, 5])
                self.antecedents[arg]['lichte stijging'] = fuzz.trimf(self.antecedents[arg].universe, [0, 20, 40])
                self.antecedents[arg]['grote stijging'] = fuzz.trimf(self.antecedents[arg].universe, [40, 100, 100])

            elif arg == 'LF_HF_ratio':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-5, 5, 1), 'LF_HF_ratio')
                self.antecedents[arg]['grote daling'] = fuzz.trimf(self.antecedents[arg].universe, [-5, -5, -1.25])
                self.antecedents[arg]['lichte daling'] = fuzz.trimf(self.antecedents[arg].universe, [-2, -1, 0])
                self.antecedents[arg]['constant'] = fuzz.trimf(self.antecedents[arg].universe, [-1, 0, 1])
                self.antecedents[arg]['lichte stijging'] = fuzz.trimf(self.antecedents[arg].universe, [0, 1, 2])
                self.antecedents[arg]['grote stijging'] = fuzz.trimf(self.antecedents[arg].universe, [1.25, 5, 5])

            # CRISP

            # elif arg == 'fysiologische_stressreactie':
            #     self.antecedents[arg] = ctrl.Antecedent(np.arange(0, 101, 1), 'fysiologische_stressreactie')
            #     self.antecedents[arg]['geen'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 25])
            #     self.antecedents[arg]['licht'] = fuzz.trimf(self.antecedents[arg].universe, [24, 40, 55])
            #     self.antecedents[arg]['gematigd'] = fuzz.trimf(self.antecedents[arg].universe, [54, 65, 75])
            #     self.antecedents[arg]['ernstig'] = fuzz.trimf(self.antecedents[arg].universe, [74, 100, 100])


            # FUZZY

            elif arg == 'fysiologische_stressreactie':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(0, 101, 1), 'fysiologische_stressreactie')
                self.antecedents[arg]['geen'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 30])
                self.antecedents[arg]['licht'] = fuzz.trimf(self.antecedents[arg].universe, [10, 35, 60])
                self.antecedents[arg]['gematigd'] = fuzz.trimf(self.antecedents[arg].universe, [30, 55, 80])
                self.antecedents[arg]['ernstig'] = fuzz.trimf(self.antecedents[arg].universe, [60, 100, 100])
            

            # Voor Beweging/Sport
            elif arg == 'BewegingSport':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-1, 10, 1), 'BewegingSport')
                self.antecedents[arg]['niet'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 25])
                self.antecedents[arg]['lichte inspanning'] = fuzz.trimf(self.antecedents[arg].universe, [20, 35, 50])
                self.antecedents[arg]['korte inspanning'] = fuzz.trimf(self.antecedents[arg].universe, [40, 50, 60])
                self.antecedents[arg]['training'] = fuzz.trimf(self.antecedents[arg].universe, [55, 67.5, 80])
                self.antecedents[arg]['intensief'] = fuzz.trimf(self.antecedents[arg].universe, [75, 100, 100])
                self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-1, -1, -1])

            #Voor Roken FUZZY
            elif arg == 'Roken':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-1, 30*60, 1), 'Roken')
                self.antecedents[arg]['tijdens'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 8*60])
                self.antecedents[arg]['kort_na'] = fuzz.trimf(self.antecedents[arg].universe, [3*60, 12*60, 20*60])
                self.antecedents[arg]['uitloper'] = fuzz.trimf(self.antecedents[arg].universe, [15*60, 30*60, 30*60])
                self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-1, -1, 0])
            
            # Voor Roken CRISP
            # elif arg == 'Roken':
            #     self.antecedents[arg] = ctrl.Antecedent(np.arange(-1, 30*60, 1), 'Roken')
            #     self.antecedents[arg]['tijdens'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 3*60])
            #     self.antecedents[arg]['kort_na'] = fuzz.trimf(self.antecedents[arg].universe, [2*60, 10*60, 20*60])
            #     self.antecedents[arg]['uitloper'] = fuzz.trimf(self.antecedents[arg].universe, [19*60, 30*60, 30*60])
            #     self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-1, -1, 0])
            

            # Voor Temperatuurschommeling
            elif arg == 'Temperatuurschommeling':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-6.25, 6.25, 0.25), 'Temperatuurschommeling')
                self.antecedents[arg]['kleine stijging'] = fuzz.trimf(self.antecedents[arg].universe, [0.5, 2, 4])
                self.antecedents[arg]['grote stijging'] = fuzz.trimf(self.antecedents[arg].universe, [2.5, 6.25, 6.25])
                self.antecedents[arg]['kleine daling'] = fuzz.trimf(self.antecedents[arg].universe, [-4, -2, -0.5])
                self.antecedents[arg]['grote daling'] = fuzz.trimf(self.antecedents[arg].universe, [-6.25, -6.25, -2.5])
                self.antecedents[arg]['constant'] = fuzz.trimf(self.antecedents[arg].universe, [-1, 0, 1])


            # Voor Cafeïne
            elif arg == 'Cafeïne':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-2, 120*60, 1), 'Cafeïne')
                self.antecedents[arg]['direct na inname'] = fuzz.trimf(self.antecedents[arg].universe, [0, 5*60, 10*60])
                self.antecedents[arg]['verwerkingstijd na inname'] = fuzz.trimf(self.antecedents[arg].universe, [0, 30*60, 120*60])
                self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-2, -1, 0])

            # Voor Eten - Tijd sinds maaltijd
            elif arg == 'EtenTijdSindsMaaltijd':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(0, 61*60, 1), 'EtenTijdSindsMaaltijd')
                self.antecedents[arg]['net na maaltijd'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 20*60])
                self.antecedents[arg]['kort na maaltijd'] = fuzz.trimf(self.antecedents[arg].universe, [20*60, 40*60, 60*60])
                self.antecedents[arg]['lang na maaltijd'] = fuzz.trimf(self.antecedents[arg].universe, [60*60, 61*60, 61*60])

            # Voor Acute pijn
            elif arg == 'AcutePijn':
                self.antecedents[arg] = ctrl.Antecedent(np.array([0, 1]), 'AcutePijn')
                self.antecedents[arg]['nee'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 0])
                self.antecedents[arg]['ja'] = fuzz.trimf(self.antecedents[arg].universe, [1, 1, 1])

            # Voor Alcohol - Hoeveelheid
            elif arg == 'AlcoholHoeveelheid':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(-2, 2, 1), 'AlcoholHoeveelheid')
                self.antecedents[arg]['1 consumptie'] = fuzz.trimf(self.antecedents[arg].universe, [0, 1, 2])
                self.antecedents[arg]['meer consumpties'] = fuzz.trimf(self.antecedents[arg].universe, [1, 2, 2])
                self.antecedents[arg]['geen_info'] = fuzz.trimf(self.antecedents[arg].universe, [-2, -1, 0])

            # Voor Fitheid
            elif arg == 'Fitheid':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(0, 8, 1), 'Fitheid')
                self.antecedents[arg]['laag'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 4])
                self.antecedents[arg]['gemiddeld'] = fuzz.trimf(self.antecedents[arg].universe, [2, 4, 7])
                self.antecedents[arg]['hoog'] = fuzz.trimf(self.antecedents[arg].universe, [4, 7, 7])

            # Voor Tijd na beweging/sport
            elif arg == 'TijdNaBewegingSport':
                self.antecedents[arg] = ctrl.Antecedent(np.arange(0, 181, 1), 'TijdNaBewegingSport')
                self.antecedents[arg]['meteen na sport'] = fuzz.trimf(self.antecedents[arg].universe, [0, 0, 5])
                self.antecedents[arg]['overgangsfase'] = fuzz.trimf(self.antecedents[arg].universe, [2, 16, 30])
                self.antecedents[arg]['herstelfase'] = fuzz.trimf(self.antecedents[arg].universe, [20, 90, 180])
            

    
    def get_antecedent(self):
        return self.antecedents

class FuzzyVariablesConsequents:
    def __init__(self, arg):
        self.print_manager = PrintManager()
        self.print_manager.print(None, "FuzzyVariablesConsequents", "__init__", "MAKE OBJECT", f"Consequent: {arg}")

        self.consequents = {}
        if arg == 'Intensiviteit_sport':
            self.consequents[arg] = ctrl.Consequent(np.arange(0, 100, 1), 'Intensiviteit_sport')
            self.consequents[arg]['niet'] = fuzz.trimf(self.consequents[arg].universe, [0, 0, 20])
            self.consequents[arg]['heel kort'] = fuzz.trimf(self.consequents[arg].universe, [20, 30, 40])
            self.consequents[arg]['gemiddeld'] = fuzz.trimf(self.consequents[arg].universe, [40, 50, 65])
            self.consequents[arg]['zwaar'] = fuzz.trimf(self.consequents[arg].universe, [60, 75, 100])

        elif arg == 'fysiologische_stress_niveau':
            self.consequents[arg] = ctrl.Consequent(np.arange(0, 101, 1), 'fysiologische_stress_niveau')
            self.consequents[arg]['geen'] = fuzz.trimf(self.consequents[arg].universe, [0, 0, 25])
            self.consequents[arg]['licht'] = fuzz.trimf(self.consequents[arg].universe, [20, 40, 60])
            self.consequents[arg]['gematigd'] = fuzz.trimf(self.consequents[arg].universe, [50, 70, 90])
            self.consequents[arg]['ernstig'] = fuzz.trimf(self.consequents[arg].universe, [80, 100, 100])
        
        elif arg == 'mentale_stress':
            self.consequents[arg] = ctrl.Consequent(np.arange(-2, 101, 1), 'mentale_stress')
            self.consequents[arg]['geen'] = fuzz.trimf(self.consequents[arg].universe, [0, 0, 30])
            self.consequents[arg]['lichte mentale stress'] = fuzz.trimf(self.consequents[arg].universe, [10, 35, 60])
            self.consequents[arg]['gemiddelde mentale stress'] = fuzz.trimf(self.consequents[arg].universe, [40, 65, 90])
            self.consequents[arg]['ernstige mentale stress'] = fuzz.trimf(self.consequents[arg].universe, [70, 100, 100])
            self.consequents[arg]['fysiologische component blijft behouden'] = fuzz.trimf(self.consequents[arg].universe, [-2, -1, -0])


    def get_consequent(self):
        return self.consequents
    
    def plot_consequents(self):
        for key, consequent in self.consequents.items():
            consequent.view()
        plt.show()

# Voorbeeld van het creëren en plotten van de fuzzy variabelen
if __name__ == "__main__":
    # Voorbeeld gebruik
    antecedents = FuzzyVariablesAntecedents('Hartslag_zone', 'Activiteit', leeftijd=30)
    consequents = FuzzyVariablesConsequents('IntensiviteitSport')

    # Plot de lidmaatschapsfuncties
    antecedents.plot_antecedents()
    consequents.plot_consequents()