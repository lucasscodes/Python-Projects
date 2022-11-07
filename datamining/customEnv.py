#Examples: https://github.com/openai/gym/tree/master/gym/envs

#pip install gym==0.18.3
import gym
import numpy as np
import time
from IPython.display import display, clear_output
from matplotlib import pyplot as plt

class CustomEnv(gym.Env):
    ACTIONS = {
        'up': 0,
        'left': 1,
        'down': 2,
        'right': 3,
    }
    SIZE = 8
    TARGET_X = 5
    TARGET_Y = 5
    REWARD_TARGET_REACHED = 1.0
    PENALTY = -0.1

    metadata = {'render.modes': ['human']}

    state: int

    def __init__(self):
        super(CustomEnv, self).__init__()

        self.action_space = gym.spaces.Discrete(len(CustomEnv.ACTIONS))
        self.observation_space = gym.spaces.Box(
            low=0,
            high=CustomEnv.SIZE - 1,
            shape=(2,),
            dtype=np.uint8
        )

        self.reset()
        
    def step(self, action):
        (agent_x, agent_y) = CustomEnv.decode_state(self.state)

        if action == CustomEnv.encode_action('up'):
            agent_y = max(agent_y - 1, 0)
        elif action == CustomEnv.encode_action('left'):
            agent_x = max(agent_x - 1, 0)
        elif action == CustomEnv.encode_action('down'):
            agent_y = min(agent_y + 1, CustomEnv.SIZE - 1)
        elif action == CustomEnv.encode_action('right'):
            agent_x = min(agent_x + 1, CustomEnv.SIZE - 1)
        else: # invalid
            raise Exception()

        self.state = CustomEnv.encode_state(agent_x, agent_y)

        if agent_x == CustomEnv.TARGET_X and agent_y == CustomEnv.TARGET_Y: # agent has reached target
            return self.state, CustomEnv.REWARD_TARGET_REACHED, True, None
        else:
            return self.state, CustomEnv.PENALTY, False, None

     
    def reset(self):
        sample = self.observation_space.sample()

        self.state = CustomEnv.encode_state(sample[0], sample[1])
        return self.state
        
    def render(self):
        target = 'x'
        reached_target = 'X'
        agent = 'Δ'
        empty = '·'

        output = ""

        (agent_x, agent_y) = CustomEnv.decode_state(self.state)

        for y in range(0, CustomEnv.SIZE):
            if y != 0:
                output += '\n'

            for x in range(0, CustomEnv.SIZE):
                if agent_x == CustomEnv.TARGET_X == x and agent_y == CustomEnv.TARGET_Y == y:
                    output += reached_target
                elif agent_x == x and agent_y == y:
                    output += agent
                elif CustomEnv.TARGET_X == x and CustomEnv.TARGET_Y == y:
                    output += target
                else:
                    output += empty

        print(output)

    @staticmethod
    def encode_action(action):
        """
        Encodes an action's string representation to its int form

        :param action: The action to encode; valid are 'up', 'left', 'down' and 'right'
        :return: The action's in form
        """
        return CustomEnv.ACTIONS[action]

    @staticmethod
    def decode_state(state):
        """
        Decodes a state's int representation to its 2D form

        :param state: The state to decode
        :return: The state in 2D representation; structured like (agent_x, agent_y)
        """
        agent_y = state % CustomEnv.SIZE
        state //= CustomEnv.SIZE

        agent_x = state

        return agent_x, agent_y

    @staticmethod
    def encode_state(agent_x, agent_y):
        """
        Encodes a state in its 2D form to its int representation

        :param agent_y: The agent's x-coordinate
        :param agent_x: The agent's y-coordinate
        :return: The state in int representation
        """
        return agent_x * CustomEnv.SIZE +\
               agent_y

env = CustomEnv()
done = False # set to false to execute cell
while not done:
    a = env.action_space.sample()
    _,_, done,_ = env.step(a)
    clear_output(wait=True)
    env.render()
    time.sleep(0.05)

def init_table():
    states = CustomEnv.SIZE**2
    actions = len(CustomEnv.ACTIONS)
    return np.zeros((states, actions))

table = init_table()

def exploit(state):
    return np.argmax(table[state])

def explore(state):
    return env.action_space.sample()

epsilon = 0.1

def eps_greedy(state):
    if np.random.rand() < epsilon:
        return explore(state)
    else:
        return exploit(state)

gamma = 0.99

# All significant changes are made here
def td_error(s, a, r, s_prime):
    return r + gamma * np.max(table[s_prime, :]) - table[s, a]

eta = 0.1

def update_table(s, a, delta):
    table[s, a] = table[s, a] + eta * delta

Q_LEARNING_EPISODES = 200

def train():
    cumulative_rewards = []

    for i in range(Q_LEARNING_EPISODES):
        cumulative_reward = 0

        state = env.reset()
        action = eps_greedy(state)

        done = False
        while not done:
            next_state, reward, done, _ = env.step(action)
            next_action = eps_greedy(next_state)

            delta = td_error(state, action, reward, next_state)
            update_table(state, action, delta)

            state = next_state
            action = next_action

            cumulative_reward += reward

        cumulative_rewards.append(cumulative_reward)

    return cumulative_rewards

q_learning_evaluation = train()

plt.title("Cumulative Rewards (Q-Learning)")
plt.plot(q_learning_evaluation)
plt.xlabel("Episode")
plt.ylabel("Cumulative Reward")
plt.show()

