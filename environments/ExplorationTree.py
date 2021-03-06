import numpy as np

from environments.DeterministicMDP import DeterministicMDP
from spaces.DiscreteSpace import DiscreteSpace


class ExplorationTree(DeterministicMDP):

    def __init__(self, name, num_states, N):

        # create the state and action space
        self.inner_size = N
        state_space = DiscreteSpace(2 ** N - 1)
        action_space = DiscreteSpace(3)

        # one maps to 2
        starting_state = 2 ** (N - 1) - 1

        # specify the transition function
        transition_func = np.zeros((2 ** N - 1, 3), dtype=np.int32)

        # iterate over and fill with the transitions
        for i in range(2 ** N - 1):
            transition_func[i, 0] = 2 * i + 1
            transition_func[i, 1] = int((i - 1) / 2)
            transition_func[i, 2] = 2 * i + 2

        # set head and leafs
        transition_func[0, 1] = 0

        for l in range(2 ** (N - 1) - 1, 2 ** N - 1):
            transition_func[l, 0] = l
            transition_func[l, 2] = l

        # now we define the reward function
        reward_function = np.zeros((2 ** N - 1, 3), dtype=np.float64)
        reward_function[2 ** N - 2, 0] = -1
        reward_function[2 ** N - 2, 2] = 1
        reward_function[2 ** (N - 1) - 1, 0] = 2 * (N + 1) / N - 1
        reward_function[2 ** (N - 1) - 1, 2] = 2 * (N + 1) / N - 1

        for state in range(2 ** (N - 1), 2 ** N - 1):
            d = state - 2.0 ** (N - 1)
            print((N - d + 1))
            print((N - d))
            next_rew = ((N - d) / (N - d + 1)) * reward_function[state - 1, 0]
            reward_function[2 ** N - 2, 0] = next_rew
            reward_function[2 ** N - 2, 2] = next_rew

        super().__init__(name, num_states, action_space, state_space, transition_func, reward_function, starting_state)

    def get_name(self):
        return "exp_tree"
