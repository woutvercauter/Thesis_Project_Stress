class RuleHolder:
    def __init__(self):
        # Regeldefinities
        self.rules = [
                # Regels voor Sport

                Rule('Sport', 1, {'HR_bpm': 'zeer laag', 'Activiteit_sport': 'laag'}, {'Intensiviteit_sport': 'niet'}, "Als hartslag zeer laag, geen sport mogelijk"),
                Rule('Sport', 2, {'Activiteit_sport': 'laag', 'Poi_sport': 'laag'}, {'Intensiviteit_sport': 'niet'}, "Als activiteit laag en poi laag, geen sport mogelijk"),
                Rule('Sport', 3, {'HR_bpm': 'licht', 'Activiteit_sport': 'gemiddeld'}, {'Intensiviteit_sport': 'niet'}, "Als hartslag laag en activiteit gemiddeld, geen sport mogelijk"),
                Rule('Sport', 4, {'HR_bpm': 'licht', 'Activiteit_sport': 'laag'}, {'Intensiviteit_sport': 'niet'}, "Als hartslag laag en activiteit laag, geen sport mogelijk"),
                Rule('Sport', 6, {'BewegingSport_recent': 'niet', 'Activiteit_sport': 'laag'}, {'Intensiviteit_sport': 'niet'}),
                Rule('Sport', 7, {'HR_bpm': 'hoog', 'Activiteit_sport': 'hoog'}, {'Intensiviteit_sport': 'zwaar'}),
                Rule('Sport', 8, {'HR_bpm': 'hoog', 'BewegingSport_recent': 'zwaar'}, {'Intensiviteit_sport': 'zwaar'}),
                Rule('Sport', 9, {'HR_bpm': 'hoog', 'Poi_sport': 'hoog'}, {'Intensiviteit_sport': 'zwaar'}),
                Rule('Sport', 10, {'HR_bpm': 'drempel', 'Activiteit_sport': 'hoog'}, {'Intensiviteit_sport': 'gemiddeld'}),
                Rule('Sport', 11, {'HR_bpm': 'drempel', 'Poi_sport': 'hoog'}, {'Intensiviteit_sport': 'gemiddeld'}),
                Rule('Sport', 12, {'HR_bpm': 'drempel', 'Activiteit_sport': 'gemiddeld', 'BewegingSport_recent': 'zwaar'}, {'Intensiviteit_sport': 'gemiddeld'}),
                Rule('Sport', 13, {'HR_bpm': 'drempel', 'Activiteit_sport': 'gemiddeld', 'BewegingSport_recent': 'licht'}, {'Intensiviteit_sport': 'gemiddeld'}),
                Rule('Sport', 14, {'HR_bpm': 'drempel', 'Activiteit_sport': 'gemiddeld', 'BewegingSport_recent': 'niet'}, {'Intensiviteit_sport': 'heel kort'}),
                Rule('Sport', 15, {'HR_bpm': 'hoog', 'Activiteit_sport': 'gemiddeld', 'BewegingSport_recent': 'niet'}, {'Intensiviteit_sport': 'heel kort'}),
                Rule('Sport', 16, {'HR_bpm': 'hoog', 'Activiteit_sport': 'hoog', 'BewegingSport_recent': 'niet'}, {'Intensiviteit_sport': 'heel kort'}),
                Rule('Sport', 17, {'HR_bpm': 'drempel', 'Activiteit_sport': 'hoog', 'BewegingSport_recent': 'niet'}, {'Intensiviteit_sport': 'heel kort'}),

                # Regels voor "Lichte Stress"
                Rule('fysiologische_stressreactie', 1, {'RMSSD_delta': 'constant', 'LF_delta': 'lichte stijging', 'HF_delta': 'lichte daling', 'HFn_delta': 'lichte daling'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 2, {'RMSSD_delta': 'constant', 'LF_delta': 'lichte stijging', 'HFn_delta': 'lichte daling', 'LFn_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 3, {'RMSSD_delta': 'constant', 'HF_delta': 'lichte daling', 'HFn_delta': 'lichte daling', 'LFn_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 4, {'RMSSD_delta': 'constant', 'LF_delta': 'lichte stijging', 'HF_delta': 'lichte daling', 'LFn_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 5, {'RMSSD_delta': 'constant', 'LF_delta': 'grote stijging', 'HF_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 6, {'RMSSD_delta': 'constant', 'LF_delta': 'grote stijging', 'HFn_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 7, {'RMSSD_delta': 'constant', 'LF_delta': 'grote stijging', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 8, {'RMSSD_delta': 'constant', 'HF_delta': 'grote daling', 'HFn_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 9, {'RMSSD_delta': 'constant', 'HF_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 10, {'RMSSD_delta': 'constant', 'HFn_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 11, {'RMSSD_delta': 'lichte daling', 'LF_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 12, {'RMSSD_delta': 'lichte daling', 'LF_HF_ratio': 'lichte stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 13, {'RMSSD_delta': 'lichte daling', 'HF_delta': 'lichte daling'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 14, {'RMSSD_delta': 'lichte daling', 'HFn_delta': 'lichte daling'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 15, {'RMSSD_delta': 'lichte daling', 'LFn_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 16, {'RMSSD_delta': 'lichte daling', 'LF_delta': 'lichte daling'}, {'fysiologische_stress_niveau': 'licht'}),
                Rule('fysiologische_stressreactie', 17, {'RMSSD_delta': 'lichte daling', 'HF_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'licht'}),

                # Regels voor "Gemiddelde Stress"
                Rule('fysiologische_stressreactie', 18, {'RMSSD_delta': 'grote daling', 'LF_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 19, {'RMSSD_delta': 'grote daling', 'HF_delta': 'lichte daling'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 20, {'RMSSD_delta': 'grote daling', 'HFn_delta': 'lichte daling'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 21, {'RMSSD_delta': 'grote daling', 'LFn_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 22, {'RMSSD_delta': 'grote daling', 'LF_delta': 'lichte daling'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 23, {'RMSSD_delta': 'grote daling', 'HF_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 24, {'RMSSD_delta': 'lichte daling', 'LF_delta': 'grote stijging', 'HF_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 25, {'RMSSD_delta': 'lichte daling', 'LF_delta': 'grote stijging', 'HFn_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 26, {'RMSSD_delta': 'lichte daling', 'LF_delta': 'grote stijging', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 27, {'RMSSD_delta': 'lichte daling', 'HF_delta': 'grote daling', 'HFn_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 28, {'RMSSD_delta': 'lichte daling', 'HF_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 29, {'RMSSD_delta': 'lichte daling', 'HFn_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 30, {'RMSSD_delta': 'constant', 'LF_delta': 'grote stijging', 'HF_delta': 'grote daling', 'HFn_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 31, {'RMSSD_delta': 'constant', 'LF_delta': 'grote stijging', 'HFn_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 32, {'RMSSD_delta': 'constant', 'HF_delta': 'grote daling', 'HFn_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),
                Rule('fysiologische_stressreactie', 33, {'RMSSD_delta': 'constant', 'LF_delta': 'grote stijging', 'HF_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'gematigd'}),

                # Regels voor "Ernstige Stress"
                Rule('fysiologische_stressreactie', 34, {'RMSSD_delta': 'grote daling', 'LF_delta': 'grote stijging', 'HF_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 35, {'RMSSD_delta': 'grote daling', 'LF_delta': 'grote stijging', 'HFn_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 36, {'RMSSD_delta': 'grote daling', 'LF_delta': 'grote stijging', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 37, {'RMSSD_delta': 'grote daling', 'HF_delta': 'grote daling', 'HFn_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 38, {'RMSSD_delta': 'grote daling', 'HF_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 39, {'RMSSD_delta': 'grote daling', 'HFn_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 40, {'RMSSD_delta': 'lichte daling', 'LF_delta': 'grote stijging', 'HF_delta': 'grote daling', 'HFn_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 41, {'RMSSD_delta': 'lichte daling', 'LF_delta': 'grote stijging', 'HFn_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 42, {'RMSSD_delta': 'lichte daling', 'HF_delta': 'grote daling', 'HFn_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 43, {'RMSSD_delta': 'lichte daling', 'LF_delta': 'grote stijging', 'HF_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'ernstig'}),
                Rule('fysiologische_stressreactie', 44, {'RMSSD_delta': 'constant', 'LF_delta': 'grote stijging', 'HF_delta': 'grote daling', 'HFn_delta': 'grote daling', 'LFn_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'ernstig'}),

                # Enkel regels met 'fysiologische_stressreactie met RMSSD_delta en LF/HF_ratio

                # Rule('fysiologische_stressreactie', 45, {'RMSSD_delta': 'constant'}, {'fysiologische_stress_niveau': 'geen'}),
                # Rule('fysiologische_stressreactie', 46, {'RMSSD_delta': 'lichte stijging'}, {'fysiologische_stress_niveau': 'geen'}),
                # Rule('fysiologische_stressreactie', 47, {'RMSSD_delta': 'grote stijging'}, {'fysiologische_stress_niveau': 'geen'}),
                # Rule('fysiologische_stressreactie', 48, {'RMSSD_delta': 'lichte daling'}, {'fysiologische_stress_niveau': 'licht'}),
                # Rule('fysiologische_stressreactie', 49, {'RMSSD_delta': 'grote daling'}, {'fysiologische_stress_niveau': 'ernstig'}),

                # Rule('fysiologische_stressreactie', 50, {'LF_HF_ratio': 'constant'}, {'fysiologische_stress_niveau': 'geen'}),
                # Rule('fysiologische_stressreactie', 51, {'LF_HF_ratio': 'lichte stijging'}, {'fysiologische_stress_niveau': 'licht'}),
                # Rule('fysiologische_stressreactie', 52, {'LF_HF_ratio': 'grote stijging'}, {'fysiologische_stress_niveau': 'ernstig'}),
                # Rule('fysiologische_stressreactie', 53, {'LF_HF_ratio': 'lichte daling'}, {'fysiologische_stress_niveau': 'geen'}),
                # Rule('fysiologische_stressreactie', 54, {'LF_HF_ratio': 'grote daling'}, {'fysiologische_stress_niveau': 'geen'}),
                

                #Beweging/Sport
                Rule('mentale_stress', 1, {'fysiologische_stressreactie': 'licht', 'BewegingSport': 'lichte inspanning'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 2, {'fysiologische_stressreactie': 'licht', 'BewegingSport': 'korte inspanning'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 3, {'fysiologische_stressreactie': 'licht', 'BewegingSport': 'training'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 4, {'fysiologische_stressreactie': 'licht', 'BewegingSport': 'intensief'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 5, {'fysiologische_stressreactie': 'gematigd', 'BewegingSport': 'korte inspanning'}, {'mentale_stress': 'lichte mentale stress'}),
                Rule('mentale_stress', 6, {'fysiologische_stressreactie': 'gematigd', 'BewegingSport': 'training'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 7, {'fysiologische_stressreactie': 'gematigd', 'BewegingSport': 'intensief'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 8, {'fysiologische_stressreactie': 'ernstig', 'BewegingSport': 'training'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 9, {'fysiologische_stressreactie': 'ernstig', 'BewegingSport': 'intensief'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 10, {'fysiologische_stressreactie': 'ernstig', 'BewegingSport': 'korte inspanning'}, {'mentale_stress': 'gemiddelde mentale stress'}),

                #Roken
                Rule('mentale_stress', 11, {'fysiologische_stressreactie': 'licht', 'Roken': 'tijdens'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 12, {'fysiologische_stressreactie': 'licht', 'Roken': 'kort_na'}, {'mentale_stress': 'geen'}),
                # Rule('mentale_stress', 13, {'fysiologische_stressreactie': 'licht', 'Roken': 'uitloper'}, {'mentale_stress': 'fysiologische component blijft behouden'}),
                Rule('mentale_stress', 13, {'fysiologische_stressreactie': 'gematigd', 'Roken': 'kort_na'}, {'mentale_stress': 'geen'}),
                # Rule('mentale_stress', 14, {'fysiologische_stressreactie': 'gematigd', 'Roken': 'tijdens'}, {'mentale_stress': 'fysiologische component blijft behouden'}),
                # Rule('mentale_stress', 15, {'fysiologische_stressreactie': 'gematigd', 'Roken': 'uitloper'}, {'mentale_stress': 'fysiologische component blijft behouden'}),
                # Rule('mentale_stress', 16, {'fysiologische_stressreactie': 'ernstig', 'Roken': 'kort_na'}, {'mentale_stress': 'gemiddelde mentale stress'}),
                # Rule('mentale_stress', 17, {'fysiologische_stressreactie': 'ernstig', 'Roken': 'tijdens'}, {'mentale_stress': 'fysiologische component blijft behouden'}),
                # Rule('mentale_stress', 18, {'fysiologische_stressreactie': 'ernstig', 'Roken': 'uitloper'}, {'mentale_stress': 'fysiologische component blijft behouden'}),

                Rule('mentale_stress', 14, {'fysiologische_stressreactie': 'licht', 'Roken': 'tijdens'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 15, {'fysiologische_stressreactie': 'licht', 'Roken': 'kort_na'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 16, {'fysiologische_stressreactie': 'licht', 'Roken': 'uitloper'}, {'mentale_stress': 'lichte mentale stress'}),
                Rule('mentale_stress', 17, {'fysiologische_stressreactie': 'gematigd', 'Roken': 'kort_na'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 18, {'fysiologische_stressreactie': 'gematigd', 'Roken': 'tijdens'}, {'mentale_stress': 'gemiddelde mentale stress'}),
                Rule('mentale_stress', 19, {'fysiologische_stressreactie': 'gematigd', 'Roken': 'uitloper'}, {'mentale_stress': 'gemiddelde mentale stress'}),
                Rule('mentale_stress', 20, {'fysiologische_stressreactie': 'ernstig', 'Roken': 'kort_na'}, {'mentale_stress': 'gemiddelde mentale stress'}),
                # Rule('mentale_stress', 21, {'fysiologische_stressreactie': 'ernstig', 'Roken': 'tijdens'}, {'mentale_stress': 'ernstige mentale stress'}),
                # Rule('mentale_stress', 22, {'fysiologische_stressreactie': 'ernstig', 'Roken': 'uitloper'}, {'mentale_stress': 'ernstige mentale stress'}),

                # Cafeïne
                Rule('mentale_stress', 21, {'fysiologische_stressreactie': 'licht', 'Cafeïne': 'direct na inname'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 22, {'fysiologische_stressreactie': 'licht', 'Cafeïne': 'verwerkingstijd na inname'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 23, {'fysiologische_stressreactie': 'gematigd', 'Cafeïne': 'direct na inname'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 24, {'fysiologische_stressreactie': 'gematigd', 'Cafeïne': 'verwerkingstijd na inname'}, {'mentale_stress': 'lichte mentale stress'}),
                Rule('mentale_stress', 25, {'fysiologische_stressreactie': 'ernstig', 'Cafeïne': 'direct na inname'}, {'mentale_stress': 'gemiddelde mentale stress'}),

                # Temperatuur - Temperatuurschommeling
                Rule('mentale_stress', 26, {'fysiologische_stressreactie': 'licht', 'Temperatuurschommeling': 'kleine daling'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 27, {'fysiologische_stressreactie': 'licht', 'Temperatuurschommeling': 'kleine stijging'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 28, {'fysiologische_stressreactie': 'licht', 'Temperatuurschommeling': 'grote daling'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 29, {'fysiologische_stressreactie': 'licht', 'Temperatuurschommeling': 'grote stijging'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 30, {'fysiologische_stressreactie': 'gematigd', 'Temperatuurschommeling': 'grote stijging'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 31, {'fysiologische_stressreactie': 'gematigd', 'Temperatuurschommeling': 'grote daling'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 32, {'fysiologische_stressreactie': 'gematigd', 'Temperatuurschommeling': 'kleine stijging'}, {'mentale_stress': 'lichte mentale stress'}),
                Rule('mentale_stress', 33, {'fysiologische_stressreactie': 'gematigd', 'Temperatuurschommeling': 'kleine daling'}, {'mentale_stress': 'lichte mentale stress'}),
                Rule('mentale_stress', 34, {'fysiologische_stressreactie': 'ernstig', 'Temperatuurschommeling': 'grote stijging'}, {'mentale_stress': 'gemiddelde mentale stress'}),
                Rule('mentale_stress', 35, {'fysiologische_stressreactie': 'ernstig', 'Temperatuurschommeling': 'grote daling'}, {'mentale_stress': 'gemiddelde mentale stress'}),

                # Alcohol - Hoeveelheid
                Rule('mentale_stress', 36, {'fysiologische_stressreactie': 'licht', 'AlcoholHoeveelheid': '1 consumptie'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 37, {'fysiologische_stressreactie': 'licht', 'AlcoholHoeveelheid': 'meer consumpties'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 38, {'fysiologische_stressreactie': 'gematigd', 'AlcoholHoeveelheid': 'meer consumpties'}, {'mentale_stress': 'geen'}),
                Rule('mentale_stress', 39, {'fysiologische_stressreactie': 'ernstig', 'AlcoholHoeveelheid': 'meer consumpties'}, {'mentale_stress': 'geen'}),

                # fysiologische stress blijft behouden.
                Rule('mentale_stress', 40, {'fysiologische_stressreactie': 'geen'}, {'mentale_stress': 'fysiologische component blijft behouden'}),
                Rule('mentale_stress', 41, {'fysiologische_stressreactie': 'licht', 'BewegingSport': 'niet', 'Roken': 'uitloper', 'Temperatuurschommeling': 'constant'}, {'mentale_stress': 'fysiologische component blijft behouden'}),
                Rule('mentale_stress', 42, {'fysiologische_stressreactie': 'gematigd', 'BewegingSport': 'niet', 'Roken': 'uitloper', 'Temperatuurschommeling': 'constant'}, {'mentale_stress': 'fysiologische component blijft behouden'}),
                Rule('mentale_stress', 43, {'fysiologische_stressreactie': 'ernstig', 'BewegingSport': 'niet', 'Roken': 'uitloper', 'Temperatuurschommeling': 'constant'}, {'mentale_stress': 'fysiologische component blijft behouden'})  

]


            #to crisp: niet aan het sporten, niet aan het lopen,...

    def get_rules(self, rule_type):
        return [rule for rule in self.rules if rule.rule_type == rule_type]

class Rule:
    def __init__(self, rule_type, number, antecedents, consequent, comment=None):
        self.rule_type = rule_type
        self.number = number
        self.antecedents = antecedents
        self.consequent = consequent
        self.comment = comment

