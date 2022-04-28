from automaton import Automaton

G = Automaton()
G.ides_import('SLOC5_R.xmd')

controllable    = [each_transition for each_state in G.states for each_transition in each_state.out_transitions if each_transition.event.controllable]
uncontrollable  = [each_transition for each_state in G.states for each_transition in each_state.out_transitions if each_transition.event.controllable == False]
disabled        = [(each_state, each_event.name) for each_state in G.states for each_event in G.event_name_map().values() if each_event not in [item.event for item in each_state.out_transitions] and each_event.controllable == True]

# [print(each_transition) for each_transition in uncontrollable]
# [print(each_transition) for each_transition in controllable]
# print(disabled)

# print(len(uncontrollable), "transitions with uncontrollable events", '\n', len(controllable), "transitions with controllable events")