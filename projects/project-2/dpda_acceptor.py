#!/usr/bin/env python3

import json
import os
import sys


def check_parse_file(filename):

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

    for x in transitions:
        print(f"\t{x[0]} --[{x[1]}, {x[2]}, {x[4]}]-> {x[3]}")


def print_dpda(dpda_dict):
    print(
        f"""[-] DPDA with:
    States: {set(dpda_dict['states'])}
    Start State: {{{dpda_dict['start_state']}}}
    Final States: {set(dpda_dict['final_states'])}
    Transitions:"""
    )
    print_transitions(dpda_dict["transition_functions"])


def choose_next_state(current_state, character, stack, dpda_dict, transition_path):

    possible_transitions = list(
        filter(
            lambda x: x[0] == current_state
            and x[1] == character
            and (stack[-1] == x[2] or x[2] == ""),
            dpda_dict["transition_functions"],
        )
    )
    print(
        f"[+] Step: \n\tCurrent state {current_state}\n\tCurrent character '{character}'\n\tStack {stack}\n\tFound {possible_transitions}."
    )

    assert len(possible_transitions) <= 2, "[X] Bad number of transitions found."

    if len(possible_transitions) == 0:
        print(f"[=] Result: Rejected with path:")
        print_transitions(transition_path)
        return None

    transition_path.append(possible_transitions[0])

    current_state = possible_transitions[0][3]
    stack.pop()
    stack_topush = list(possible_transitions[0][4])
    stack_topush.reverse()
    [stack.append(x) for x in stack_topush if not x == ""]

    return current_state


def dpda_complement(dpda_dict):

    accepting_states = dpda_dict["final_states"]
    nonaccepting_states = (
        set(dpda_dict["states"])
        - set(dpda_dict["final_states"])
        - {dpda_dict["start_state"]}
    )

    print(
        f"[-] Generating Complement Acceptor: Swapping:\n\tAccepting States: {{{accepting_states}}}\n\tNonaccepting States: {{{nonaccepting_states}}}"
    )

    complement_dict = dpda_dict

    complement_dict["final_states"] = list(nonaccepting_states)

    return complement_dict


def dpda_run(dpda_dict):

    word = input("Please input a word to test:")
    transition_path = []
    stack = ["Z"]
    current_state = dpda_dict["start_state"]

    while (not (current_state in dpda_dict["final_states"])) or (word != ""):

        character = "" if len(word) == 0 else word[0]
        if not word == "":
            word = word[1:]

        result_state = choose_next_state(
            current_state, character, stack, dpda_dict, transition_path
        )

        if result_state == None:
            print(f"[=] Terminated at state {current_state}")
            return
        else:
            print(f"[+] Chose next state {current_state}")
            current_state = result_state

    print(f"[=] Result: Accepted with path:")
    print_transitions(transition_path)
    return


if __name__ == "__main__":

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
