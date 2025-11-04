from xmlParser.xmlParser import xmlParser
from machine.automaton import Automaton

GR = Automaton()
GR = Automaton.load(GR, 'NewModelingTAC/GR.xml')

# (Ha x GR)
Ha = Automaton()
Ha = Automaton.load(Ha, 'NewModelingTAC/Ha.xml')

# (Hb x GR)
# RB = Automaton()
# RB = Automaton.load(RB, 'Fischertechnik-models/Rb.xml')

S = Automaton.RobRecSup(GR,Ha, ['m2', 'm2_a'])
# print(S)
S.save('NewModelingTAC/RRS.xml')

# HbTeste = Automaton()
# HbTeste = Ha.attacked_events_remove(['m2', 'm2_a'])
# HbTeste.save('NewModelingTAC/NewTes.xml')
# print(Ha.attacked_events_remove(['m2', 'm2_a']))