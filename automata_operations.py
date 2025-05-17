from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
import json
import os

@dataclass
class Automaton:
    """Base class representing a finite automaton"""
    states: Set[str]
    alphabet: Set[str]
    transitions: Dict[Tuple[str, str], Set[str]]  # (state, symbol) -> set of target states
    initial_state: str
    final_states: Set[str]
    name: str = "Untitled Automaton"

class AutomataManager:
    """Handles basic automata management operations"""
    def __init__(self):
        self.current_automaton: Optional[Automaton] = None
        self.automata_dir = "saved_automatas"
        # Ensure the directory exists
        if not os.path.exists(self.automata_dir):
            os.makedirs(self.automata_dir)
    
    def create_automaton(self, states: Set[str], alphabet: Set[str], 
                        transitions: Dict[Tuple[str, str], Set[str]],
                        initial_state: str, final_states: Set[str], 
                        name: str = "Untitled") -> Automaton:
        """Create a new automaton with the given components"""
        try:
            # Validate inputs
            if not states:
                raise ValueError("States set cannot be empty")
            if not alphabet:
                raise ValueError("Alphabet cannot be empty")
            if not initial_state in states:
                raise ValueError("Initial state must be in states set")
            if not final_states.issubset(states):
                raise ValueError("Final states must be a subset of states")
            
            # Validate transitions
            for (state, symbol), targets in transitions.items():
                if state not in states:
                    raise ValueError(f"Invalid source state in transition: {state}")
                if symbol not in alphabet:
                    raise ValueError(f"Invalid symbol in transition: {symbol}")
                if not targets.issubset(states):
                    raise ValueError(f"Invalid target state(s) in transition from {state} on {symbol}")
            
            # Create and return the automaton
            self.current_automaton = Automaton(
                states=states,
                alphabet=alphabet,
                transitions=transitions,
                initial_state=initial_state,
                final_states=final_states,
                name=name
            )
            return self.current_automaton
            
        except Exception as e:
            raise ValueError(f"Failed to create automaton: {str(e)}")
    
    def save_automaton(self, filename: str = None) -> bool:
        """Save the current automaton to a file in the saved_automatas directory"""
        if not self.current_automaton:
            return False
            
        if not filename:
            filename = f"{self.current_automaton.name}.json"
            
        # Ensure the filename has .json extension
        if not filename.endswith('.json'):
            filename += '.json'
            
        # Create full path in saved_automatas directory
        filepath = os.path.join(self.automata_dir, filename)
        
        # Convert automaton to serializable format
        data = {
            "name": self.current_automaton.name,
            "states": list(self.current_automaton.states),
            "alphabet": list(self.current_automaton.alphabet),
            "transitions": {
                f"{state},{symbol}": list(targets)
                for (state, symbol), targets in self.current_automaton.transitions.items()
            },
            "initial_state": self.current_automaton.initial_state,
            "final_states": list(self.current_automaton.final_states)
        }
        
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False
    
    def load_automaton(self, filename: str, preview: bool = False) -> Optional[Automaton]:
        """Load an automaton from the saved_automatas directory.
        If preview=True, returns a new Automaton instance without setting it as current_automaton"""
        try:
            # Create full path in saved_automatas directory
            filepath = os.path.join(self.automata_dir, filename)
            
            with open(filepath, 'r') as f:
                data = json.load(f)
                
            # Validate required fields
            required_fields = ['name', 'states', 'alphabet', 'transitions', 
                             'initial_state', 'final_states']
            for field in required_fields:
                if field not in data:
                    raise ValueError(f"Missing required field: {field}")
                    
            # Validate data types
            if not isinstance(data['states'], list):
                raise ValueError("States must be a list")
            if not isinstance(data['alphabet'], list):
                raise ValueError("Alphabet must be a list")
            if not isinstance(data['transitions'], dict):
                raise ValueError("Transitions must be a dictionary")
            if not isinstance(data['final_states'], list):
                raise ValueError("Final states must be a list")
                
            # Convert data back to proper types
            states = set(data['states'])
            alphabet = set(data['alphabet'])
            final_states = set(data['final_states'])
            
            # Validate initial state
            if data['initial_state'] not in states:
                raise ValueError("Initial state must be in states set")
                
            # Validate final states
            if not final_states.issubset(states):
                raise ValueError("Final states must be a subset of states")
                
            # Parse and validate transitions
            transitions = {}            
            for key, targets in data['transitions'].items():
                try:
                    # Split from the right once to handle states that contain commas
                    state, symbol = key.rsplit(',', 1)
                    if state not in states:
                        raise ValueError(f"Invalid source state in transition: {state}")
                    if symbol not in alphabet:
                        raise ValueError(f"Invalid symbol in transition: {symbol}")
                        
                    target_set = set(targets)
                    if not target_set.issubset(states):
                        raise ValueError(f"Invalid target state(s) in transition from {state} on {symbol}")
                        
                    transitions[(state, symbol)] = target_set
                except ValueError as e:
                    raise ValueError(f"Invalid transition format: {key}. {str(e)}")
            # Create the automaton instance
            automaton = Automaton(
                states=states,
                alphabet=alphabet,
                transitions=transitions,
                initial_state=data['initial_state'],
                final_states=final_states,
                name=data['name']
            )
            
            # Only set as current_automaton if not in preview mode
            if not preview:
                self.current_automaton = automaton
                
            return automaton
            
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
        except Exception as e:
            raise ValueError(f"Failed to load automaton: {str(e)}")

    def list_saved_automata(self) -> List[str]:
        """List all saved automata files from the saved_automatas directory"""
        if not os.path.exists(self.automata_dir):
            return []
        return [f for f in os.listdir(self.automata_dir) if f.endswith('.json')]
    
    def delete_automaton(self, filename: str) -> bool:
        """Delete a saved automaton file from the saved_automatas directory"""
        try:
            filepath = os.path.join(self.automata_dir, filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception:
            return False

class AutomataAnalyzer:
    """Handles analysis operations on automata"""
    @staticmethod
    def is_deterministic(automaton: Automaton) -> bool:
        """Check if the automaton is deterministic"""
        # Check if there's exactly one initial state
        if not automaton.initial_state:
            return False
            
        # Check if each state has exactly one transition for each symbol
        for state in automaton.states:
            for symbol in automaton.alphabet:
                targets = automaton.transitions.get((state, symbol), set())
                if len(targets) != 1:
                    return False
        return True
    
    @staticmethod
    def is_complete(automaton: Automaton) -> bool:
        """Check if the automaton is complete"""
        for state in automaton.states:
            for symbol in automaton.alphabet:
                if not automaton.transitions.get((state, symbol)):
                    return False
        return True
    
    @staticmethod
    def make_complete(automaton: Automaton) -> Automaton:
        """Make the automaton complete by adding a trap state"""
        # Create a copy of the automaton
        new_states = automaton.states | {"trap"}
        new_transitions = dict(automaton.transitions)
        
        # Add missing transitions to trap state
        for state in automaton.states:
            for symbol in automaton.alphabet:
                if not new_transitions.get((state, symbol)):
                    new_transitions[(state, symbol)] = {"trap"}
                    
        # Add trap state transitions
        for symbol in automaton.alphabet:
            new_transitions[("trap", symbol)] = {"trap"}
            
        return Automaton(
            states=new_states,
            alphabet=automaton.alphabet,
            transitions=new_transitions,
            initial_state=automaton.initial_state,
            final_states=automaton.final_states,
            name=f"{automaton.name}_complete"
        )
    
    @staticmethod
    def nfa_to_dfa(automaton: Automaton) -> Automaton:
        """Convert an NFA to an equivalent DFA using subset construction."""
        from collections import deque
        # Each DFA state is a frozenset of NFA states
        dfa_states = set()
        dfa_transitions = dict()
        dfa_final_states = set()
        state_name_map = dict()  # frozenset -> string name
        queue = deque()

        # Start state is the set containing only the NFA initial state
        start_set = frozenset([automaton.initial_state])
        queue.append(start_set)
        dfa_states.add(start_set)
        state_name_map[start_set] = 'S0'
        name_counter = 1

        # If any NFA state in a DFA state is final, the DFA state is final
        if automaton.final_states & start_set:
            dfa_final_states.add('S0')

        while queue:
            current = queue.popleft()
            current_name = state_name_map[current]
            for symbol in automaton.alphabet:
                # Compute the set of NFA states reachable from any state in current on symbol
                next_set = set()
                for nfa_state in current:
                    next_set.update(automaton.transitions.get((nfa_state, symbol), set()))
                next_frozen = frozenset(next_set)
                if not next_frozen:
                    continue  # No transition for this symbol
                if next_frozen not in dfa_states:
                    dfa_states.add(next_frozen)
                    state_name_map[next_frozen] = f'S{name_counter}'
                    if automaton.final_states & next_frozen:
                        dfa_final_states.add(state_name_map[next_frozen])
                    queue.append(next_frozen)
                    name_counter += 1
                dfa_transitions[(current_name, symbol)] = {state_name_map[next_frozen]}

        # Build DFA state names
        dfa_state_names = set(state_name_map.values())
        dfa_initial_state = 'S0'
        dfa = Automaton(
            states=dfa_state_names,
            alphabet=automaton.alphabet,
            transitions=dfa_transitions,
            initial_state=dfa_initial_state,
            final_states=dfa_final_states,
            name=automaton.name + '_dfa'
        )
        return dfa

    @staticmethod
    def is_minimal_dfa(automaton: Automaton) -> Tuple[bool, Optional[Set[frozenset]]]:
        """Check if a DFA is minimal. Returns (is_minimal, partition) where partition is the set of state groups."""
        # Only works for DFA
        if not AutomataAnalyzer.is_deterministic(automaton):
            return False, None
        # Remove unreachable states
        reachable = set()
        queue = [automaton.initial_state]
        while queue:
            state = queue.pop()
            if state in reachable:
                continue
            reachable.add(state)
            for symbol in automaton.alphabet:
                targets = automaton.transitions.get((state, symbol), set())
                for t in targets:
                    if t not in reachable:
                        queue.append(t)
        # Hopcroft's partition refinement
        F = automaton.final_states & reachable
        NF = reachable - F
        if not F or not NF:
            # Trivial DFA (all states final or all non-final)
            return True, {frozenset(reachable)}
        partition = [set(F), set(NF)]
        worklist = [set(F), set(NF)]
        while worklist:
            A = worklist.pop()
            for symbol in automaton.alphabet:
                pre = set()
                for (state, sym), targets in automaton.transitions.items():
                    if sym == symbol and any(t in A for t in targets):
                        pre.add(state)
                new_partition = []
                for Y in partition:
                    inter = Y & pre
                    diff = Y - pre
                    if inter and diff:
                        new_partition.extend([inter, diff])
                        if Y in worklist:
                            worklist.remove(Y)
                            worklist.extend([inter, diff])
                        else:
                            if len(inter) <= len(diff):
                                worklist.append(inter)
                            else:
                                worklist.append(diff)
                    else:
                        new_partition.append(Y)
                partition = new_partition
        # If number of groups == number of reachable states, DFA is minimal
        num_groups = len(partition)
        if num_groups == len(reachable):
            return True, {frozenset(g) for g in partition}
        else:
            return False, {frozenset(g) for g in partition}

    @staticmethod
    def minimize_dfa(automaton: Automaton) -> Automaton:
        """Minimize a DFA using partition refinement (Hopcroft's algorithm). Returns a new minimized DFA."""
        if not AutomataAnalyzer.is_deterministic(automaton):
            raise ValueError("Minimization requires a deterministic automaton (DFA).")
        # Remove unreachable states
        reachable = set()
        queue = [automaton.initial_state]
        while queue:
            state = queue.pop()
            if state in reachable:
                continue
            reachable.add(state)
            for symbol in automaton.alphabet:
                targets = automaton.transitions.get((state, symbol), set())
                for t in targets:
                    if t not in reachable:
                        queue.append(t)
        F = automaton.final_states & reachable
        NF = reachable - F
        if not F or not NF:
            # Trivial DFA (all states final or all non-final)
            return Automaton(
                states=set(reachable),
                alphabet=automaton.alphabet,
                transitions={k: v for k, v in automaton.transitions.items() if k[0] in reachable},
                initial_state=automaton.initial_state,
                final_states=F,
                name=automaton.name + '_minimized'
            )
        partition = [set(F), set(NF)]
        worklist = [set(F), set(NF)]
        while worklist:
            A = worklist.pop()
            for symbol in automaton.alphabet:
                pre = set()
                for (state, sym), targets in automaton.transitions.items():
                    if sym == symbol and any(t in A for t in targets):
                        pre.add(state)
                new_partition = []
                for Y in partition:
                    inter = Y & pre
                    diff = Y - pre
                    if inter and diff:
                        new_partition.extend([inter, diff])
                        if Y in worklist:
                            worklist.remove(Y)
                            worklist.extend([inter, diff])
                        else:
                            if len(inter) <= len(diff):
                                worklist.append(inter)
                            else:
                                worklist.append(diff)
                    else:
                        new_partition.append(Y)
                partition = new_partition
        # Build state name mapping: frozenset -> new state name
        group_names = {}
        for idx, group in enumerate(partition):
            group_names[frozenset(group)] = f'M{idx}'
        # Find which group contains the initial state
        for group in partition:
            if automaton.initial_state in group:
                new_initial = group_names[frozenset(group)]
                break
        # New final states
        new_finals = set()
        for group in partition:
            if group & automaton.final_states:
                new_finals.add(group_names[frozenset(group)])
        # Build new transitions
        new_transitions = {}
        for group in partition:
            rep = next(iter(group))
            for symbol in automaton.alphabet:
                target = next(iter(automaton.transitions.get((rep, symbol), set())), None)
                if target is not None:
                    # Find the group containing the target
                    for g2 in partition:
                        if target in g2:
                            new_transitions[(group_names[frozenset(group)], symbol)] = {group_names[frozenset(g2)]}
                            break
        return Automaton(
            states=set(group_names.values()),
            alphabet=automaton.alphabet,
            transitions=new_transitions,
            initial_state=new_initial,
            final_states=new_finals,
            name=automaton.name + '_minimized'
        )

    @staticmethod
    def compute_union(automaton1: Automaton, automaton2: Automaton) -> Automaton:
        """Compute the union of two automata. The resulting automaton accepts strings accepted by either automaton."""
        # Verify alphabets match
        if automaton1.alphabet != automaton2.alphabet:
            raise ValueError("Both automata must have the same alphabet")

        # Convert to DFAs if needed
        if not AutomataAnalyzer.is_deterministic(automaton1):
            automaton1 = AutomataAnalyzer.nfa_to_dfa(automaton1)
        if not AutomataAnalyzer.is_deterministic(automaton2):
            automaton2 = AutomataAnalyzer.nfa_to_dfa(automaton2)

        # Create states as pairs
        states = {f"({q1},{q2})" for q1 in automaton1.states for q2 in automaton2.states}
        
        # Initial state is pair of initial states
        initial_state = f"({automaton1.initial_state},{automaton2.initial_state})"
        
        # Final states are pairs where at least one state is final
        final_states = {
            f"({q1},{q2})" 
            for q1 in automaton1.states 
            for q2 in automaton2.states 
            if q1 in automaton1.final_states or q2 in automaton2.final_states
        }

        # Build transitions for the product automaton
        transitions = {}
        for q1 in automaton1.states:
            for q2 in automaton2.states:
                for symbol in automaton1.alphabet:
                    # Get next states from both automata
                    next_q1 = next(iter(automaton1.transitions.get((q1, symbol), set())))
                    next_q2 = next(iter(automaton2.transitions.get((q2, symbol), set())))
                    current_state = f"({q1},{q2})"
                    next_state = f"({next_q1},{next_q2})"
                    transitions[(current_state, symbol)] = {next_state}

        return Automaton(
            states=states,
            alphabet=automaton1.alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
            name=f"{automaton1.name}_{automaton2.name}_union"
        )
    
    @staticmethod
    def compute_intersection(automaton1: Automaton, automaton2: Automaton) -> Automaton:
        """Compute the intersection of two automata. The resulting automaton accepts only strings accepted by both automata."""
        # Verify alphabets match
        if automaton1.alphabet != automaton2.alphabet:
            raise ValueError("Both automata must have the same alphabet")

        # Convert to DFAs if needed
        if not AutomataAnalyzer.is_deterministic(automaton1):
            automaton1 = AutomataAnalyzer.nfa_to_dfa(automaton1)
        if not AutomataAnalyzer.is_deterministic(automaton2):
            automaton2 = AutomataAnalyzer.nfa_to_dfa(automaton2)

        # Create states as pairs
        states = {f"({q1},{q2})" for q1 in automaton1.states for q2 in automaton2.states}
        
        # Initial state is pair of initial states
        initial_state = f"({automaton1.initial_state},{automaton2.initial_state})"
        
        # Final states are pairs where BOTH states are final (unlike union where we use 'or')
        final_states = {
            f"({q1},{q2})" 
            for q1 in automaton1.states 
            for q2 in automaton2.states 
            if q1 in automaton1.final_states and q2 in automaton2.final_states
        }

        # Build transitions for the product automaton
        transitions = {}
        for q1 in automaton1.states:
            for q2 in automaton2.states:
                for symbol in automaton1.alphabet:
                    # Get next states from both automata
                    next_q1 = next(iter(automaton1.transitions.get((q1, symbol), set())))
                    next_q2 = next(iter(automaton2.transitions.get((q2, symbol), set())))
                    current_state = f"({q1},{q2})"
                    next_state = f"({next_q1},{next_q2})"
                    transitions[(current_state, symbol)] = {next_state}

        return Automaton(
            states=states,
            alphabet=automaton1.alphabet,
            transitions=transitions,
            initial_state=initial_state,
            final_states=final_states,
            name=f"intersection_{automaton1.name}_{automaton2.name}"
        )
    
    @staticmethod
    def compute_complement(automaton: Automaton) -> Automaton:
        """Compute the complement of a DFA. The resulting automaton accepts strings rejected by the input automaton and rejects strings accepted by it.
        
        The input automaton must be deterministic and complete.
        The complement operation simply swaps the final and non-final states while keeping everything else the same.
        
        Args:
            automaton (Automaton): A deterministic and complete automaton to complement.
            
        Returns:
            Automaton: A new automaton that is the complement of the input automaton.
            
        Raises:
            ValueError: If the input automaton is not deterministic or not complete.
        """
        # Verify automaton is deterministic
        if not AutomataAnalyzer.is_deterministic(automaton):
            raise ValueError("The automaton must be deterministic")
            
        # Verify automaton is complete
        if not AutomataAnalyzer.is_complete(automaton):
            raise ValueError("The automaton must be complete")
            
        # Create the complement automaton by swapping final and non-final states
        complement_final_states = automaton.states - automaton.final_states
        
        return Automaton(
            states=automaton.states,
            alphabet=automaton.alphabet,
            transitions=automaton.transitions,
            initial_state=automaton.initial_state,
            final_states=complement_final_states,
            name=f"{automaton.name}_complement"
        )

class WordProcessor:
    """Handles word and language operations"""
    @staticmethod
    def accepts_word(automaton: Automaton, word: str) -> bool:
        """Check if the automaton accepts a given word"""
        current_states = {automaton.initial_state}
        
        for symbol in word:
            if symbol not in automaton.alphabet:
                return False
                
            next_states = set()
            for state in current_states:
                targets = automaton.transitions.get((state, symbol), set())
                next_states.update(targets)
            
            if not next_states:
                return False
                
            current_states = next_states
        
        # Check if any current state is final
        return bool(current_states & automaton.final_states)
    
    @staticmethod
    def generate_words(automaton: Automaton, max_length: int = 5) -> List[str]:
        """Generate words accepted by the automaton up to max_length"""
        accepted_words = []
        
        def explore(current_state: str, current_word: str):
            if len(current_word) > max_length:
                return
            if current_state in automaton.final_states:
                accepted_words.append(current_word)
                
            for symbol in automaton.alphabet:
                for next_state in automaton.transitions.get((current_state, symbol), set()):
                    explore(next_state, current_word + symbol)
        
        explore(automaton.initial_state, "")
        return sorted(accepted_words, key=len)

    @staticmethod
    def generate_all_words(alphabet: Set[str], length: int) -> List[str]:
        """Generate all possible words of given length using the given alphabet"""
        if length == 0:
            return [""]
            
        words = []
        shorter_words = WordProcessor.generate_all_words(alphabet, length - 1)
        for word in shorter_words:
            for symbol in sorted(alphabet):  # Sort for consistent order
                words.append(word + symbol)
                
        return words

class Visualizer:
    """Handles automaton visualization using Graphviz"""
    @staticmethod
    def to_dot(automaton: Automaton) -> str:
        """Convert automaton to DOT format for visualization"""
        dot = ["digraph {", 
               "  rankdir=LR;",
               "  node [shape=circle fontname=\"Arial\" fontsize=12];",
               "  edge [fontname=\"Arial\" fontsize=10];",
               
               "  # Add invisible start node",
               "  start [shape=none label=\"\"];"]
        
        # Style for final states (double circle)
        for state in automaton.final_states:
            dot.append(f'  "{state}" [shape=doublecircle];')
            
        # Style for non-final states (single circle)
        for state in automaton.states - automaton.final_states:
            dot.append(f'  "{state}" [shape=circle];')
        
        # Add initial state transition
        dot.append(f'  start -> "{automaton.initial_state}";')
        
        # Add all other transitions
        for (state, symbol), targets in automaton.transitions.items():
            for target in targets:
                dot.append(f'  "{state}" -> "{target}" [label="{symbol}"];')
        
        dot.append("}")
        return "\n".join(dot)
        
    @staticmethod
    def render_automaton(automaton: Automaton, output_path: str = None, format: str = 'png') -> str:
        """
        Render the automaton visualization using Graphviz.
        Returns the path to the generated file.
        """
        import graphviz
        if not automaton:
            raise ValueError("No automaton provided for visualization")
            
        # Create a graphviz.Source object from the DOT representation
        dot = graphviz.Source(Visualizer.to_dot(automaton))
        
        # If no output path specified, use a default name based on the automaton name
        if not output_path:
            output_path = f"automaton_{automaton.name}"
            
        # Render the graph
        try:
            rendered_path = dot.render(output_path, format=format, cleanup=True)
            return rendered_path
        except Exception as e:
            raise Exception(f"Failed to render automaton: {str(e)}")
            
    @staticmethod
    def get_svg_content(automaton: Automaton) -> str:
        """
        Generate SVG content for the automaton.
        Useful for displaying in the GUI without saving to file.
        """
        import graphviz
        if not automaton:
            return ""
            
        dot = graphviz.Source(Visualizer.to_dot(automaton))
        try:
            # Generate SVG content directly
            svg_content = dot.pipe(format='svg').decode('utf-8')
            return svg_content
        except Exception as e:
            raise Exception(f"Failed to generate SVG: {str(e)}")
