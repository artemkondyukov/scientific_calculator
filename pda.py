class PDA:
    # Implementation of push-down automaton
    def __init__(self, states, current_state=None):
        """
        Creates a new push-down automaton
        :param states: dictionary, keys are name of states, values are functions
        handling a token given (must have input parameter and return nothing in
        case of successful consuming token and an error message otherwise
        :return:
        """
        self.states = {}
        for name, function in states.items():
            self.states[name] = function
        if current_state is not None:
            if current_state in self.states:
                self.current_state = current_state
            else:
                raise ValueError("Invalid current state given")
        else:
            self.current_state = list(states.keys())[0] if len(list(states.keys)) > 0 else None
        self.stack = []

    def consume_token(self, token):
        return self.states[self.current_state](token)
