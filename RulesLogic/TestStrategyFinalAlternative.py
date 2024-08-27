from abc import ABC, abstractmethod
import skfuzzy.control as ctrl
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
from skfuzzy.control import ControlSystem, Antecedent, Consequent, Rule, ControlSystemSimulation
import sys
import os

# Bepaal de huidige directory van dit script
current_dir = os.path.dirname(os.path.abspath(__file__))
# Ga één directory omhoog naar de project root
project_root = os.path.abspath(os.path.join(current_dir, '..'))
# Voeg de project_root directory toe aan sys.path als het er nog niet in zit
if project_root not in sys.path:
    sys.path.append(project_root)

from RulesLogic.RuleHolderB import RuleHolder
from RulesLogic.SetBase import FuzzyVariablesAntecedents, FuzzyVariablesConsequents
from utilities import PrintManager

# Definieer een abstracte klasse voor de strategieën die de basis legt voor alle strategieën
class Strategy(ABC):
    @abstractmethod
    def execute(self, **kwargs):
        # Deze methode moet worden geïmplementeerd door subklassen en wordt gebruikt om de strategie uit te voeren
        pass

    @abstractmethod
    def set_attributes(self, type, consequent, *antecedents, **extra_info):
        # Deze methode moet worden geïmplementeerd door subklassen en stelt de attributen van de strategie in
        pass

class FuzzyStrategy(Strategy):
    
    def set_attributes(self, type, consequent, *antecedents, **extra_info):
        # Initialiseert de fuzzy strategy met de gegeven type, consequent en antecedenten
        self.print_manager = PrintManager()
        self.type = type
        self.antecedents = antecedents
        self.consequent = consequent
        # Zet de basis voor antecedenten en consequenten
        self.antecedents_base = FuzzyVariablesAntecedents(*antecedents, **extra_info).get_antecedent()
        self.consequent_base = FuzzyVariablesConsequents(consequent).get_consequent()
        # Initialiseer een fuzzy regelgenerator
        self.fuzzyRulesGenerator = FuzzyRules(type, self.antecedents_base, self.consequent_base)
        self.base = self.fuzzyRulesGenerator.get_rulebase()  # Haalt de regels op die bij de strategie horen

    def execute(self, **antecedent_values):
        # Voert de fuzzy strategy uit met de gegeven waarden voor de antecedenten
        # Maak een regelsysteem op basis van de regelbasis
        control_system = ctrl.ControlSystemSimulation(self.base)
        input_values = {}
        # Voeg de inputwaarden toe aan het controlesysteem
        for antecedent_name, value in antecedent_values.items():
            try:
                input_values[antecedent_name] = value
                if value is not None:
                    control_system.input[antecedent_name] = value
            except ValueError as e:
                print(control_system.input)
                  
        # Voer het controlesysteem uit om de consequenten te berekenen
        try:
            control_system.compute()

            # Haal de resultaten op van de consequents
            output = control_system.output[self.consequent]

            # Verzamel de regels die hebben bijgedragen aan de output
            relevant_rules = {}
            regels = self.base.rules
            i = 1
            
            for regel in regels:
                waarheidregel = regel.aggregate_firing[control_system]
                if waarheidregel != 0:
                    relevant_rules[i] = waarheidregel
                i += 1

            return Result(self.type, output, input_values, relevant_rules)
        
        except ValueError as ve:
            if 'Crisp output cannot be calculated' in str(ve):
                # Foutafhandeling voor als er geen duidelijke output kan worden berekend
                self.print_manager.print(self.type, "FuzzyStrategy", "execute", "ERROR", "Fout: Het systeem is te dun bezet om een crisp output te berekenen. Controleer of elke Antecedent ten minste één verbonden Term activeert via de huidige set Rules.")
                self.print_manager.print(self.type, "FuzzyStrategy", "execute", "CRITICAL", f"Input was: {input_values}")
                return None
            else:
                raise ve  # Gooi de fout opnieuw als het een andere ValueError is
        except AssertionError as ae:
            if 'Total area is zero in defuzzification' in str(ae):
                # Foutafhandeling voor als het totale gebied nul is tijdens defuzzificatie
                self.print_manager.print(self.type, "FuzzyStrategy", "execute", "ERROR", "Fout: Het totale gebied is nul tijdens defuzzificatie! Controleer of de regels correct zijn ingesteld en dat er voldoende inputs zijn.")
                self.print_manager.print(self.type, "FuzzyStrategy", "execute", "CRITICAL", f"Input was: {input_values}")
                return None
            else:
                raise ae  # Gooi de fout opnieuw als het een andere AssertionError is

class Result:
    def __init__(self, type, output, input_values, relevant_rules, success=True):
        # Initialiseer de Result klasse met type, output, inputwaarden en relevante regels
        self.type = type
        self.output = output
        self.input_values = input_values
        self.relevant_rules = relevant_rules
        self.print_manager = PrintManager()
        self.print_manager.print(self.type, "FuzzyStrategy", "Result", "MAKE OBJECT", f"Output: {self.output}, Input values: {self.input_values},  Relevant rules: {self.relevant_rules}")

        # SCHRIJF DE RESULTATEN NAAR BESTAND
        if success:
            with open("fuzzy_results.txt", "a") as file:
                file.write(f"{self.type} - {self.output} - {self.input_values} - {self.relevant_rules}\n")
        else:
            with open("fuzzy_errors.txt", "a") as file:
                file.write(f"{self.type} - {self.output} - {self.input_values} - {self.relevant_rules}\n")

        # Sluit het bestand
        file.close()

class FuzzyRules:
    def __init__(self, type, antecedents, consequents):
        # Initialiseer de FuzzyRules klasse met type, antecedenten en consequenten
        self.fuzzy_rules = []  # Een array om de fuzzy regels op te slaan
        self.fuzzy_vars_ant = antecedents
        self.fuzzy_vars_cons = consequents
        self.holder = RuleHolder()  # Regelhouder wordt later geïnjecteerd
        self.text_rules = self.holder.get_rules(type)
        self.convert_rules()
    
    def convert_rules(self):
        # Converteer tekstuele regels naar fuzzy regels
        for rule in self.text_rules:
            comment = rule.comment

            key, value = list(rule.consequent.items())[0]
            consequent = self.fuzzy_vars_cons[key][value]

            # Bouw de uitdrukking voor antecedenten op
            antecedents_terms = []
            for (key, value) in rule.antecedents.items():
                try:
                    antecedents_terms.append(self.fuzzy_vars_ant[key][value])
                except KeyError as e:
                    PrintManager().print(self.__class__.__name__, "FuzzyRuleProcessor", "process_rule", "WARNING", f"KeyError voor antecedent '{key}' met waarde '{value}': {str(e)}")
                    continue
                
            antecedents = antecedents_terms[0]  # Start met het eerste element

            # Voeg dynamisch de &-operator toe tussen elk element in antecedents_terms
            for term in antecedents_terms[1:]:
                antecedents &= term

            regel = ctrl.Rule(antecedents, consequent, comment)
            self.fuzzy_rules.append(regel)
    
    def get_rulebase(self):
        # Retourneer het regelsysteem (regelbasis) gebaseerd op fuzzy regels
        return ctrl.ControlSystem(self.fuzzy_rules)

# Voorbeeld gebruik
# fuzzy_strategy = FuzzyStrategy()
# input = ['fysiologische_stressreactie', 'BewegingSport', 'Roken', 'Cafeïne', 'Temperatuurschommeling', 'AlcoholHoeveelheid']

# fuzzy_strategy.set_attributes('mentale_stress', 'mentale_stress', *input, leeftijd=35)
# result = fuzzy_strategy.execute(fysiologische_stressreactie=70, BewegingSport=10, Roken=18*59, Cafeïne=0,
#             Temperatuurschommeling=-3, AlcoholHoeveelheid=-1)

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# Aannemende dat FuzzyStrategy en bijbehorende klassen al eerder zijn gedefinieerd...

def visualiseer_fuzzy_model(fuzzy_strategy, var1_naam, var2_naam, output_naam, var1_bereik, var2_bereik):
    # Maak een meshgrid voor de twee variabelen
    var1_waarden = np.linspace(var1_bereik[0], var1_bereik[1], 25)
    var2_waarden = np.linspace(var2_bereik[0], var2_bereik[1], 25)
    var1_grid, var2_grid = np.meshgrid(var1_waarden, var2_waarden)

    # Bereid een lege grid voor de output voor
    output_grid = np.zeros_like(var1_grid)

    # Bereken de fuzzy logica output voor elke combinatie van var1 en var2
    for i in range(var1_grid.shape[0]):
        for j in range(var1_grid.shape[1]):
            input_waarden = {
                var1_naam: var1_grid[i, j],
                var2_naam: var2_grid[i, j],
                # 'Temperatuurschommeling' : 0,  # Standaardwaarde voor andere inputs
                # 'Cafeïne': 0,
                # 'BewegingSport': 0,
                # 'AlcoholHoeveelheid': 0
            }
            output = fuzzy_strategy.execute(**input_waarden).output
            if output < 0:
                output = var2_grid[i, j]
            output_grid[i, j] = output

    # Maak een 3D-plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot het oppervlak
    ax.plot_surface(var1_grid, var2_grid, output_grid, cmap='viridis')

    # Stel plotlabels en titel in
    # ax.set_xlabel('tijd na roken (min)')
    # ax.set_ylabel('fysiologische stressreactie (waarde 0-100)')
    # ax.set_zlabel('mentale stress')
    # ax.set_title(f'Kans op mentale stress in functie van roken en de fysiologische stressreactie')

    # Labels in het Engels
    ax.set_xlabel('Time after smoking (min)')
    ax.set_ylabel('Physiological stress response (value 0-100)')
    ax.set_zlabel('Mental stress')
    ax.set_title(f'Chance of mental stress as a function of smoking and the physiological stress response')

    plt.show()

# Voorbeeld
# fuzzy_strategy = FuzzyStrategy()
# input_vars = ['fysiologische_stressreactie', 'Roken']
# fuzzy_strategy.set_attributes('mentale_stress', 'mentale_stress', *input_vars, leeftijd=35)

# Visualiseer fysiologische_stressreactie (0-100) en Roken (0 tot 30 minuten)
# visualiseer_fuzzy_model(fuzzy_strategy, 
#                       var2_naam='fysiologische_stressreactie', 
#                       var1_naam='Roken', 
#                       output_naam='mentale_stress', 
#                       var2_bereik=(0, 100), 
#                       var1_bereik=(0, 30))
