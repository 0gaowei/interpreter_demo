class DFAState:
    def __init__(self, name, is_accepting=False):
        self.name = name
        self.is_accepting = is_accepting  # 是否是接受状态
        self.transitions = {}  # 输入字符 -> 转移到的下一个状态\

    def add_transition(self, char_class, next_state):
        self.transitions[char_class] = next_state

    def get_next_state(self, char_class):
        if char_class not in self.transitions:
            return None
        return self.transitions[char_class]


class DFA:
    def __init__(self):
        # 创建DFA状态
        self.start_state = DFAState("START")
        self.state_1 = DFAState("ID", is_accepting=True)
        self.state_2 = DFAState("NUMBER", is_accepting=True)
        self.state_3 = DFAState("POINT", is_accepting=True)
        self.state_4 = DFAState("MUL", is_accepting=True)
        self.state_5 = DFAState("MIX", is_accepting=True)
        self.state_6 = DFAState("/", is_accepting=True)
        self.state_7 = DFAState("MINUS", is_accepting=True)
        self.curr_state = self.start_state  # 当前状态

        # 状态0的转移
        self.start_state.add_transition('letter', self.state_1)
        self.start_state.add_transition('digit', self.state_2)
        self.start_state.add_transition('*', self.state_4)
        self.start_state.add_transition('/', self.state_6)
        self.start_state.add_transition('-', self.state_7)
        self.start_state.add_transition('+', self.state_5)
        self.start_state.add_transition(',', self.state_5)
        self.start_state.add_transition(';', self.state_5)
        self.start_state.add_transition('(', self.state_5)
        self.start_state.add_transition(')', self.state_5)
        # 状态1的转移
        self.state_1.add_transition('letter', self.state_1)
        self.state_1.add_transition('digit', self.state_1)
        # 状态2的转移
        self.state_2.add_transition('digit', self.state_2)
        self.state_2.add_transition('.', self.state_3)
        # 状态3的转移
        self.state_3.add_transition('digit', self.state_3)
        # 状态4的转移
        self.state_4.add_transition('*', self.state_5)
        # 状态6的转移
        self.state_6.add_transition('/', self.state_5)
        # 状态7的转移
        self.state_7.add_transition('-', self.state_5)
