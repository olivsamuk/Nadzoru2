#!/usr/bin/python

import sys

# import pluggins # this causes errors in python 3.8.9+
from machine.automaton import Automaton
from gui import Application
from cli.newDFA import new_dfa
from cli.json_parser import json_export, json_load
from cli.xml_parser import ides_export
from xmlParser.xmlParser import xmlParser
import os

def findKeys(path_sup, path_plant):
    sup = xmlParser(path_sup)
    plant = xmlParser(path_plant)

    def getControllableEventsList(model_sup):
        controllableEventsList = []
        for each_event in model_sup.events:
            if each_event.controllable:
                controllableEventsList.append(each_event)
        return controllableEventsList

    print('Controllable Events List: ', getControllableEventsList(sup))
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
                # print(each_event.name, ' (Feasible)')
                isFeasible = True

        return isFeasible
    def getControlCommands(model_sup):
        control_commands = {}
        for eachState in model_sup.states:
            state_events = []
            control_commands[eachState] = {'enablement':[], 'disablement':[], 'NotPhysicallyPossible':[]}

            for eachTransition in eachState.out_transitions:
                if eachTransition.event.controllable:
                    state_events.append(eachTransition.event)
                    control_commands[eachState]['enablement'].append(eachTransition.event.name)

            diff = set(getControllableEventsList(model_sup)) - set(state_events)

            for each_event in diff:
                control_commands[eachState]['disablement'].append(each_event.name)

                if not isPhysicallyPossible(eachState, each_event):
                    control_commands[eachState]['NotPhysicallyPossible'].append(each_event.name)

        return control_commands

    print(getControlCommands(sup))
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

    # findKeys('USER/xml/S.xml', 'USER/xml/G.xml')
    # -----------------
    cli()
    # ------------------
    # application = Application()
    # application.run(sys.argv)