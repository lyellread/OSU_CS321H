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

    print(
        f"[-] Found DPDA with:\n\tstates[{states}]\n\tstart[{start_state}]\n\tfinal[{final_states}]."
    )

    assert start_state in states, "[X] Start state not in state set."
    assert final_states.issubset(
        states
    ), "[X] Final States are not subset of state set."

    return dpda_dict


def print_path(path):

    for x in path:
        print(f"\t{x[0]} --[{x[1]}, {x[2]}, {x[4]}]-> {x[3]}")


def choose_next_state(current_state, character, stack, dpda_dict, transition_path):

    possible_transitions = list(
        filter(
            lambda x: x[0] == current_state and x[1] == character and stack[-1] == x[2],
            dpda_dict["transition_functions"],
        )
    )
    print(
        f"[+] Step: \n\tCurrent state {current_state}\n\tCurrent character '{character}'\n\tStack {stack}\n\tFound {possible_transitions}."
    )

    assert len(possible_transitions) <= 2, "[X] Bad number of transitions found."

    if len(possible_transitions) == 0:
        print(f"[=] Result: Rejected with path:")
        print_path(transition_path)
        exit()

    transition_path.append(possible_transitions[0])

    current_state = possible_transitions[0][3]
    stack.pop()
    stack_topush = list(possible_transitions[0][4])
    stack_topush.reverse()
    [stack.append(x) for x in stack_topush if not x == ""]

    return current_state


def dpda_run(dpda_dict):

    word = input("Please input a word to test:")
    transition_path = []
    stack = ["Z"]
    current_state = dpda_dict["start_state"]

    while (not (current_state in dpda_dict["final_states"])) or (word != ""):

        character = "" if len(word) == 0 else word[0]
        if not word == "":
            word = word[1:]

        current_state = choose_next_state(
            current_state, character, stack, dpda_dict, transition_path
        )

        if current_state == None:
            print(f"[W] Terminated at state {current_state}")
            exit()
        else:
            print(f"[+] Chose next state {current_state}")

    print(f"[=] Result: Accepted with path:")
    print_path(transition_path)
    exit()


if __name__ == "__main__":

    assert (
        len(sys.argv) == 2
    ), "[X] Please pass the JSON DPDA Definition file as an argument."

    input_file = os.path.abspath(sys.argv[1])

    print(f"[-] Found input file {input_file}")

    dpda_dict = check_parse_file(input_file)

    dpda_run(dpda_dict)
