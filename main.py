#!/usr/bin/python

import sys

# import pluggins # this causes errors in python 3.8.9+
from machine.automaton import Automaton
# from gui import Application #Problem with gi (windows)
from cli.newDFA import new_dfa
from cli.json_parser import json_export, json_load
from cli.xml_parser import ides_export
from xmlParser.xmlParser import xmlParser
import os

def getControlCommands(sup, plant):
    def getControllableEventsList(model_sup):
        controllableEventsList = []
        for each_event in model_sup.events:
            if each_event.controllable:
                controllableEventsList.append(each_event)
        return controllableEventsList
    def isPhysicallyPossible(sup_state, event):
        plant_state_name = sup_state.name.replace('(', '').replace(')', '').split(',')[0]

        state_events = []
        for eachState in plant.states:
            if eachState.name == plant_state_name:
                for eachTransition in eachState.out_transitions:
                    state_events.append(eachTransition.event)

        isFeasible = False
        for each_event in state_events:
            if each_event.name == event.name:
                isFeasible = True

        return isFeasible

    # MAIN
    control_commands = {}
    for eachState in sup.states:
        state_events = []
        control_commands[eachState] = {'enablement':[], 'disablement':[], 'NotPhysicallyPossible':[]}

        for eachTransition in eachState.out_transitions:
            if eachTransition.event.controllable:
                state_events.append(eachTransition.event)
                control_commands[eachState]['enablement'].append(eachTransition.event.name)

        diff = set(getControllableEventsList(sup)) - set(state_events)

        for each_event in diff:
            if isPhysicallyPossible(eachState, each_event):
                control_commands[eachState]['disablement'].append(each_event.name)
            else:
                control_commands[eachState]['NotPhysicallyPossible'].append(each_event.name)

    return control_commands

def isMonoalphabeticCypherProtectable(path_sup, path_plant, damagingEvents):
    sup = xmlParser(path_sup)
    plant = xmlParser(path_plant)

    control_commands = getControlCommands(sup, plant)
    controls = []
    for each_state, each_control_command in control_commands.items():
        if any(event in each_control_command['disablement'] for event in damagingEvents):
            transitions = {'to_an_unsafe_state':[], 'to_a_safe_state':[]}
            plant_state_name = each_state.name.replace('(', '').replace(')', '').split(',')[0]
            plant_state = None
            # Get state from plant
            for each_plant_state in plant.states:
                if each_plant_state.name == plant_state_name:
                    plant_state = each_plant_state
                    for each_transition in plant_state.out_transitions:
                        if each_transition.to_state.diagnoser_bad:
                            transitions['to_an_unsafe_state'].append(each_transition)
                        else:
                            transitions['to_a_safe_state'].append(each_transition)

            if len(transitions['to_an_unsafe_state']) <= len(transitions['to_a_safe_state']):
                controls.append(True)
            else:
                controls.append(False)

    if False not in controls:
        return True
    else:
        return False

def cli():
    while True:
        print('Choose an option:')
        print('0 - Create | 1 - Show Automata | 2 - Quit')

        try:
            var_input = int(input())
            if var_input != 0 and var_input != 1 and var_input != 2:
                raise ValueError('Not valid')
        except ValueError as e:
            print(e)
            continue

        # DFA CREATION CONTROLLER
        if var_input == 0:
            try:
                var_input = input('Enter the DFA name: ')
            except ValueError:
                print('Empty')
                continue
            DFA = new_dfa()
            print(var_input, ": ", DFA)
            json_export(DFA, var_input)

            while True:
                try:
                    ides_export_confirm = input('Want to export to IDES? (y/n*)')
                    if len(ides_export_confirm) > 0 and ides_export_confirm != 'y': raise ValueError('Invalid Option')
                except ValueError as error:
                    print(error)
                    continue
                else:
                    if ides_export_confirm == 'y':
                        ides_export(DFA, var_input)
                        break
                    else:
                        break

        # DFA SHOW CONTROLLER
        elif var_input == 1:
            dir_list = os.listdir('USER/json/')
            while True:
                try:
                    user_dfa = str(input('Enter the DFA name: '))
                    if user_dfa+".json" not in dir_list: raise ValueError('DFA NOT FOUND!')
                except ValueError as error:
                    print(error, '\n'*2)
                    break
                else:
                    DFA = json_load(user_dfa)
                    print(user_dfa, ": ", DFA)
                    break
        # Parallel Composition
        elif var_input == 2:
            break

        # ANY OTHER OPTION
        else:
            break

if __name__ == '__main__':
    print(isMonoalphabeticCypherProtectable('USER/xml/S.xml', 'USER/xml/G.xml', ['P_on', 'V_close']))
    # a = getControlCommands('USER/xml/S.xml', 'USER/xml/G.xml')
    # print(a)
    # -----------------
    # cli()
    # ------------------
    # application = Application()
    # application.run(sys.argv)