
from dataclasses import dataclass, field

from typing import List


# Define state description
@dataclass
class stateDescription:
    stateName: str
    preRequisite: List[str] = field(default_factory=list)
    postRequisite: List[str] = field(default_factory=list)
    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.stateName == other.stateName and self.preRequisite == other.preRequisite and self.postRequisite == other.postRequisite

    def __hash__(self):
        return hash((self.stateName, tuple(self.preRequisite), tuple(self.postRequisite)))

# State descriptions
Start = stateDescription("Start",
                         ["None"],
                         ["Nav", "Listen"])

Nav = stateDescription("Nav",
                       ["Pick", "Audio Output", "Look For", "Look For wh"],
                       ["Look For", "Place", "Audio Output"])
Nav1 = stateDescription("Nav",
                       ["Pick", "Audio Output", "Look For"],
                       ["Look For", "Place", "Audio Output"])
Nav2 = stateDescription("Nav",
                       ["Pick", "Audio Output", "Look For"],
                       ["Look For", "Place", "Audio Output"])
Nav3 = stateDescription("Nav",
                       ["Pick", "Audio Output", "Look For"],
                       ["Look For", "Place", "Audio Output"])
LookFor_wh = stateDescription("Look For wh",
                           ["Start"],
                           ["Nav","Listen"])

LookFor = stateDescription("Look For",
                           ["Nav"],
                           ["Pick", "Place", "Nav"])

Pick = stateDescription("Pick",
                        ["Look For"],
                        ["Nav"])

Place = stateDescription("Place",
                         ["Nav", "Look For"],
                         ["End"])

Listen = stateDescription("Listen",
                          ["Start", "Audio Output"],
                          ["Look For", "Audio Output"])

AudioOutput = stateDescription("Audio Output",
                               ["Listen", "Nav", "Look For"],
                               ["Nav", "End"])
AudioOutput1 = stateDescription("Audio Output",
                               ["Listen", "Nav", "Look For"],
                               ["Nav", "End"])
AudioOutput2 = stateDescription("Audio Output",
                               ["Listen", "Nav", "Look For"],
                               ["Nav", "End"])

# Follow = stateDescription("Follow",
#                           ["Audio Output"],
#                           ["End"])

End = stateDescription("End",
                       ["Place", "Audio Output"],   # remove follow for now
                       ["None"])

def state_ordering(states):
    choices = [End]
    # print(choices[-1].preRequisite)
    states_left = states
    for state in states:
        # print(choices[-1].preRequisite)
        if state.stateName in choices[-1].preRequisite:
            choices.insert(0, state)
    #         states_left.remove(state)
    # for state in states:
    #     for state2 in states:
    #         if state2.stateName in state.preRequisite:
    #             choices.append([state2.stateName, state.stateName])
    #             states_left.remove(state)
    #             states_left.remove(state2)
    #
    # for choice in choices:
    #     for state in choice[0]:
    #         for state2 in states:
    #             if state2.stateName in state.preRequisite:
    #                 if state.stateName == choice[1] and state2.stateName == choice[0]:

    choices_names = [x.stateName for x in choices]
    print(choices_names)


        # for postReq in state.postRequisite:
        #     if postReq not in [x.stateName for x in states]:
        #         raise Exception(f"Post-requisite {postReq} for {state.stateName} not found in states")


def find_state_pairs(states):
    all_choices = []  # Step 1: Initialize a list to hold all possible choice lists.

    def add_state_to_choices(choices, state):
        new_choices = choices.copy()
        new_choices.insert(0, state)
        return new_choices

    for state in states:  # Step 2: Iterate through the states.
        if state.stateName in End.preRequisite:  # Check if the state is a prerequisite for End.
            choices = [End]  # Start a new choice list with End.
            choices = add_state_to_choices(choices, state)  # Add the found state to the new choice list.
            all_choices.append(choices)  # Add the new choice list to the main list.

            # Step 4: Check if the found state has its own prerequisites.
            for preReq in state.preRequisite:
                for inner_state in states:
                    if inner_state.stateName == preReq:
                        # Step 5: For each matching prerequisite, create a new list and insert the matching state.
                        updated_choices = add_state_to_choices(choices, inner_state)
                        all_choices.append(updated_choices)  # Add the updated list to the main list.

    return all_choices

# Usage
# states = [Start, Nav, LookFor_wh, LookFor, Listen, AudioOutput, End]


def find_possible_chains_backwards(states, end_state):
    all_chains = []

    def can_precede(state, next_state):
        # Check if state can precede next_state based on prerequisites
        return next_state.stateName in state.postRequisite

    def build_chain_backwards(current_chain, visited_states):
        current_state = current_chain[0]
        if not current_state.preRequisite or current_state.preRequisite == ["None"]:
            all_chains.append(current_chain[::-1])  # Reverse the chain to start from the beginning
            return
        for state in states:
            if state not in visited_states and can_precede(state, current_state):
                build_chain_backwards([state] + current_chain, visited_states | {state})

    build_chain_backwards([end_state], {end_state})
    return all_chains


def find_specific_chain(states, end_state):
    final_chain = [end_state]  # Start with the end state
    used_indices = []
    def can_precede(state, next_state):
        # Check if state can precede next_state based on prerequisites
        return next_state.stateName in state.postRequisite and state.stateName in next_state.preRequisite

    while True:
        found = False
        for i in range(len(states)-1, -1, -1):
            state = states[i]
            if i not in used_indices and can_precede(state, final_chain[0]):
                final_chain.insert(0, state)
                used_indices.append(i)
                found = True
                break
        if not found:
            break  # Exit the loop if no preceding state is found

    return final_chain

# Convert the chains to readable format (list of state names)
def chains_to_readable_format(chains):
    return [state.stateName for state in chains]




# Convert the chains to readable format (list of state names)
# def chains_to_readable_format(chains):
#     return [[state.stateName for state in chain] for chain in chains]





if __name__ == "__main__":
    # There is a person at the storage rack, their request is: tell me how many
    # foods there are on the pantry
    # start -> lookfor_wh -> nav -> AudioOutput -> Listen -> AudioOutput -> nav -> lookfor(count) -> nav(to person) -> AudioOutput ->end
    # state_ordering(states)


    # states = [Start, Nav, Nav, Nav, LookFor_wh, LookFor, Listen, AudioOutput, AudioOutput, End]
    # all_possible_choices = find_state_pairs(states)
    # for choice_list in all_possible_choices:
    #     print([state.stateName for state in choice_list])

    # # Usage
    # states = [Start, Nav1, Nav2, Nav3, LookFor_wh, LookFor, Listen, AudioOutput1, AudioOutput2, End]
    # end_state = End
    # all_possible_chains_backwards = find_possible_chains_backwards(states, end_state)
    # readable_chains_backwards = chains_to_readable_format(all_possible_chains_backwards)
    # for chain in readable_chains_backwards:
    #     print(chain)


    # Usage
    states = [Start, LookFor_wh, Nav, AudioOutput, Listen, AudioOutput, Nav, LookFor, Nav, AudioOutput, End]
    # states = [Start, Nav, Nav, Nav, LookFor_wh, LookFor, Listen, AudioOutput, AudioOutput, End]
    end_state = End
    specific_chain = find_specific_chain(states, end_state)
    readable_chain = chains_to_readable_format(specific_chain)
    print(readable_chain)
