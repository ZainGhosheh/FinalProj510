"""
EECS 510 - Final Project
Finite Automaton Implementation
Authors: Ahmad Awan, Abdulahi Mohamed, Zain Ghosheh

Description:
This project implements a finite automaton to recognize a formal language representing arithmetic expressions. 
The automaton is defined using states, transitions, and input symbols, and can be constructed dynamically 
from a file. It includes functionality to test if strings are accepted or rejected by the language.
"""


import os

class FiniteAutomaton: # Class to represent a finite automaton.
    def __init__(self, states, input_symbols, transitions, start_state, accept_states, symbol_groups): 
        # Initialize the finite automaton with its states, input symbols, transitions, start state, accept states, and symbol groups.
        self.states = states  
        self.input_symbols = input_symbols  # Symbols the automaton can read.
        self.transitions = transitions  # Dictionary of transitions: {(current_state, symbol): next_state}.
        self.start_state = start_state  # Initial state of the automaton.
        self.accept_states = accept_states  # States where the automaton accepts a string.
        self.symbol_groups = symbol_groups  # Symbol groups to simplify transition definitions (e.g., digits or operators).

    def accepts(self, string):
        # Check if the automaton accepts or rejects a given string.
        current_state = self.start_state  # Start in the initial state.
        print(f"Starting at state: {current_state}")  # Debug output for initial state.

        for symbol in string:  # Process each symbol in the string.
            print(f"Reading symbol: {symbol}") # Debug output for the current symbol.
            matched = False  # Tracks if a matching transition is found.

            # Check if the symbol matches a group (digits or operators).
            for group_name, group_symbols in self.symbol_groups.items(): # Iterate over symbol groups.
                if symbol in group_symbols: # Check if the symbol is in the current group.
                    transition_key = (current_state, group_name) # Define the group transition key.
                    if transition_key in self.transitions:  # Check for group transition.
                        current_state = self.transitions[transition_key] # Transition to the next state.
                        print(f"Transitioned to state: {current_state}") # Debug output for the new state.
                        matched = True # Set matched to True if a transition is found.
                        break  # Exit the group-check loop if a transition is found.

            if not matched: # If no group transition is found, check for a direct transition using the symbol itself.
                if (current_state, symbol) in self.transitions: # Check for a direct transition.
                    current_state = self.transitions[(current_state, symbol)] # Transition to the next state.
                    print(f"Transitioned to state: {current_state}") # Debug output for the new state.
                else: # If no transition is found, reject the string.
                    print(f"No transition found for state: {current_state} and symbol: {symbol}") # Debug output.
                    return "reject" # Reject the string.


        if current_state in self.accept_states: # Check if the final state is an accept state.
            print(f"String accepted in state: {current_state}") # Debug output for accepted string.
            return "accept" # Accept the string.
        print(f"String rejected in state: {current_state}") # Debug output for rejected string.
        return "reject" # Reject the string.

    @staticmethod # Static method to create a FiniteAutomaton instance from a file.
    def from_file(file_path): # File path containing the automaton's definition.
        if not os.path.exists(file_path):  # Check if the file exists.
            raise FileNotFoundError(f"File '{file_path}' not found. Ensure the file exists in the correct directory.") # Raise an error if the file is missing.

        with open(file_path, "r", encoding="utf-8") as file: # Open the file for reading.
            lines = file.readlines()  # Read all lines from the file.
            states = lines[0].strip().split()  # First line contains the states.
            input_symbols = lines[1].strip().split()  # Second line contains input symbols.
            start_state = lines[2].strip()  # Third line is the start state.
            accept_states = lines[3].strip().split()  # Fourth line contains accept states.

            transitions = {} # Initialize an empty dictionary for transitions.
            for line in lines[4:]:  # Remaining lines define transitions.
                parts = line.strip().split() # Split each line into parts.
                if len(parts) == 3:  # Each transition has three parts: state, symbol, next_state.
                    state, symbol, next_state = parts # Unpack the parts into variables.
                    transitions[(state, symbol)] = next_state # Add the transition to the dictionary.

        # Define symbol groups for simplified transitions (digits or operators).
        symbol_groups = {
            "dig": {str(i) for i in range(10)},  # Group for digits (0-9).
            "op": {"+", "-", "*", "/"}  # Group for operators.
        }

        # Return a new FiniteAutomaton instance initialized with the parsed data.
        return FiniteAutomaton(states, input_symbols, transitions, start_state, accept_states, symbol_groups)



def main(): # Main function to test the finite automaton.
    nfa_file = "file.txt"  # File containing the automaton's definition.
    try: # Try to run the main code block.
        if not os.path.exists(nfa_file):  # Ensure the file exists.
            raise FileNotFoundError(f"File '{nfa_file}' not found. Ensure the file exists in the correct directory.") # Raise an error if the file is missing.

        nfa = FiniteAutomaton.from_file(nfa_file)  # Create the automaton from the file.

        # List of strings to test on the automaton.
        strings_to_test = ["3+5$", "1/4*3$", "7-2+1$", "3+5", "5*", "$"]
        for string in strings_to_test:  # Test each string.
            result = nfa.accepts(string)  # Check if the string is accepted or rejected.
            print(f"String '{string}': {result}\n")  # Print the result for each string.

    except FileNotFoundError as e:
        # Handle case where the file is missing.
        print(e) # Print the error message.
    except OSError as e: 
        # Handle other I/O errors.
        print(f"An I/O error occurred: {e}")
    except Exception as e:
        # Handle unexpected errors.
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Run the main function if the script is executed directly.
    main()
