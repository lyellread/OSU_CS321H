#!/usr/bin/env python3

import json
import os
import sys


def check_parse_file(filename):

    """
    This function will read from the JSON file, and
    parse the input. It checks, using assertions, that
    the DPDA meets certain requirements.

    Arguments: A full path to the JSON to parse
    Returns: A dictionary containing the parsed JSON DPDA
    """

    with open(filename) as f:
        dpda_dict = json.loads(f.read())

    try:
        states = set(dpda_dict["states"])
        start_state = dpda_dict["start_state"]
        final_states = set(dpda_dict["final_states"])

    except Exception as exc:
        print(f"[X] Exception raised during JSON Parse: {exc}")
        exit()

    assert start_state in states, "[X] Start state not in state set."
    assert final_states.issubset(
        states
    ), "[X] Final States are not subset of state set."

    return dpda_dict


def print_transitions(transitions):

    """
    Helper to print transitions in special format.
    """

    for x in transitions:
        print(f"\t{x[0]} --[{x[1]}, {x[2]}, {x[4]}]-> {x[3]}")


def print_dpda(dpda_dict):

    """
    Helper to print the transitions and states associated with
    a DPDA in a readable format.
    """

    print(
        f"""[-] DPDA with:
    States: {set(dpda_dict['states'])}
    Start State: {{{dpda_dict['start_state']}}}
    Final States: {set(dpda_dict['final_states'])}
    Transitions:"""
    )
    print_transitions(dpda_dict["transition_functions"])


def choose_next_state(current_state, character, stack, dpda_dict, transition_path):

    """
    Chooses what move to make, and makes it.

    This entails filtering the set of all transitions based on the
    state we are in, the value at the top of the stack and the
    character we are processing.

    Should we return 2 or more applicable transitions, this will
    show there is nondeterminism in the PDA, which will generate a
    failure.

    Should we find no possible transitions, we are in a final
    state and must decide what to do: accept or reject.

    The rest of the function updates the stack, the trace/path and
    prepares for the next run.

    Arguments: The current state, the current character, the current stack,
        dictionary representing the DPDA, the current transition path.
    Returns: New stack [reference], new transition path [reference], new state.
    """

    possible_transitions = list(
        filter(
            lambda x: x[0] == current_state
            and (x[1] == character or x[1] == "")
            and (stack[-1] == x[2] or x[2] == ""),
            dpda_dict["transition_functions"],
        )
    )
    print(
        f"""[+] Step:
        Current state {current_state}
        Current character '{character}'
        Stack {stack}
        Found {possible_transitions}."""
    )

    assert (
        len(possible_transitions) <= 1
    ), f"[X] Nondeterminism found on state {current_state}"

    if len(possible_transitions) == 0:
        return None

    # Add to path
    transition_path.append(possible_transitions[0])

    # Set current state
    current_state = possible_transitions[0][3]

    # Stack Update
    stack.pop()
    stack_topush = list(possible_transitions[0][4])
    stack_topush.reverse()
    [stack.append(x) for x in stack_topush if not x == ""]

    return current_state


def dpda_complement(dpda_dict):

    """
    Complement a DPDA. If it is a true DPDA, we can set all
    non terminal states to terminal states, and visa
    versa. We end up with the complement DPDA.

    Arguments: Dictionary representing the DPDA
    Returns: Dictionary represetting complement DPDA to passed dictionary
    """

    accepting_states = dpda_dict["final_states"]
    nonaccepting_states = (
        set(dpda_dict["states"])
        - set(dpda_dict["final_states"])
        # - {dpda_dict["start_state"]}
    )

    print(
        f"""[-] Generating Complement Acceptor: Swapping:
        Accepting States: {{{accepting_states}}}
        Nonaccepting States: {{{nonaccepting_states}}}"""
    )

    complement_dict = dpda_dict

    complement_dict["final_states"] = list(nonaccepting_states)

    return complement_dict


def dpda_run(dpda_dict):

    """
    Function to seek input and run the DPDA provided.
    This function iterates over the word until a terminal
    condition is reached.

    Arguments: Dictionary representing the DPDA
    Returns: Nothing
    """

    word = input("[>] Please input a word to test:")
    transition_path = []
    stack = ["Z"]
    current_state = dpda_dict["start_state"]

    # Iterate until we are done
    while True:

        character = "" if len(word) == 0 else word[0]
        if not word == "":
            word = word[1:]

        result_state = choose_next_state(
            current_state, character, stack, dpda_dict, transition_path
        )

        if result_state == None and word == "":
            print(f"[=] Terminated at state {current_state}")
            if current_state in dpda_dict["final_states"]:
                print(f"[=] Result: Accepted with path:")
                print_transitions(transition_path)
            else:
                print(f"[=] Result: Rejected with path:")
                print_transitions(transition_path)
            return
        elif result_state == None and word != "":
            print(f"[=] Terminated at state {current_state}")
            print(f"[=] Result: Rejected with path:")
            print_transitions(transition_path)
            return
        else:
            print(f"[+] Chose next state {current_state}")
            current_state = result_state
    return


if __name__ == "__main__":

    """
    Main Function. Reads input file, calls associated functions.
    """

    assert (
        len(sys.argv) == 2
    ), "[X] Please pass the JSON DPDA Definition file as an argument."

    input_file = os.path.abspath(sys.argv[1])

    print(f"[-] Found input file {input_file}")

    dpda_dict = check_parse_file(input_file)
    print_dpda(dpda_dict)

    dpda_run(dpda_dict)

    dpda_dict_complement = dpda_complement(dpda_dict)
    print_dpda(dpda_dict_complement)

    dpda_run(dpda_dict_complement)
