def getSuffix(n):
    if n < 0: raise Exception("Ordinal negative numbers are not allowed")
    if n % 100 in [11, 12, 13]: return 'th'
    if n % 10 == 1: return 'st'
    if n % 10 == 2: return 'nd'
    if n % 10 == 3: return 'rd'
    return 'th'

def new_dfa():
    name = {"events":[],"states":[],"transitions":[]}
    events_set = new_events_set(name)
    states_set = new_states_set(name)
    transitions_set = new_transitions_set(name)

    name['events'] = events_set
    name['states'] = states_set
    name['transitions'] = transitions_set

    return name

def new_events_set(name):
    events_count = 0
    while(True):
        print("Enter the ", events_count + 1, getSuffix(events_count + 1),"event:")
        try:
            if events_count == 0:
                var_input = str(input())
            else:
                var_input = str(input('Event label: (-1 to quit) '))
            if not var_input or (var_input == '-1' and events_count == 0):
                raise ValueError('Not valid')
        except ValueError as x:
            print(x)
            continue
        else:
            if var_input != '-1' or '':
                event = {}
                event['id'] = events_count
                event['label'] = var_input
            else:
                break

        try:
            var_input = int(input('Controllable? 0 - False | 1 = True '))
            if var_input != 0 and var_input != 1:
                raise ValueError('Not the right data type')
        except ValueError as y:
            print(y)
            continue
        else:
            pass
        event['controllable'] = True if var_input == 1 else False

        try:
            var_input = int(input('Observable? 0 - False | 1 = True '))
            if var_input != 0 and var_input != 1:
                raise ValueError('Not the right data type')
        except ValueError as z:
            print(z)
            continue
        else:
            pass

        event['observable'] = True if var_input == 1 else False
        events_count += 1
        name['events'].append(event)

    print('\n' * 20)
    return name['events']

def new_states_set(name):
    states_count = 0
    print("Lets create the states set. It'll be numbered (0,1,2,3...)")
    print('The initial state is 0')
    try:
        var_input = int(input('Enter the total number of states: '))
    except ValueError as x:
        print(x)
    else:
        for i in range(var_input):
            state = {}
            state['id'] = states_count
            state['label'] = states_count
            state['initial'] = True if states_count == 0 else False
            name["states"].append(state)
            states_count += 1

    # Getting the list of marked states
    print('\n'*20)
    number_of_mstates = 0
    m_states_list = []
    all_states_id = []
    for each_state in name['states']:
        all_states_id.append(each_state['id'])
    while True:
        if len(name['states']) == len(m_states_list): break
        try:
            print("Enter the", number_of_mstates+1, getSuffix(number_of_mstates+1), "marked state")
            var_input = int(input())
            if var_input == -1:
                break
            elif var_input not in all_states_id: raise ValueError('Invalid State')
        except ValueError as x:
            print(x)
            continue
        else:
            m_states_list.append(var_input)
            number_of_mstates+=1
            all_states_id.remove(var_input)
    for state in name["states"]:
        state['marked'] = True if int(state['id']) in m_states_list else False

    return name['states']

def new_transitions_set(name):
    print('\n' * 20)
    transitions_count = 0
    print("Lets create the transitions!")
    while True:
        transition = {}
        print("Enter the", transitions_count + 1, getSuffix(transitions_count + 1), "transition: ")
        print('\n')

        # DEFINE EXIT STATE
        all_states_id = []
        for each_state_id in name['states']:
            all_states_id.append(each_state_id['id'])
        try:
            var_input = int(input('Exit state: '))
            if var_input == -1: break
            if var_input not in all_states_id: raise ValueError('Invalid State')
        except ValueError as x:
            print(x)
            continue
        else:
            transition = {}
            transition['id'] = transitions_count
            transition['source'] = var_input

            # DEFINE TARGET
            try:
                var_input = int(input('Entrance state: '))
                if var_input not in all_states_id: raise ValueError('Invalid State')
            except ValueError as z:
                print(z)
                continue
            else:
                transition['target'] = var_input

            # DEFINE EVENT
            all_events_label = []
            for each_event_label in name['events']:
                all_events_label.append(each_event_label['label'])
            print(all_events_label)
            try:
                var_input = input('Event Label: ')
                if var_input not in all_events_label: raise ValueError('empty string')
            except ValueError as y:
                print(y)
                continue
            else:
                for each_event in name['events']:
                    if each_event['label'] == str(var_input):
                        transition['event'] = each_event['id']


            transitions_count += 1
            name['transitions'].append(transition)
    return name['transitions']